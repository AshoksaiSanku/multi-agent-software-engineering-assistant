# Lesson-11: Vector Store, Embeddings, ChromaDB, Semantic Search

## Objective

Implement repository vector indexing and semantic search.

## Files Created

```text
backend/app/vector_store/__init__.py
backend/app/vector_store/store.py
```

## Knowledge Required

- **Embedding**: Numeric representation of text.
- **Vector**: List of numbers.
- **Vector database**: Stores vectors and finds similar ones.
- **ChromaDB**: Local vector database used here.
- **Semantic search**: Search by meaning, not just exact words.
- **Cosine similarity/distance**: Measures how similar vectors are.
- **HashingVectorizer**: scikit-learn tool for local deterministic embeddings.

## Data Flow

Code chunks -> embeddings -> Chroma collection -> query text becomes embedding -> nearest chunks returned.

## Common Mistakes

- Reindexing without deleting old vectors.
- Invalid Chroma collection names.
- Blocking async server with sync vector DB calls.

## Verification

Index two test chunks and query for one topic. The relevant file should rank first.

