# Lesson-03: Development Environment Setup

## Objective

Prepare the tools needed to rebuild and run the project.

## Tools Required

- VS Code: code editor.
- Python 3.12 or compatible: backend language runtime.
- Node.js 22 or compatible: frontend JavaScript runtime and npm package manager.
- Git: source control.
- Docker Desktop: container runtime for PostgreSQL, backend, and frontend deployment.
- Browser: to test the UI.

## Knowledge Required

- **Runtime**: Software that executes code. Python executes backend code; Node.js executes frontend build tools.
- **Package manager**: Installs libraries. Python uses `pip`; Node.js uses `npm`.
- **PATH**: A Windows system variable that lets terminal commands find installed programs.
- **Virtual environment**: An isolated Python dependency folder.
- **Terminal**: Text interface for commands.

## Commands To Verify Tools

Run these in VS Code terminal:

```powershell
python --version
```

Expected output: a Python version.

```powershell
node --version
```

Expected output: a Node.js version.

```powershell
npm --version
```

Expected output: an npm version.

```powershell
git --version
```

Expected output: a Git version.

```powershell
docker --version
```

Expected output: a Docker version.

## Common Errors

- Command not recognized: tool is not installed or not on PATH.
- Docker command fails: Docker Desktop is not running.
- Python opens Microsoft Store: install Python from python.org and add it to PATH.

## Why This Lesson Comes Now

Every future lesson depends on these tools. If the environment is broken, code that is correct will still fail.

## Verification

All version commands should print a version number.

