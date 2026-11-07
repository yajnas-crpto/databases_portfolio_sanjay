# Reflection 4 (Module 4)

**What is your take-away, what do you want to remember, what would be your advice?**
My main takeaway is that edge databases must enforce their own rules because there is no server to validate the data. I want to remember the three layers of integrity (Entity, Referential, Semantic) we mapped out in our pod study. My advice to myself is to never rely on application code to filter bad data; always use `CHECK` constraints and `STRICT` tables directly in SQLite.

**What was good?**
Testing the constraints in Task 1 was very satisfying. Seeing the database actively reject impossible temperatures and incorrect data types proved that the physical rules were working. Setting up the `UPSERT` Python script to handle duplicate network packets without crashing or duplicating rows was also a highlight.

**What was difficult, where did you struggle?**
I struggled initially to understand how access control works without a server. Since SQLite doesn't use `GRANT` or user roles, learning to secure the database using read-only connection strings (`mode=ro`) and file permissions was a new concept to wrap my head around.

**Was there any good/fun “struggling”/exploration?**
Exploring the difference between `BEFORE` and `AFTER` triggers was a fun challenge. I realized that using an `AFTER` trigger for alarms is much safer, because it guarantees the database only logs an alarm if the underlying sensor reading was successfully saved.

**How was your interaction with peers/instructors?**
Our interaction was highly collaborative during the initial Pod Study (Tasks A and B). We worked together as a team to test the unconstrained scratch table and discuss how the different layers of integrity operate. Once we mapped out that theory together, we transitioned to independent work to actually build out our individual edge databases for Tasks 1 to 5.
