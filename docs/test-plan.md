# Test Plan - Toolshop

Scenarios per feature (happy / boundary / negative), with the suite each is assigned to.
`Automated` = covered in this repo; `Planned` = not yet written. Test-plan-first: scenarios are listed before the suite is written.

## Authentication

| # | Scenario | Type | Suite | Status |
|---|----------|------|-------|--------|
| AUTH-1 | Valid credentials -> redirected to account | happy | smoke | Automated (UI + API) |
| AUTH-2 | Invalid password -> error shown / 401 | negative | regression | Automated (UI + API) |
| AUTH-3 | Valid login issues a bearer token with expiry | happy | smoke | Automated (API) |
| AUTH-4 | Empty fields -> validation blocks submit | boundary | regression | Planned |
| AUTH-5 | Locked / unknown account -> error | negative | regression | Planned |
| AUTH-6 | Register new customer -> 201 + typed body | happy | regression | Automated (API) |
| AUTH-7 | Register with missing fields -> 422 | negative | regression | Automated (API) |
| AUTH-8 | Register with existing email -> 409 | negative | regression | Automated (API) |

## Catalog & search

| # | Scenario | Type | Suite | Status |
|---|----------|------|-------|--------|
| CAT-1 | Search by name returns matching products | happy | smoke | Automated (UI) |
| CAT-2 | Product list is paginated, pages are distinct | happy | regression | Automated (API) |
| CAT-3 | Unknown product id -> 404 | negative | regression | Automated (API) |
| CAT-4 | Categories & brands expose expected shape | happy | regression | Automated (API) |
| CAT-5 | Search with no match -> empty state | boundary | regression | Automated (UI) |
| CAT-6 | Filter by category / brand narrows results | happy | regression | Planned |

## Cart & checkout

| # | Scenario | Type | Suite | Status |
|---|----------|------|-------|--------|
| CHK-1 | Add in-stock product -> cart badge increments | happy | smoke | Automated |
| CHK-2 | Full checkout (cart -> billing -> payment) succeeds; cart total reflects item price | happy | smoke | Automated |
| CHK-3 | Billing form blocks proceed until required fields set | boundary | regression | Partial (observed in recon) |
| CHK-4 | Payment method reveals its required sub-fields | boundary | regression | Planned |
| CHK-5 | Out-of-stock product cannot be added | negative | regression | Planned |
| CHK-6 | Update quantity recalculates totals | happy | regression | Planned |

## Accessibility

| # | Scenario | Type | Suite | Status |
|---|----------|------|-------|--------|
| A11Y-1 | Home page: no serious/critical axe violations | happy | a11y | Automated |
| A11Y-2 | Search is keyboard-operable | happy | a11y | Automated |
| A11Y-3 | Checkout pages: no serious/critical violations | happy | a11y | Planned |
| A11Y-4 | Focus returns to trigger after modal close | boundary | a11y | Planned |
