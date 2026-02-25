# Security Note: NPM Audit Report

## Issue Summary 1

- **Package affected**: 'minimatch' (<10.2.1).
- **Severity**: High.
- **Vulnerability**: Regular Expression Denial of Service (ReDos) via repeated wildcards with non-matching literals in pattern.
- **Reference**: [Github Advisory GHSA-3ppc-4f35-3m26](https://github.com/advisories/GHSA-3ppc-4f35-3m26).

<br>

## Dependency Chain

- `minimatch` is pulled in via 'glob'.
- `glob` is used by Jest and related packages (`jest-config`, `jest-runtime`, `@jest/reporters`, etc.).
- Vulnerability exists in **devDependencies** only testing framework.

<br>

## Audit Results

- Running `npm audit` show **18 high vulnerabilities**.
- Suggested fix: `npm audit fix --force` -> downgrade Jest to `25.0.0` (breaking change).
- Running `npm audit --omit=Dev` showed **0 vulnerabilities**, confirming that production dependencies are not affected.

## Resolution Plan

- Since the vulnerability is confined in the devDependencies, production builds are not affected.
- Action taken:
  - Verified with `npm audit --omit=Dev` returns **0 vulnerabilities**
- Next steps:
  - Monitor Jest releases for updated version that remove the vulnerable `glob/minimatch` chain.
  - Upgrade Jest to the latest stable version once is available.
  - Re-run `npm audit` regularly to confirm no new issues.

<br>

## Issue Summary 2

- **Package affected**: 'minimatch' (<10.2.1).
- **Severity**: High.
- **Vulnerability**: Regular Expression Denial of Service (ReDos) via repeated wildcards with non-matching literals in pattern.
- **Reference**: [Github Advisory GHSA-3ppc-4f35-3m26](https://github.com/advisories/GHSA-3ppc-4f35-3m26).

<br>

## Dependency Chain

- `minimatch` is pulled in via:
  - `@eslint/config-array`
  - `@eslint/eslintrc`
  - `@typescript-eslint/typescript-estree`
- These packages are part of **ESLint** and **TypeScript‑ESLint**, which are used only in development for linting and static analysis.
- The vulnerability therefore exists in **devDependencies** only.

<br>

## Audit Results

- Running `npm audit` showed **10 high severity vulnerabilities**.
- Suggested fix: `npm audit fix --force` → downgrades ESLint to `10.0.1` (breaking change).
- Running `npm audit --omit=dev` showed **0 vulnerabilities**, confirming that production dependencies are not affected.

<br>

## Resolution Plan

- Since the vulnerability is confined in the devDependencies, production builds are not affected.
- Action taken:
  - Verified with `npm audit --omit=Dev` returns **0 vulnerabilities**
- Next steps:
  - Upgrade ESLint and TypeScript‑ESLint to the latest stable versions once they release patched builds.
  - Re-run `npm audit` regularly to confirm no new issues.
