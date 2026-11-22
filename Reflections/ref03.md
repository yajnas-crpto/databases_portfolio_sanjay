# Reflection 3 in Module 3

### Key Take-Away & Advice

- **Key Take-Away:** I learned that AI-generated code can create a false sense of understanding. The important part is being able to test, verify, and explain the code yourself. I also learned how `EXPLAIN QUERY PLAN` helps us understand how SQLite executes queries and where performance improvements might be possible.
- **Advice:** Use AI as a tutor rather than an autopilot. Make sure you understand the query and its logic before submitting your work.

### What Was Good?

- I enjoyed working with the 240,000-row `warehouse.db` database and seeing how query plans changed during testing.
- Benchmarking indexes was interesting because I discovered that adding an index does not always improve performance. Sometimes SQLite can use the primary key or another approach more efficiently.
- I also reorganised my repository into separate evidence files, which made my portfolio easier to follow.

### What Was Difficult & Where Did I Struggle?

- My biggest difficulty was realising that I sometimes relied too much on AI and could not confidently explain all the generated database logic from scratch.
- There were no major technical blockers, but this module showed me that I need to spend more time understanding and verifying the queries instead of only focusing on getting them to work.

### Peer Interaction & Teamwork

- Our pod worked well by sharing different parts of the work and explaining our findings to each other. Isa temporarily joined our pod for the Module 3 group task because his own pod partner was unavailable. He helped us understand relational algebra and how it connects to SQL.
- Sebastian explained the difference between the written order of SQL clauses and the order in which they are evaluated. Myo also helped with query tuning and security.
- I contributed by explaining `SCAN`, `SEARCH`, and `COVERING` from `EXPLAIN QUERY PLAN`. We also documented our findings in `sql-notes.md` so Jomarie could catch up after being absent.

### Help & Extra Work

- **Help received:** Isa, Sebastian, and Myo shared useful explanations with the group, which helped me understand different parts of the module.
- **Help given:** I explained query plan terminology to my teammates and shared what I learned from testing the queries.
- **Extra contributions:** I organised my repository into evidence files such as `task1-profiling.md` and `bench.py`, and helped document our group findings.