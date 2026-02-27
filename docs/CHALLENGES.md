# Development Challenges Log

## Phase 1: Planning and Setup

### Challenge 1: npm Audit Vulnerabilities (Server)

**Problem:**
<br>
After installing dev dependencies (`Jest`, `supertest`, `nodemon`, `eslint`) in the server package, `npm audit` reported **18 high-vulnerabilities**. Attempting to use `npm audit fix --force` will downgrade the Jest version to v19 (2017), breaking the test entirely.

**Root-cause:**
<br>
The vulnerabilities comes from sub-dependencies within the `Jest` and `Eslint` toolchains, not from the packages installed directly. These deeply nested packages (`minimatch`, `glob`, `braces`, `form-data`) had known security issues that their parent packages had not updated yet.

**Resoulution:**
<br>
Ran `npm audit --omit=dev` which return 0 vulnerability, confirmed the issues were confined to development tooling only and would not affect in production. Proceed without forcing breaking upgrades, ensure production deployment steps use `npm ci --omit=dev`. (clean install, avoid unnecessary tooling).

**Lesson Learned:**
<br>
Always separate between production and development dependency issues. Not evey `npm audit` findings require immediate action. Important is to understand the actual risk and write down the decisions so it's clear in the future.

### Challenge 2: create-react-app (CRA) Vulnerabilities (Client)

**Problem:**
<br>
Initial client setup used `create-react-app`, which reported 55 vulnerabilities (53 high, 2 moderate). This is cause by `react-scripts`, an unmaintained package pulling dozens of outdated dependencies.

**Root Cause:**
<br>
Due to lack of active maintainers, Create React App had officially deprecated on 14 Feb 2025. This result with outdated dependencies and unresolved vulnerabilities, which many are unable to solve automatically using `npm audit fix`.

**Resolution:**
<br>
React team encouraged developer to migrate away from CRA to new framework. Replace with **vite** (`npm create vite@latest client -- --template react ts`), which is actively maintained and fast. Remaining vulnerabilities (10 high, all in ESlint toolchain) were confirmed as dev only via `npm audit --omit=dev`, which return 0.

**Lesson Learned:**
<br>
Selection of tools is crucial to development work. Using modern, actively maintained tools can prevent years of unmaintained dependency debt. **Vite** is currently the industry standard for new React projects, with it speed, active maintenance, and widely adoption.

## Challenge 3: Docker Compose YAML Validation Error

**Problem:**
<br>
Running `docker compose up` produce the error: "additional properties 'image', 'pipeline', 'restart', 'depends_on', 'healthcheck', 'ports', 'redis', 'Services', 'container_name', 'environment' not allowed."

**Root Cause:**
<br>
YAML indentation and case-sensitive error in `docker-compose.yml`. Properties like `image`, `ports`, and `environment` were placed at the wrong indentation level (top-level instead of under `services:`). YAML is whitespace-sensitive — incorrect indentation changes the meaning of the file entirely, "Services:" instead of "services:" would cause a error too.

**Resolution:**
<br>
Recreated the `docker-compose.yml` with correct indentation, and adhere to the lowercase type, ensuring all service-level properties were nested under their respective service names within the `services:` block. Used `docker compose config` to validate the file before running `docker compose up`.

**Lesson Learned:**
<br>
YAML is strict about indentation and case-sensitive. Always validate with `docker compose config` before starting containers. Use a consistent 2-space indentation and a YAML-aware editor (VS Code with YAML extension).

## Challenge 4: PostgreSQL 18+ Data Directory Format Error

**Problem:**
<br>
The Postgres container failed to start with the error: "in 18+, these Docker images are configured to store database data in a format which is compatible with pg_ctlcluster... there appears to be PostgreSQL data in /var/lib/postgresql/data (unused mount/volume)."

**Root Cause:**
<br>
The `docker-compose.yml` used `postgres:latest` instead of a pinned version. `latest` resolved to PostgreSQL 18+, which changed the internal data directory layout. The existing Docker volume (from a previous run with an older version) was incompatible with this new layout.

**Resolution:**
<br>

1. Pinned the Postgres image to `postgres:15-alpine` to avoid unexpected version changes. (`postgres:15-alpine`: 15-version, alpine-built on Alpine Linux, a minimal Linux distribution)
2. Removed the stale volume with `docker compose down -v`.
3. Restarted with a fresh volume: `docker compose up -d`.

