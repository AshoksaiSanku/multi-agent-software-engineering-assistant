# Lesson-04: Git Setup and Repository Hygiene

## Objective

Learn how Git tracks project changes and which files should never be committed.

## Knowledge Required

- **Git**: Source-control tool that records file history.
- **Commit**: A saved snapshot.
- **Repository**: A folder tracked by Git.
- **Working tree**: Your current files.
- **Staging area**: Files prepared for commit.
- **Ignore file**: `.gitignore` tells Git which generated files to skip.

## Commands

Check Git status:

```powershell
git status
```

If starting from a new folder:

```powershell
git init
```

Configure identity:

```powershell
git config user.name "Your Name"
git config user.email "you@example.com"
```

## Files Created In This Stage

```text
.gitignore
```

Purpose: Ignore generated artifacts like virtual environments, compiled files, databases, model artifacts, dependency folders, and build outputs.

## Common Mistakes

- Committing `.env` secrets.
- Committing `node_modules`.
- Committing `venv`.
- Committing generated Chroma/vector files.
- Committing local SQLite databases.

## Verification

`git status` should show only meaningful source files after `.gitignore` is created.

