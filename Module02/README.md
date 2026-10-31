# Module 2 — Data Contracts & Reading Legacy Schemas (ERD Audits)

This module covers the *Conceptual Database Design* and *requirements analysis* phases by auditing an undocumented, flawed schema, reconstructing its intended ER model, and formalizing it into a code-first data contract.

## 🎯 Learning Goals
1. Reconstruct an **[ER/EER model](./mermaid-lab.md)** (entities, attributes, keys, relationships, cardinalities) from an undocumented SQL schema.
2. Identify **[integrity defects](./er-audit.md)** — missing foreign keys, orphan rows, redundant data, normalization violations — with queries, not intuition.
3. Distinguish an **[entity relationship](./study-log.md)** from an attribute, and a **surrogate key** from a natural key, and justify the choice.
4. Express a schema as a **[code-first data contract](./contract.py)** (Pydantic / SQLAlchemy) that an application can enforce.
5. Write the **[requirements the schema forgot](./er-audit.md)**: the business rules nobody encoded.


## 📝 Task Execution & Evidence

*Note: I executed the core tasks for this module independently, but synced asynchronously with my Task Pod to compare findings and establish our agreed learnings.*

### Pod Study & Conceptual Modeling (Tasks A, B, C)
My research on ER models, natural vs. surrogate keys, my four drawn cardinality examples, and the agreed learning bullet points from my pod sync are documented in my study log.
* **Evidence:** [study-log.md](./study-log.md)

### Legacy Schema Audit & Integrity Defects (Tasks 1 & 2)
I reconstructed the intended ER diagram from the flawed `legacy.db` schema using Mermaid, proved the true cardinalities using SQL `COUNT` queries, and identified 5 critical data integrity defects (with their production impacts).
* **Evidence:** [er-audit.md](./er-audit.md)
* **Database Setup:** [setup.sql](./setup.sql)

### Code-First Data Contract (Task 3)
I repaired the schema and expressed the corrected constraints using Pydantic (for application-level validation) and SQLAlchemy (for database-level structural enforcement), outputting the corrected DDL.
* **Evidence:** [contract.py](./contract.py) (and the emitted DDL in `er-audit.md`)

### Stretcher Tasks (Tasks 4 & 5)
I completed the Model Inheritance stretcher (evaluating single-table vs. joined-table inheritance) and adapted my found ER diagrams into fully functioning Mermaid code blocks.
* **Evidence:** Documented inside [er-audit.md](./er-audit.md) and [study-log.md](./study-log.md).

## 🧠 Reflection
* **Module 2 Logbook Entry:** [Reflection 2](../Reflections/ref02.md)