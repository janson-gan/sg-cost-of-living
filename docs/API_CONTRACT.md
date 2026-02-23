# API Contract
An API Contract is a agreement between two systems about how they can talk to each other through an API (Application Programme Interface).

- Define what request can be made, for example, available endpoints and methods: GET, POST, etc.
- Specifies what data is expected, for example, parameters, headers, body format.
- Describes what response looks like, for example, status code, JSON structure, error message.
- Both API provider and API consumer rely on this contract, so that they both understand how to interact to each other.

## Why?
- Frontend and backend can be built in parellel if both agree on the contract.
- Know exactly what data is needed, so backend know what queries to built.
- Prevent miscommunication, for example, frontend expect price, but backend send resale_price.

<br>
<br>

# Define API Endpoints
<br>

## Versioning (/api/v1/)
In future, if need to change the api, we can create new api by **/api/v2/**. This does not break the existing frontend code.

## Health Check
```GET /api/v1/health```
- **Purpose**: To verify server, database, and Redis are all working.
- **Used By**: DevOps monitoring, self debugging.
- **Returns**: ```{status: "ok", services: {database: "connected", redis: "connected"}}```

## Dashboard
```GET /api/v1/dashboard/kpis```
- **Purpose**: KPI cards on the homepage.
- **Used By**: Frontend dashboard page.
- **Returns**: ```[
    {kpi_name: "avg_hdb_price", kpi_value: 650000, kpi_pct_change: 2.5},
    {kpi_name: "avg_coe_premium", kpi_value: 9800, kpi_pct_change: -1.5},
]```
- **Database Query**: ```SELECT * FROM analytics.dashboard_kpis```

## HDB Data
```Get /api/v1/hdb/transaction?town=&flat_type=&from=&to=&page=&limit=```
- **Purpose**: List of HDB transactions with filters.
- **Used By**: Frontend data table page.
- **Returns**: ```{data: [...], pagination: {page: 1, totalPages: 100, total: 2000}}```
<br>

*Using **Pagination** to limit data list per page, as 500k+ records unable to send to frontend at once.*
<br>

```GET /api/v1/hdb/trends?town=&flat_type=&from=&to=```
- **Purpose**: Monthly average prices for line charts.
- **Used By**: Frontend trend chart
- **Returns**: ```[{month: "2024-01", avg_price: 590000, transaction_count: 45}, ...]```

<br>

```GET /api/v1/hdb/map-data```
- **Purpose**: Latest average prices per town for the interactive map.
- **Used By**: Frontend map component.
- **Returns**: ```[{town: "Ang MoKio", avg_price: 510000, lat: 1.32, lon: 103.85}, ...]```

<br>

## COE Data
```GET /api/v1/coe/trends?vehicle_class=&from=&to=```
- **Purpose**: COE premium trends chart.
- **Used By**: Frontend COE trends section.
- **Returns**: ```[{month: "2024-01", vehicle_class: "cat A", avg_premium: 93000}, ...]```

<br>

## CPI Data
```GET /api/v1/cpi/trends?category=&from=&to=```
- **Purpose**: CPI trends over time, filterable by category
- **Used By**: Frontend CPI trends chart
- **Returns**: ```[{ month: "2024-01", category: "Food", cpi_value: 112.5, yoy_change_pct: 3.2 }, ...]```

<br>

## Pipeline Staus
```GET /api/v1/pipeline/staus```
- **Purpose**: Monitor last updated data.
- **Used By**: Admin/debugging, display "Last Updated" on frontend.
- **Returns**: ```{last_run: "2024-01-15T02:00:00Z", records_processed: 5000, status: "success"}```





