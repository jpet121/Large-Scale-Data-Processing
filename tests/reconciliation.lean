import Std

/- Small independent reconciliation model. This does not prove Python, CSV,
   filesystem syscalls, gzip, or the monetary ledger correct. The Python
   correspondence test checks all 31 classification sequences of length <= 4. -/
def accepted : List Bool → Nat
  | [] => 0
  | true :: rest => 1 + accepted rest
  | false :: rest => accepted rest

def rejected : List Bool → Nat
  | [] => 0
  | true :: rest => rejected rest
  | false :: rest => 1 + rejected rest

theorem classification_reconciles (rows : List Bool) :
    accepted rows + rejected rows = rows.length := by
  induction rows with
  | nil => simp [accepted, rejected]
  | cons valid rest ih =>
    cases valid <;> simp [accepted, rejected] at * <;> omega

def canCommit (complete writesDurable balanced : Bool) : Bool :=
  complete && writesDurable && balanced

theorem incomplete_never_commits (writesDurable balanced : Bool) :
    canCommit false writesDurable balanced = false := by
  simp [canCommit]

theorem commit_requires_all_checks (complete writesDurable balanced : Bool)
    (h : canCommit complete writesDurable balanced = true) :
    complete = true ∧ writesDurable = true ∧ balanced = true := by
  cases complete <;> cases writesDurable <;> cases balanced <;> simp_all [canCommit]
