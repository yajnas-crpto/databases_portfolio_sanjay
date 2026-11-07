### Task B

## Task B: sharing with another pod

**Most surprising thing an unconstrained table accepted (our pod):**
The word 'hot' went into a REAL column with no error, and typeof() showed it
was stored as text. SQLite only *tries* to convert values to the declared type:
'7' becomes the integer 7, but 'abc' is kept as text. The declared type is a hint,
not a rule.

**Hardest constraint to get right:** CHECK with NULL.
[Replace this if your pod found a different one hardest.]
A column with CHECK (value BETWEEN -273.15 AND 5000) still accepts NULL, because
the check only rejects rows where the condition is false, and a comparison with
NULL is "unknown". The fix is to add NOT NULL.
Runners-up: UNIQUE (sensor_id, metric) accepted two rows with sensor_id NULL,
because NULLs count as distinct; and STRICT accepted the text '1.0' in an INTEGER
column by converting it, while rejecting 1.5.

**What the other pod reported:**

**Agreed points:**
- STRICT, NOT NULL, CHECK and UNIQUE each catch a different kind of bad row, so
  none replaces another.
- A CHECK on a nullable column does not stop NULL; pair it with NOT NULL.
- UNIQUE does not treat NULLs as duplicates.
- A range check blocks the impossible, not the implausible: 4999 °C still passes.

**Unresolved:**
- Should plausible ranges be set per metric, with a CHECK using CASE or a trigger?
- Is it acceptable that STRICT converts '1.0' to 1 for an INTEGER column?