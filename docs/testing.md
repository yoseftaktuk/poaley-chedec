# Testing Guide

This project uses **Vitest** (frontend) and **pytest** (backend) with coverage reporting and CI integration.

## Quick Start

```bash
# Frontend
cd frontend && npm run test

# Backend (requires PostgreSQL test database)
cd backend && pytest
```

## Frontend

### Scripts

| Script | Description |
|--------|-------------|
| `npm run test` | Run all tests once |
| `npm run test:watch` | Watch mode |
| `npm run test:coverage` | Run with coverage report (80% threshold) |

### Run a single test

```bash
npm run test -- src/lib/utils.test.ts
npm run test -- -t "renders button"
```

### Coverage report

After `npm run test:coverage`, open `frontend/coverage/index.html`.

### Directory structure

```
frontend/src/
  test/
    setup.ts          # Global setup, MSW, mocks
    utils.tsx         # renderWithProviders()
    mocks/
      handlers.ts     # MSW API handlers
      server.ts       # MSW server
  **/*.test.ts(x)     # Colocated or mirrored tests
```

### Conventions

- Use **MSW** for API mocking — no real network calls
- Use `renderWithProviders()` for components needing Router/QueryClient
- Mock `IntersectionObserver` and `matchMedia` in setup (already configured)
- **No arbitrary `setTimeout`** — use `waitFor`, `findBy*`, or MSW
- Prefer `userEvent` over `fireEvent` for interactions

## Backend

### Requirements

- PostgreSQL test database (default: `poaley_chedec_test`)
- Set `TEST_DATABASE_URL` if using a different connection string

```bash
# Create test database (local)
createdb poaley_chedec_test
```

### Scripts

```bash
cd backend
pytest                    # All tests with coverage (pythonpath configured in pytest.ini)
pytest tests/api/test_auth.py   # Single file
pytest -k "test_login"    # By name
pytest --cov=app --cov-report=html  # HTML coverage
```

Always run pytest from the `backend/` directory so the `app` package resolves correctly.

### Coverage report

After `pytest`, open `backend/htmlcov/index.html`. Target: **90%**.

### Directory structure

```
backend/tests/
  conftest.py           # DB fixtures, client, auth helpers
  api/                  # Endpoint integration tests
  services/             # Business logic unit tests
  schemas/              # Pydantic validation tests
```

### Conventions

- Tests use a **separate test database** — never production
- Each test runs in a **rolled-back transaction** for isolation
- Rate limiter is disabled in tests
- Mock external services (Cloudinary, SMTP) — never call real APIs
- Use `auth_headers` fixture for protected endpoints

## CI

GitHub Actions workflow `.github/workflows/test.yml` runs both frontend and backend tests on push/PR. Pipeline fails if tests fail or coverage thresholds are not met.

## Writing new tests

1. **Utilities** — pure functions, no mocks needed
2. **Hooks** — `renderHook` with `createWrapper()`
3. **Components** — RTL + `renderWithProviders`
4. **API endpoints** — `client` fixture + `auth_headers` for admin routes
5. **Schemas** — valid/invalid payload assertions with `pytest.raises(ValidationError)`

## Best practices

- Keep tests deterministic and independent
- One logical assertion per test when possible
- Name tests by behavior: `test_login_rejects_invalid_password`
- Extract shared fixtures to `conftest.py`
- Refactor untestable code into pure functions rather than skipping coverage
