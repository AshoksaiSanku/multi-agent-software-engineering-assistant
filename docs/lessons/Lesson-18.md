# Lesson-18: Frontend Pages and Workflows

## Objective

Build all user-facing screens.

## Files Created

```text
frontend/src/pages/LoginPage.jsx
frontend/src/pages/DashboardPage.jsx
frontend/src/pages/RepositoriesPage.jsx
frontend/src/pages/ChatPage.jsx
frontend/src/pages/AgentsPage.jsx
frontend/src/pages/AnalysisPage.jsx
frontend/src/pages/MLPage.jsx
frontend/src/pages/DocumentsPage.jsx
```

## Knowledge Required

- **Controlled form**: Input value stored in React state.
- **Effect**: Code that runs after render, often for data loading.
- **Conditional rendering**: Showing UI only when conditions are true.
- **Optimistic update**: UI updates before server confirms, with rollback on error.
- **WebSocket client**: Browser connection for live events.
- **Blob download**: Browser downloads binary API response.

## Page Responsibilities

- `LoginPage`: register/login.
- `DashboardPage`: summary metrics.
- `RepositoriesPage`: GitHub ingestion/search/delete.
- `ChatPage`: repository chat.
- `AgentsPage`: run agents and stream logs.
- `AnalysisPage`: architecture report.
- `MLPage`: bug-risk prediction.
- `DocumentsPage`: PDF/ZIP exports.

## Common Mistakes

- Not handling loading states.
- Not catching API errors.
- Using stale selected repository state.
- Forgetting to close WebSocket on unmount.

## Verification

Log in and visit every route without console errors.

