# Toolshop Automation - Playwright + pytest

[![CI](https://github.com/kasprzakqa/playwright-pytest-toolshop/actions/workflows/ci.yml/badge.svg)](https://github.com/kasprzakqa/playwright-pytest-toolshop/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)

End-to-end test automation framework for the [Practice Software Testing](https://practicesoftwaretesting.com)
("Toolshop") application - UI journeys, REST API, and accessibility - built with Python,
Playwright (sync) and pytest, with the API layer gated continuously in GitHub Actions.

## What it covers

| Layer | Coverage |
|-------|----------|
| **API** | Products & catalog (schema-validated), pagination, 404, authentication (token + 401) |
| **UI E2E** | Login (valid / invalid), catalog search, full checkout (cart -> billing -> payment -> confirmation) |
| **Accessibility** | axe-core scan gated on serious/critical, keyboard operability |

## Design highlights

- **Page Object Model** - locators live in page classes; tests read as scenarios.
- **Role-first locators** - `get_by_role` / `get_by_placeholder` / `get_by_test_id`; no brittle CSS.
- **Deterministic waiting** - Playwright web-first assertions only; zero `time.sleep`.
- **Isolation** - authentication injected via `storage_state`, not re-driven per test.
- **Typed API contracts** - `pydantic` models make a renamed/missing field fail loudly.
- **Suite markers** - `smoke` (deploy gate) / `regression` / `sanity`, plus `api` / `a11y`.
- **Parallel** - `pytest-xdist` (`-n auto`).

## Project layout

```
pages/        Page Object Model (base, login, home, product, checkout)
tests/
  conftest.py shared fixtures (API context, storage_state auth)
  api/        API tests (pydantic-validated)
  e2e/        UI journeys: auth, catalog, checkout
  a11y/       axe scan + keyboard
data/         pydantic models + Faker factories
utils/        config + API clients
docs/         test strategy & test plan
```

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

pytest -n auto                 # full suite, parallel
pytest -m smoke                # critical-path gate
pytest --headed tests/e2e      # watch the browser
```

Configuration is environment-driven (`.env`, see `.env.example`) so the same suite runs against
the public demo or a local instance.

## CI

GitHub Actions runs **lint + the API suite** on every push and PR (one controlled retry, HTML report
artifact), plus a nightly API regression. The UI e2e and accessibility suites are not on hosted CI:
GitHub runners cannot reliably reach the public Toolshop SPA (the demo throttles datacenter IPs), so
they run locally and via a clean-clone check, with a containerized CI job as the documented next step
(see the [test strategy](docs/test-strategy.md)). The same suite passes for anyone who clones and runs it.

## Documentation

- [Test strategy](docs/test-strategy.md)
- [Test plan](docs/test-plan.md)
