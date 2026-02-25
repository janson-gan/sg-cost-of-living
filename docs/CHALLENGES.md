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
