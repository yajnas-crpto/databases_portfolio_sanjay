# Reflection 5 in Module 5

### Key Take-Away & Advice

- **Key Take-Away:** I learned why database normalization is important and how 1NF, 2NF, and 3NF help reduce duplicate data and prevent update, insert, and delete anomalies. I also learned that denormalization can improve read performance, but it can create extra costs for updates and storage.
- **Advice:** Understand why tables are split during normalization instead of just memorising the different normal forms. It is also important to consider how a database will actually be used before deciding whether to normalize or denormalize it.

### What Was Good?

- I found creating `normalize.db` and generating approximately 200,000 rows in a flat table interesting. It was useful to work with a larger dataset and see how the information could be organised into smaller related tables.
- Comparing normalized and denormalized designs helped me understand that database design involves trade-offs rather than one solution that is always best.

### What Was Difficult & Where Did I Struggle?

- Understanding functional dependencies and deciding which attributes belong in separate tables required some thought.
- Comparing the two designs was also challenging because performance depends on the type of queries and operations being performed. This helped me understand why the best design can differ depending on the workload.

### Peer Interaction & Teamwork

- Our team decided to work remotely together during the lecture and informed the professor about our arrangement. We worked through Module 5 together and shared our understanding whenever someone needed help.
- Htet officially joined our pod during Module 5, after having worked with us on some tasks in Module 4. We welcomed him and helped him become familiar with the work we had already completed.
- Isa also joined our group later in Module 5. Having both of them involved gave us more opportunities to share knowledge and discuss different approaches. Our pod grew to six members.

### Help & Extra Work

- **Help received:** Discussing the normalization and denormalization tasks with the group helped me understand the different design choices and their trade-offs.
- **Help given:** We supported the new members as they joined the pod and helped each other understand the module tasks.
- **Contributions:** I worked on creating the flat dataset, organizing the data into related tables, and comparing the normalized and denormalized approaches.