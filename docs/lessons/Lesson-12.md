# Lesson-12: AI Service, Local Fallback, Ollama/OpenAI Provider Boundary

## Objective

Create one controlled boundary for AI text generation.

## Files Created

```text
backend/app/services/ai_service.py
```

## Knowledge Required

- **LLM**: Large language model that generates text.
- **Provider boundary**: A wrapper hiding which AI service is used.
- **Local fallback**: Deterministic code path that avoids paid APIs.
- **Ollama**: Local LLM server.
- **OpenAI API**: Optional cloud model provider.
- **Prompt**: Text instructions sent to an AI model.
- **Prompt injection**: Malicious text inside repository content that tries to control the assistant.

## Data Flow

Service receives instructions and prompt -> selects provider based on settings -> returns generated text.

## Common Mistakes

- Sending private code to cloud AI unintentionally.
- Trusting repository text as instructions.
- No fallback when provider is unavailable.

## Verification

With `AI_PROVIDER=local`, chat and agents should still produce deterministic demo output.

