# Reflection 4 in Module 4

### Key Take-Away & Advice
- **Key Take-Away:** I learned that edge databases must enforce their own data rules. I want to remember the three layers of integrity: Entity, Referential, and Semantic.
- **Advice:** Don't rely only on application code to prevent bad data. Use database features such as `CHECK` constraints and `STRICT` tables.

### What Was Good?
- I enjoyed testing constraints and seeing SQLite reject invalid temperatures and incorrect data types.
- Setting up the Python `UPSERT` script was also interesting because it handled duplicate network packets without creating duplicate records.

### What Was Difficult & Where Did I Struggle?
- I initially struggled to understand access control without a database server. Learning how SQLite uses read-only connections (`mode=ro`) and file permissions instead of traditional user roles was new to me.

### Interesting Exploration
- Exploring `BEFORE` and `AFTER` triggers was interesting. I learned that an `AFTER` trigger is useful for alarms because it only logs an alarm after the sensor reading has been successfully saved.

### Peer Interaction & Teamwork
- During the initial Pod Study (Tasks A and B), we worked together to test the unconstrained table and understand the three layers of integrity.
- After discussing the concepts as a group, we moved on to completing our individual edge database tasks.