erDiagram
    MACHINE ||--o{ MAINTENANCE_JOB : "undergoes"
    TECHNICIAN ||--o{ MAINTENANCE_JOB : "performs"
    MAINTENANCE_JOB }o--o{ PART : "uses"

    MACHINE {
        string machine_name PK
        string serial_no
        string site
        string installed
    }
    PART {
        string part_no PK
        string description
        string unit_price
    }
    MAINTENANCE_JOB {
        int job_id PK
        string machine_name FK
        string technician FK
        string done_on
        string parts_used
    }
    TECHNICIAN {
        string name PK
    }