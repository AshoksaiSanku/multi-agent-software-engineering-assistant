# Lesson-16: Exports - PDF Reports and ZIP Generated Projects

## Objective

Implement downloadable documentation artifacts.

## Files Created

```text
backend/app/services/export_service.py
backend/app/api/routes/documents.py
```

## Knowledge Required

- **StreamingResponse**: FastAPI response for file streams.
- **MIME type**: Browser hint for file type.
- **Content-Disposition**: Header that tells browser to download a file.
- **ReportLab**: Python PDF generation library.
- **ZipFile**: Python standard library archive writer.
- **BytesIO**: In-memory binary stream.

## Data Flow

Repository/project id -> ownership check -> report/zip generated -> binary stream returned to browser.

## Common Mistakes

- Wrong content type.
- Not seeking stream to start.
- Missing ownership check.

## Verification

Download generated project ZIP and repository PDF from API/frontend.

