# Lesson-19: Testing, Debugging, and CI

## Objective

Add automated tests and CI checks.

## Files Created

```text
backend/pytest.ini
backend/tests/test_health.py
.github/workflows/ci.yml
```

## Knowledge Required

- **Test**: Code that verifies other code.
- **Pytest**: Python test framework.
- **TestClient**: FastAPI testing client.
- **Assertion**: Statement that must be true.
- **CI**: Automated checks on GitHub.
- **GitHub Actions**: CI workflow runner.
- **YAML**: Configuration file format.

## Data Flow

CI trigger -> install dependencies -> compile backend -> run tests -> install frontend dependencies -> build frontend.

## Common Mistakes

- Importing app before test environment variables.
- Tests relying on real external services.
- CI working directory wrong.
- Not testing cleanup side effects.

## Verification

Run:

```powershell
pytest
```

and:

```powershell
npm run build
```

from the correct folders.

