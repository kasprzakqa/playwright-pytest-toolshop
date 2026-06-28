# Test Strategy - Toolshop Automation

End-to-end test automation framework for the **Practice Software Testing ("Toolshop")**
application, covering the UI, the REST API, and accessibility. The framework is built in
Python with Playwright and pytest, and runs continuously in GitHub Actions.

---

## 1. Purpose & scope

**Goal:** provide fast, reliable, maintainable automated coverage of the business-critical paths
of an e-commerce application, and gate releases on their health.

**In scope**

- UI end-to-end journeys: authentication, product catalog & search, cart, checkout
- REST API: products, categories/brands, authentication, cart
- Accessibility: WCAG 2.1 AA on key pages (automated axe scan + keyboard/focus checks)
- Cross-browser capable: Chromium by default; Firefox / WebKit via the planned containerized matrix

**Out of scope**

- Performance/load testing (public demo environment - not to be stressed)
- Security/penetration testing
- Payment-provider integration beyond the application's own checkout flow

---

## 2. System under test

| Layer | Endpoint | Notes |
|-------|----------|-------|
| UI    | `https://practicesoftwaretesting.com`       | Angular single-page application |
| API   | `https://api.practicesoftwaretesting.com`   | REST (Laravel), OpenAPI/Swagger documented |

The application is a public, read-mostly demo. Tests respect it as a shared environment: no load
generation, each test uses unique generated data to stay isolated, and the smoke suite is
deliberately small.

---

## 3. Risk-based prioritization

Coverage follows business risk, not uniform breadth. Each path is scored on **impact** (revenue /
trust) x **likelihood** (change frequency / complexity):

| Area | Risk | Priority | Suite |
|------|------|----------|-------|
| Login / session | High | P1 | smoke |
| Product search & catalog | High | P1 | smoke + regression |
| Add to cart / cart totals | High | P1 | smoke + regression |
| Checkout flow | High | P1 | smoke + regression |
| Product detail, filters, pagination | Medium | P2 | regression |
| Accessibility of key pages | Medium | P2 | a11y |
| Static/content pages | Low | P3 | sanity |

P1 paths form the **smoke suite** - the build-alive gate that must pass before a deploy is allowed.

---

## 4. Test levels & types

- **API tests** - fast, stable foundation of the pyramid. Validate status, headers, body schema
  (typed models) and negative paths (401/422/404). Run first.
- **UI E2E tests** - user journeys through the SPA, organized by feature, built on the Page Object
  Model. Reserved for behavior that genuinely needs the browser.
- **Accessibility tests** - automated axe-core scan (gated on serious/critical) plus manual
  keyboard-operability and focus-management checks.

Distribution follows the test pyramid: more API than UI, UI focused on journeys that can't be
proven at the API layer.

---

## 5. Test approach

- **Page Object Model** - locators and page interactions live in page classes; tests read as
  business scenarios.
- **Locator strategy** - role-based locators first (`get_by_role`), resilient to markup churn;
  CSS/XPath only as a documented last resort.
- **Deterministic waiting** - Playwright web-first assertions (`expect`) and auto-waiting only;
  no fixed sleeps.
- **Isolation** - every test is standalone and order-independent; authentication is injected via
  stored session state rather than re-driven through the UI in each test.
- **One behavior per test**, named for the expected outcome
  (`test_login_with_invalid_credentials_shows_error`).

---

## 6. Test data

- Generated with **Faker** through factories/builders - realistic but never real PII.
- Each test creates the unique data it needs (e.g. a freshly registered account), so runs stay
  isolated without depending on shared accounts or teardown - the shared demo exposes no delete
  path, so isolation is achieved by uniqueness, not cleanup.
- Credentials and secrets come from environment variables / CI secrets, never the codebase.

---

## 7. Environments & configuration

- Base URLs and credentials are resolved from environment variables (`.env` locally via
  `python-dotenv`, GitHub Secrets in CI) - never hardcoded.
- The same suite runs locally and in CI; CI enables a single controlled retry on the otherwise
  zero-retry policy to absorb transient blips against the shared demo.
- **Planned hardening:** run the application from its container image in CI for a fully hermetic,
  deterministic environment, removing the dependency on the public demo's uptime.

---

## 8. Entry & exit criteria

**Entry (a feature is ready to automate):** acceptance criteria known, scenarios listed in the
test plan (happy / boundary / negative), environment reachable.

**Exit (a release may ship):**
- CI gate green (lint + API suite); UI smoke paths green locally on Chromium
- No open P1 defects on covered paths
- No tests skipped without a linked, justified ticket
- Accessibility: zero serious/critical violations on key pages

---

## 9. CI/CD quality gates

GitHub's hosted runners cannot reliably reach the public Toolshop SPA (the demo throttles datacenter
IPs), so the hosted pipeline gates what is reachable there - lint and the API suite - while the UI
e2e and accessibility suites run locally and via a clean-clone check.

Pipeline (ordered cheap-to-expensive for fast feedback, GitHub Actions):

1. **Lint** - `ruff` + `black --check`
2. **API suite (deploy gate)** - `pytest tests/api -n auto`, one controlled retry, HTML report artifact
3. **Nightly** - scheduled API regression health-check

**Planned hardening:** run the application from a container in CI so the full suite (UI + a11y, plus
a cross-browser matrix) runs hermetically against localhost, removing the public-demo dependency.

---

## 10. Reporting

- **`pytest-html`** is the current report: a self-contained HTML artifact with per-test results,
  uploaded from every CI run and carrying the traces/screenshots captured on failure.
- A richer **Allure** report (severities, history, trends) published to GitHub Pages is planned as
  a follow-up, once the suite has a stable green baseline - it is not shipped half-wired.

---

## 11. Flaky-test policy

A test is proven flaky by repeated runs, not a single failure. Flaky tests are **quarantined**
(moved to a non-blocking job and tagged), never deleted, and fixed at the root cause within a
fixed window. Reruns are damage control, never a substitute for a fix.

---

## 12. Tooling

| Concern | Tool |
|---------|------|
| Language / runner | Python 3.11+, pytest |
| Browser automation | Playwright (sync) |
| Parallelism | pytest-xdist |
| API models | pydantic |
| Test data | Faker |
| Accessibility | axe-core (axe-playwright-python) |
| Reporting | pytest-html (Allure planned) |
| Quality | ruff, black, pre-commit |
| CI/CD | GitHub Actions |

---

## 13. Maintenance

- Pre-commit hooks keep formatting and linting consistent before code lands.
- Page objects localize change: a UI markup change touches one class, not every test.
- The test plan (`docs/test-plan.md`) is kept in step with coverage as features evolve.
