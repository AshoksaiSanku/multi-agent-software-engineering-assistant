# Lesson-05: Root Project Files and Documentation Foundation

## Objective

Create root-level files that explain and configure the project before writing application logic.

## Files Created

```text
.dockerignore
.env.example
.gitignore
README.md
docker-compose.yml
docs/ARCHITECTURE.md
docs/API.md
docs/DEPLOYMENT.md
```

## Knowledge Required

- **Markdown**: Plain-text documentation format.
- **Environment variable**: Runtime configuration value.
- **Docker Compose**: Tool for running multiple containers.
- **Documentation-first development**: Explaining architecture before implementation.

## Responsibilities

- `.env.example`: Documents required configuration.
- `.dockerignore`: Keeps Docker build context clean.
- `README.md`: Gives project overview and quick start.
- `docker-compose.yml`: Later runs database, API, and frontend.
- `docs/*`: Explains architecture, API, and deployment.

## Common Mistakes

- Putting real secrets in `.env.example`.
- Writing documentation that does not match actual code.
- Forgetting to update docs after route or config changes.

## Verification

You should be able to explain every root file before backend coding begins.

