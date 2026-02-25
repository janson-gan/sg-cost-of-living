# Tech Stack Used for this Project

## React JS

- Frontend web application

## Library Used for this Project

## Express JS

- Web framework for building APIs.

## PG

- PostgreSQL client for Node js.
- Run queries from JavaScript

## Redis

- Redis client for caching
- Store frequent requested data in memory

## Cors

- Cross-Origin Resources Sharing middleware.
- Used to allow different localhost talk to each other as browser security blocks requests from different localhost (Different port).

## Helmet

- Security headers middleware
- Automatically sets HTTP headers that prevent common attack from X-content-Type-Options (prevent MIME sniffing) and X-Frame-Options (prevent clickjacking).
- One line of code, significant security improvement.

## Morgan

- HTTP request logger middleware.
- Logs every request to console.

## Dotenv

- Secure sensitive information like password
- Prevent hardcoding

## Express-rate-limit

- Limits request per IP address.
- Prevent server abuse: e.g., max 100 requests per 15 minutes.

## Jsonwebtoken

- Create and verifieds JWT tokens
- Used for authentication on protected endpoints.

## Docker

- A virtualization software.
- A container that store application and everything it needs to run. For example, source code, libraries, dependencies, settings, etc.
- Container that contain application can works in any machine, apps run the same eveywhere.
- Is isolated in each container, so app does not mess up with another.