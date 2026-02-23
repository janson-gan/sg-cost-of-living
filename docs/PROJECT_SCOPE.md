# SG Real-Time Cost of Living Tracker

## Problem Statement

Singaporean lack a centralised, data-driven platform to track and compare cost of living trends across key categories (housing, transportation, food, utilities).

## Why This Matters

- HDB resale prices hit record highs in recent years.
- COE premiumns have been volatile.
- Residents need transparent, accessible data to make informed decisions.
- Government provides raw data, but no user-friendly combined dashboard exists.

## Target Users

- Singaporean residents tracking affordability.

## Core Features (MVP)

### Must Have

- [ ] Dashboard with KPI cards (average HDB price, COE price, CPI index).
- [ ] HDB resale price trends (line chart by town).
- [ ] COE price trends (line chart by category).
- [ ] Interactive map showing HDB prices by town.
- [ ] Filter by date range, town, flat type.
- [ ] Daily automated data pipeline.

### Nice to Have (only if time permits)

- [ ] Hawker food price tracker
- [ ] Cost comparison calculator
- [ ] Email alerts for price changes
- [ ] Dark mode

## Data Sources

| Souce       | URL         | Update Frequency |
| ----------- | ----------- | ---------------- |
| HDB Resale  | data.gov,sg | Quarterly        |
| COE Results | data.gov.sg | Twice monthly    |
| CDI Data    | data.gov.sg | Monthly          |

## Tech Stack

- Frontend: React.js, Tailwind CSS, Recharts, Leaflet
- Backend: Node.js, Express.js, Redis
- Pipeline: Python, pandas, psycopg2, schedule
- Database: PostgreSQL
- DevOps: Docker, GitHub Actions, AWS/GCP
- Testing: Jest, Supertest, React Testing Library, pytest

## Abbreviation

- KPI: Key Performance Indicator
- HDB: Housing & Development Board
- COE: Certificate of Entitlement
- CDI: Consumer Price Index

## Attribute

[data.gov.sg](https://www.data.gov.sg)