**Lesson Learned:**
<br>
Never use `:latest` for database images in development or production. Always pin to a specific major version (e.g., `postgres:15-alpine`). Docker volumes persist data across container rebuilds — when changing database versions, you must reset the volume or perform a proper upgrade.

## Challenge 5: Port Conflict - Local vs Docker PostgreSQL

**Problem:**
<br>
Express server reported `database "sg_cost_living" does not exist` even though the Docker PostgreSQL container was healthy and the database was confirmed to exist inside Docker.

**Root Cause:**
<br>
A locally installed PostgreSQL (Windows Service) was already running on port 5432. When Express connected to `localhost:5432`, the operating system routed the connection to the **local** PostgreSQL (which did not have `sg_cost_living`) instead of the **Docker** PostgreSQL (which did).

**Resolution:**
<br>
Stopped the local PostgreSQL Windows Service via Services (`services.msc`). With the local instance stopped, `localhost:5432` correctly routed to the Docker PostgreSQL container.

**Lesson Learned:**
<br>
When Docker used a port that already occupied by a local service, the local service will override it. Always check for port conflicts when Docker services can't be reached. Use `netstat -ano | findstr :5432` on Windows to identify which process owns a port. Consider changing the Docker host port (e.g., `5433:5432`) or disabling the local service.

<br>

# Phase 2: Data Pipeline - Extract and Load Raw Data

## Challenge 1: Pipeline Extraction Hitting Rate Limits

**Problem:**
<br>
First pipeline run fetched only 10,000 HDB records before receiving a status code of 429 error (too many requests). The pipeline had no retry logic, so it immediately stopped extraction.

**Root Cause:**
<br>
The `api_client.py` had no delay between requests and no retry mechanism. It keep sending requests which triggered the API's rate limiter after first or second request.

**Resolution:**
<br>
Added three mechanism to `api_client.py`:

1. **Delay_between_requests** (`delay_between_requests = 5`) to stay under rate limit.
2. **Automatic retry with exponential backoff**: when 429 is received, wait progressively (10s -> 20s -> 40s -> 80s -> 160s) before retrying.
3. **Maximum retry limit** (Set to 5 retries) to prevent infinite loops.

**Lesson Learned:**
<br>
Any production ETL pipeline that calls for external APIs must have rate limit handling. Exponential backoff is an industry standard pattern for waiting longer after each failure, giving server time to recover.

## Challenge 2: Rate Limiting Persisting Despite Retry Logic (Second Attempt)

**Problem:**
<br>
Even with the retry logic in place, and a 10 second delay between requests, the HDB extraction still hit max retries (5/5) at around 65,000 records of 225,902.

**Root Cause:**
<br>
The request batch size set limit to 10,000 was too large (`limit = 10000`).The API slow down large requests more heavily and with many requests back-to-back, the rate limiter still kicked in even though added delays.

**Resolution:**
<br>
Reduced the batch size from 10000 to 5000 records per request (`limit = 5000`). This spread the load across more evenly with smaller requests. This result the total number of request went up, but each of the request was less likely to hit rate limit.

**Lesson Learned:**
<br>
When dealing with rate limited APIs, reducing the request size can be as effective as adding delays. And for MVP, sometimes partial data (like 65k out of 225k records) is good enough, rather than spending hours fighting rate limit to get everything. The full dataset can be fetched later during off-peak periods or overnight.

## Challenge 3: Unexpected CPI Data Structure (Wide Format)

**Problem:**
<br>
CPI data from data.gov.sg was structured differently from HDB and COE datasets. Instead of one row per data point (long format), it returned one row per category with hundreds of columns, one for each month acreoss all years (wide format).
<br>

```
{
  "DataSeries": "All Items",
  "1961Jan": "21.071",
  "1961Feb": "21.094",
  ...
  "2024Dec": "100.661"
}
```

**Root Cause:**
<br>
The CPI dataset was published in a pivoted/wide format where year-month is represented by columns.

**Resolution:**
<br>
Stored the CPI data as-is in the raw_data.cpi_data table (JSONB). Use Pandas `melt()` function to unpivot the wide format into long format needed for the cleaned_data.cpi_data table.
<br>

```
Wide:  DataSeries=All Items, 2024Jan=98.752, 2024Feb=99.755
Long:  month=2024-01, category=All Items, cpi_value=98.752
       month=2024-02, category=All Items, cpi_value=99.755
```

**Lesson Learned:**
<br>
Always explore the actual dataset structure before planning for transformation.
