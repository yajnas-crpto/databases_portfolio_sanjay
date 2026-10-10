# Task 10: Datasette Facets, Filters, and JSON API

### 1. URLs Used
- **Filtered Table View:** `http://127.0.0.1:8001/telemetry/readings?machine__exact=cnc-01`
- **Faceted View:** `http://127.0.0.1:8001/telemetry/readings?_facet=vib_rms&_facet=machine`
- **JSON API View:** `http://127.0.0.1:8001/telemetry/readings.json?_size=5`

### 2. Overview
Datasette automatically maps URL query parameters to SQL clauses, allowing seamless transitions between HTML web views and structured JSON API responses without requiring custom web server code.