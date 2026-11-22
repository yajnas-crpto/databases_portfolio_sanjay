# Reflection 4 in Module 4

### Key Take-Away & Advice

- **Key Take-Away:** I learned that edge databases must enforce their own data rules instead of relying only on application code. I want to remember the three layers of integrity: Entity, Referential, and Semantic.
- **Advice:** Do not rely only on application code to prevent bad data. Use database features such as `CHECK` constraints, foreign keys, and `STRICT` tables to help keep the data valid.

### What Was Good?

- I enjoyed testing constraints and seeing SQLite reject invalid temperatures and incorrect data types. It helped me understand why database-level validation is important.
- Setting up the Python `UPSERT` script was also interesting because it handled duplicate network packets without creating duplicate records.
- Exploring triggers also helped me understand how a database can automatically react to changes in its data.

### What Was Difficult & Where Did I Struggle?

- I initially struggled to understand access control without a database server. Learning how SQLite uses read-only connections with `mode=ro` and file permissions instead of traditional database user roles was new to me.
- I also learned that foreign-key enforcement needs to be enabled for each connection. This caused some confusion when testing the tasks in a new terminal session.

### Interesting Exploration

- Exploring `BEFORE` and `AFTER` triggers was interesting. I learned that an `AFTER` trigger is useful for alarms because it only logs an alarm after the sensor reading has been successfully saved.
- Testing the different integrity rules also showed me how important it is to check invalid data rather than only testing whether valid data can be inserted.

### Peer Interaction & Teamwork

- During the initial Pod Study tasks (Tasks A and B), we worked together to test the unconstrained table and understand the three layers of integrity.
- We also worked with Htet on some of the Module 4 tasks, although he had not officially joined our pod at that point.
- I helped Sebastian debug an issue with `PRAGMA foreign_keys`. It had been reset to `OFF` in a new terminal connection, so we enabled it again, removed an incorrectly inserted row, and reran the test.
- After discussing the concepts and testing together, we continued with our individual edge database tasks.

### Help & Extra Work

- **Help received:** Working through the tasks with my teammates helped me understand the integrity rules and debug issues, especially when testing foreign-key enforcement.
- **Help given:** I helped Sebastian identify and fix the foreign-key setting issue in his new connection.
- **Contributions:** I completed the individual edge database tasks, tested constraints and triggers, and worked through the Python `UPSERT` and read-only access examples.