# Recommendation Memo: Machine Health Dashboard Schema

**To:** Yasmin Kaya, Operations Lead  
**From:** Sanjay Maheshwari  
**Date:** November 12, 2026  
**Subject:** Local benchmark and reporting-table recommendation

On this 200,000-row SQLite dataset, the denormalized dashboard query had a 98.508 ms median compared with 124.415 ms for the normalized join, and both returned the same 350 groups. The report index did not improve this aggregation in the measured run: its median was 89.405 ms after dropping the index versus 98.508 ms with it, although run-to-run timing varied. The report table and its index allocated 14,077,952 bytes compared with 8,155,136 bytes for the normalized tables and indexes, while a site change affected 4,000 report rows versus one `machine` row. I recommend keeping the transactional source in 3NF and using a separate reporting snapshot only if the dashboard's measured latency justifies its storage and refresh costs. Target a refresh every 30 seconds by starting a SQLite transaction, replacing the reporting rows from `job_part`, `job`, `machine`, and `part`, validating the replacement, and committing only after validation succeeds; readers cannot observe partially replaced rows. If any step fails, roll back so the previous committed snapshot remains; 30 seconds is a target rather than a guaranteed freshness bound, since scheduling delays, build time, or failures can make the snapshot older. Measure refresh and write interference before deployment.
