# Lesson-10: Repository Ingestion with GitHub API

## Objective

Implement GitHub repository reading and source-file preparation.

## Files Created

```text
backend/app/services/github_service.py
backend/app/services/repository_service.py
backend/app/api/routes/repositories.py
```

## Knowledge Required

- **GitHub API**: HTTP API for repository metadata and file trees.
- **HTTP client**: Code that sends web requests; this project uses `httpx`.
- **URL parsing**: Reading owner/repo from a GitHub URL.
- **Background task**: Work started after an API response.
- **Chunking**: Splitting files into smaller text pieces.
- **Repository status**: queued, indexing, ready, failed.

## Data Flow

Frontend submits GitHub URL -> backend saves repository as queued -> background task fetches files -> source files are filtered and chunked -> later vector indexing stores chunks.

## Common Mistakes

- Fetching huge files.
- Fetching binary files.
- Not handling GitHub rate limits.
- Not recording failure messages.

## Verification

Create repository through API and confirm status changes from queued/indexing to ready or failed with a useful error.

