# Module 5: Functional Dependencies & Anomalies

## Round 1: Functional Dependencies & ER Diagrams

### 1. Functional Dependencies (FDs)
From the 5-row sample relation `(job_id, machine_id, site, technician, part_no, part_price)`:

* **`job_id -> machine_id`** *(Domain Fact)*: A specific job takes place on exactly one physical machine.
* **`job_id -> technician`** *(Domain Fact)*: A job is assigned to one primary technician.
* **`job_id -> done_on`** *(Domain Fact)*: A job is completed on a single date.
* **`machine_id -> site`** *(Domain Fact)*: A physical machine is located at exactly one plant/site.
* **`part_no -> part_price`** *(Domain Fact)*: A part has a fixed unit price.
* **`(job_id, part_no)` -> ALL** *(Candidate Key)*: The minimal composite key uniquely identifying a job-part line item.

*Observed vs. Domain Fact:* The sample shows `technician -> site` (tech-0 only at Gütersloh), but this is merely **observed** in these 5 rows. A technician can be reassigned to Bielefeld, making it a non-dependency in the true domain.

### 2. ER Diagram Transformation
* **Unnormalized (Flat):** Single entity `flat_jobpart` with attributes `(job_id, machine_id, site, technician, part_no, part_price)`. Contains transitive dependency `job_id -> machine_id -> site` and partial dependency `part_no -> part_price`.
* **Normalized (3NF):** Four entities:
  - `machine(machine_id PK, site)`
  - `part(part_no PK, part_price)`
  - `job(job_id PK, machine_id FK, technician, done_on)`
  - `job_part(job_id FK, part_no FK, PK(job_id, part_no))`
* **Disappearing Arrow:** The direct transitive dependency arrow `job -> site` disappears in the 3NF diagram, replaced by traversing `job -> machine -> site`.

---

## Round 2: Causing Database Anomalies

```sql
CREATE TABLE flat5(
  job_id INTEGER, machine_id TEXT, site TEXT,
  technician TEXT, part_no TEXT, part_price REAL
);

INSERT INTO flat5 VALUES
  (1,'cnc-01','Gütersloh','tech-0','P-0001',6.00),
  (1,'cnc-01','Gütersloh','tech-0','P-0002',7.00),
  (2,'cnc-02','Gütersloh','tech-1','P-0001',6.00),
  (2,'cnc-02','Gütersloh','tech-1','P-0003',8.50),
  (3,'cnc-01','Gütersloh','tech-0','P-0003',8.50);