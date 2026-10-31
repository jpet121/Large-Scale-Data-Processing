"""Exclusive private attempt, durable files, then a final completion marker.

All output path components are opened relative to directory descriptors with
O_NOFOLLOW. An existing target is never reused. Files survive failures for local
inspection, but without the marker they are never authoritative.
"""
import hashlib
import json
import os
from pathlib import Path


def directory_fd(path):
    path = Path(os.path.abspath(path))
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


class Publication:
    """Explicit durability seam; production methods perform real local syscalls."""
    def rename(self, fd):
        os.rename('.commit-pending', 'COMMITTED.json', src_dir_fd=fd, dst_dir_fd=fd)

    def sync(self, fd):
        os.fsync(fd)

    def revoke(self, fd):
        os.unlink('COMMITTED.json', dir_fd=fd)


class Files:
    def __init__(self, output, publication=None):
        self.publication = publication or Publication()
        target = Path(os.path.abspath(output))
        parent = directory_fd(target.parent)
        try:
            os.mkdir(target.name, mode=0o700, dir_fd=parent)
            os.fsync(parent)
            self.fd = os.open(target.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        finally:
            os.close(parent)
        self.handles = []

    def create(self, name):
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=self.fd)
        handle = os.fdopen(fd, 'w', encoding='utf-8', newline='')
        self.handles.append(handle)
        return handle

    def json(self, name, value):
        handle = self.create(name)
        json.dump(value, handle, sort_keys=True, indent=2, allow_nan=False)
        handle.write('\n')

    def sync(self):
        for handle in self.handles:
            handle.flush()
            os.fsync(handle.fileno())
        os.fsync(self.fd)

    def publish(self, summary):
        self.json('summary.json', summary)
        self.sync()
        artifacts = {}
        for name in ('validated.csv', 'rejected.csv', 'summary.json'):
            digest = hashlib.sha256()
            size = 0
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self.fd)
            with os.fdopen(fd, 'rb') as source:
                while chunk := source.read(65536):
                    size += len(chunk)
                    digest.update(chunk)
            artifacts[name] = {'sha256': digest.hexdigest(), 'size_bytes': size}
        self.json('.commit-pending', {'format_version': 1, 'complete': True, 'artifacts': artifacts})
        self.sync()
        # Finish all data/marker file closes before exposing completion.
        for handle in self.handles:
            handle.close()
        self.handles.clear()
        try:
            self.publication.rename(self.fd)
            self.publication.sync(self.fd)
        except BaseException:
            # Revoke a marker if directory durability fails after publication.
            try:
                self.publication.revoke(self.fd)
            except FileNotFoundError:
                pass
            raise

    def close(self):
        try:
            for handle in self.handles:
                handle.close()
        finally:
            os.close(self.fd)
