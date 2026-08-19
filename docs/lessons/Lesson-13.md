# Lesson-13: Chat and Architecture Analysis RAG Flows

## Objective

Build repository-aware chat and architecture analysis.

## Files Created

```text
backend/app/services/chat_service.py
backend/app/services/analysis_service.py
backend/app/api/routes/chat.py
backend/app/api/routes/analysis.py
```

## Knowledge Required

- **RAG**: Retrieve relevant context before generating answers.
- **Conversation history**: Saved user/assistant messages.
- **Markdown**: Text format used for rich answers.
- **Source citation**: Referencing file paths used in answers.

## Data Flow

Question -> vector search -> context prompt -> AIService -> answer saved in database -> answer returned to frontend.

## Common Mistakes

- Answering without retrieved evidence.
- Not saving both user and assistant messages.
- Letting users access another user's repository context.

## Verification

Ask "list files" and a repository question after indexing a repository.

