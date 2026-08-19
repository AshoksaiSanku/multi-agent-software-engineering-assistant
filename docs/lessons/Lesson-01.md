# Lesson-01: Project Overview, Learning Contract, and VS Code Orientation

## Objective

By the end of this lesson, you will understand what we are going to build, why the project exists, how the major parts fit together, and how to use VS Code as your engineering workspace.

You will not write backend or frontend application code in this lesson yet. That is intentional. A professional engineer first understands the goal, the tools, the architecture, and the workflow before typing code.

## What We Are Building

Project name:

```text
Multi-Agent Software Engineering Assistant
```

This project is a full-stack software engineering platform.

In simple language, it is a web application where a user can:

1. Create an account and log in.
2. Add a GitHub repository URL.
3. Let the backend read and index source-code files.
4. Ask questions about the repository.
5. Run multiple AI-style engineering agents that plan, generate code, document work, and review code.
6. Predict bug risk and maintainability using machine learning.
7. Export architecture reports as PDF files.
8. Export generated project artifacts as ZIP files.

In technical language, it is a React frontend connected to a FastAPI backend that uses JWT authentication, SQLAlchemy persistence, ChromaDB vector search, retrieval-augmented generation, LangGraph workflow orchestration, XGBoost/scikit-learn ML models, Docker deployment, and GitHub Actions CI.

Do not worry if many words are new. This course will explain every one before we use it.

## Why This Lesson Exists

This lesson exists because beginners often start by typing code without understanding the system they are building. That causes confusion later.

Before creating folders and files, you need to know:

- What the project does.
- Which major parts exist.
- Why each part exists.
- Which tools you will use.
- How to navigate VS Code.
- How professional developers move through a project.

Skipping this lesson would make later backend, frontend, database, Docker, and AI lessons feel disconnected.

## Expected Outcome

After this lesson, you should be able to explain:

- What a full-stack application is.
- What frontend and backend mean.
- Why the project uses a database.
- Why the project uses AI/RAG/vector search.
- Why the project uses machine learning.
- Why Docker is useful.
- What the main VS Code panels do.
- How this project will be rebuilt step by step.

You should also be able to open VS Code, open the correct folder, open the terminal, and identify the main panels.

## Prerequisites

You need:

- A Windows computer.
- VS Code installed.
- The existing completed project available only as a reference.
- A willingness to manually type code in future lessons.

You do not need prior knowledge of programming for this lesson.

## Concepts

### Software Project

A software project is a collection of files and folders that work together to create an application.

This project contains:

- Backend code.
- Frontend code.
- Database models.
- Machine learning code.
- AI workflow code.
- Documentation.
- Tests.
- Docker deployment files.
- CI automation.

### Full-Stack Application

A full-stack application has at least two major parts:

- **Frontend**: The part users see in the browser.
- **Backend**: The server-side part that handles data, security, APIs, databases, and business logic.

This project is full-stack because it has both:

- A React frontend in the `frontend` folder.
- A FastAPI backend in the `backend` folder.

### Frontend

The frontend is the user interface.

In this project, the frontend:

- Shows the login page.
- Shows dashboards.
- Lets users add GitHub repositories.
- Lets users chat with repository context.
- Lets users launch agents.
- Lets users download PDF and ZIP files.

Technology used:

- **JavaScript**: The programming language used in the browser.
- **React**: A JavaScript library for building user interfaces from components.
- **Vite**: A tool that runs and builds the React application.
- **Tailwind CSS**: A styling framework that provides utility classes.

### Backend

The backend is the server-side application.

In this project, the backend:

- Creates user accounts.
- Logs users in.
- Verifies JWT tokens.
- Reads GitHub repositories.
- Stores data in a database.
- Stores repository chunks in a vector database.
- Answers questions using RAG.
- Runs agent workflows.
- Runs ML predictions.
- Generates PDF and ZIP exports.

Technology used:

- **Python**: The backend programming language.
- **FastAPI**: The web framework used to build APIs.
- **SQLAlchemy**: The database ORM.
- **ChromaDB**: The vector database.
- **LangGraph**: The workflow engine for agents.
- **scikit-learn and XGBoost**: Machine learning libraries.

### API

API means Application Programming Interface.

In this project, the API is the set of backend URLs the frontend calls.

Examples:

```text
POST /api/v1/auth/login
GET  /api/v1/repositories
POST /api/v1/chat
POST /api/v1/ml/predict
```

The frontend sends requests to these endpoints. The backend sends responses back.

### Database

A database stores data permanently.

This project stores:

- Users.
- Repositories.
- Chat messages.
- ML predictions.
- Agent logs.
- Generated project files.

Technologies used:

- **PostgreSQL** in Docker deployment.
- **SQLite** for easy local development/testing.
- **SQLAlchemy** to write database logic in Python.

### AI Agents

An agent is a software component that performs a specific task.

This project has multiple specialist agents:

1. Requirement Analysis Agent.
2. Repository Understanding Agent.
3. Backend Generation Agent.
4. Frontend Generation Agent.
5. Documentation Agent.
6. Code Review Agent.

They run in order using LangGraph.

### RAG

RAG means Retrieval-Augmented Generation.

Simple explanation:

1. The system reads repository files.
2. It breaks files into chunks.
3. It stores searchable representations of those chunks.
4. When the user asks a question, it retrieves relevant chunks.
5. It uses those chunks to answer.

Why this matters:

Without RAG, the assistant may answer generally.

With RAG, the assistant can answer using actual repository evidence.

### Vector Database

A vector database stores numbers that represent text meaning.

In this project:

- Source-code chunks become vectors.
- A user question becomes a vector.
- ChromaDB finds code chunks with similar meaning.

This enables semantic search, meaning the system can find relevant code even if the exact words are different.

### Machine Learning

Machine learning is a way for software to learn patterns from data.

This project uses ML to estimate:

- Bug probability.
- Maintainability score.

It uses code metrics such as:

- Cyclomatic complexity.
- File size.
- Dependency count.
- Commit frequency.

### Docker

Docker packages applications into containers.

A container is like a small isolated computer environment for one service.

This project uses Docker to run:

- PostgreSQL database.
- FastAPI backend.
- React/Nginx frontend.

### CI

CI means Continuous Integration.

It automatically checks the project when code changes.

This project uses GitHub Actions to:

- Install backend dependencies.
- Compile backend Python files.
- Run backend tests.
- Install frontend dependencies.
- Build frontend production files.

## Tools

### VS Code

VS Code is the code editor we will use.

It helps you:

- Create folders.
- Create files.
- Edit code.
- Run terminal commands.
- Search files.
- Use Git.
- Read errors.
- Install extensions.
- Debug applications.

### Terminal

The terminal lets you type commands.

Examples of commands we will use later:

```powershell
python --version
node --version
npm --version
docker --version
git status
```

We will not run project-building commands in this first lesson yet.

### Browser

The browser displays the frontend.

Later, we will open:

```text
http://localhost:5173
```

for local frontend development, and:

```text
http://localhost:3000
```

for Docker deployment.

## Commands

No project commands are required in this lesson.

However, you should learn what a command is.

A command is an instruction typed into the terminal.

Example:

```powershell
python --version
```

Explanation:

- `python` means we are asking the Python program to run.
- `--version` asks Python to print its installed version.

Expected output later:

```text
Python 3.x.x
```

Possible error:

```text
python is not recognized as an internal or external command
```

Meaning:

Python is not installed or not added to PATH.

PATH is a system setting that tells Windows where executable programs are located.

## Folder Creation

No folder creation is required in this lesson.

In the next lessons, we will create folders manually in chronological order.

The future root project folder will contain:

```text
Multi-Agent Software Engineering Assistant
├── backend
├── frontend
├── docs
├── docker
└── .github
```

Explanation:

- `backend` will contain server-side Python code.
- `frontend` will contain browser UI code.
- `docs` will contain documentation.
- `docker` will contain Nginx/Docker support files.
- `.github` will contain GitHub Actions automation.

## File Creation

No application file is created in this lesson.

This lesson itself is documentation:

```text
docs/lessons/Lesson-01.md
```

Why this file exists:

It begins the course and sets the learning foundation.

Why the filename was selected:

The course uses numbered lessons so we can build the project in order.

Why the extension is `.md`:

`.md` means Markdown. Markdown is a simple text format for headings, lists, code blocks, and documentation.

## VS Code Orientation

Open VS Code now.

### Step 1: Open VS Code

Why this step is necessary:

VS Code is where you will create, edit, run, test, and organize the project.

What problem it solves:

It gives you one professional workspace instead of editing files randomly.

What happens if we skip it:

You will not have a consistent place to type files and run commands.

Action:

1. Press the Windows key.
2. Type `Visual Studio Code`.
3. Press `Enter`.

Expected result:

VS Code opens.

### Step 2: Open the Project Folder

Why this step is necessary:

VS Code needs to know which folder is your workspace.

Action:

1. In VS Code, click `File`.
2. Click `Open Folder`.
3. Select:

```text
C:\Users\DELL\Documents\Multi-Agent Ai Software Engineering Assistant
```

4. Click `Select Folder`.

Expected result:

The project files appear in the Explorer panel.

### Step 3: Understand the Explorer Panel

The Explorer panel shows files and folders.

Where it is:

Usually on the left side of VS Code.

Icon:

Looks like two files.

Shortcut:

```text
Ctrl + Shift + E
```

Why it matters:

You will use Explorer to create folders, create files, rename files, and open files.

Common beginner mistake:

Creating files in the wrong folder. Always check the folder path before creating a file.

### Step 4: Understand the Search Panel

The Search panel lets you find words across the project.

Shortcut:

```text
Ctrl + Shift + F
```

Why it matters:

In real projects, you often search for function names, route names, variables, or errors.

Example:

If you search for:

```text
auth
```

VS Code shows all files containing that word.

### Step 5: Understand the Source Control Panel

Source Control is where Git changes appear.

Shortcut:

```text
Ctrl + Shift + G
```

Why it matters:

Git helps track every change you make.

Common terms:

- **Modified**: A file changed.
- **Staged**: A file is prepared for commit.
- **Commit**: A saved snapshot of changes.
- **Repository**: A folder tracked by Git.

We will learn Git properly in a later lesson.

### Step 6: Understand the Run and Debug Panel

The Run and Debug panel helps start programs with debugging.

Shortcut:

```text
Ctrl + Shift + D
```

Why it matters:

Debugging means pausing code while it runs so you can inspect variables and understand behavior.

We will not debug yet, but you should know the panel exists.

### Step 7: Understand the Extensions Panel

Extensions add features to VS Code.

Shortcut:

```text
Ctrl + Shift + X
```

Examples of useful extensions later:

- Python.
- Pylance.
- ESLint.
- Docker.
- Tailwind CSS IntelliSense.

Common beginner mistake:

Installing too many extensions without understanding them. We will install only what we need.

### Step 8: Understand the Terminal Panel

The terminal runs commands.

Shortcut:

```text
Ctrl + `
```

The backtick key is usually below `Esc`.

Alternative menu:

1. Click `Terminal`.
2. Click `New Terminal`.

Why it matters:

We will use the terminal to install dependencies, run servers, run tests, build Docker containers, and use Git.

## High-Level Architecture

Here is the big-picture architecture:

```text
Browser
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  +--> PostgreSQL / SQLite Database
  |
  +--> GitHub API
  |
  +--> ChromaDB Vector Store
  |
  +--> Local / Ollama / OpenAI AI Service
  |
  +--> ML Models
```

Explanation:

- The browser runs the React frontend.
- The frontend sends HTTP requests to the FastAPI backend.
- The backend checks authentication.
- The backend stores and reads data from the database.
- The backend fetches repository files from GitHub.
- The backend indexes source-code chunks in ChromaDB.
- The backend uses AI logic to answer questions or generate agent outputs.
- The backend uses ML models to predict code risk.

## Request Lifecycle

Example: user asks a repository question.

```text
User types question
  |
  v
React ChatPage sends POST /api/v1/chat
  |
  v
FastAPI chat route receives request
  |
  v
JWT token verifies user identity
  |
  v
ChatService retrieves relevant code chunks from ChromaDB
  |
  v
AIService creates answer
  |
  v
Conversation saved in database
  |
  v
Backend returns JSON response
  |
  v
React displays answer as markdown
```

## Data Flow

The main data flow for repository ingestion:

```text
GitHub URL
  |
  v
Repository API route
  |
  v
Repository row saved as queued
  |
  v
Background ingestion starts
  |
  v
GitHub files fetched
  |
  v
Files split into chunks
  |
  v
Chunks embedded into vectors
  |
  v
Vectors stored in ChromaDB
  |
  v
Metadata stored in SQL database
  |
  v
Repository marked ready
```

## Design Decisions

### Why React?

React is widely used in companies to build interactive browser interfaces.

Alternative:

- Plain HTML/CSS/JavaScript.
- Vue.
- Angular.

Why React was chosen:

- Component-based.
- Large ecosystem.
- Good for dashboards.
- Works well with Vite.

### Why FastAPI?

FastAPI is a modern Python web framework.

Alternative:

- Flask.
- Django.
- Express with Node.js.

Why FastAPI was chosen:

- Fast to develop.
- Built-in validation with Pydantic.
- Automatic API documentation.
- Good async support.
- Clean dependency injection.

### Why PostgreSQL?

PostgreSQL is a reliable relational database used in many companies.

Alternative:

- SQLite.
- MySQL.
- MongoDB.

Why PostgreSQL was chosen:

- Good production database.
- Strong SQL support.
- Works well with SQLAlchemy.
- Runs easily in Docker.

### Why ChromaDB?

ChromaDB is a vector database.

Alternative:

- FAISS.
- Pinecone.
- Weaviate.
- pgvector.

Why ChromaDB was chosen:

- Easy local setup.
- Persistent storage.
- Good for demos and local RAG.

### Why LangGraph?

LangGraph lets us define an ordered workflow of AI agents.

Alternative:

- Manual function calls.
- Celery workflows.
- LangChain chains.

Why LangGraph was chosen:

- Explicit graph structure.
- Good for multi-step agent workflows.
- Easy to stream updates.

### Why Docker?

Docker makes the project easier to run consistently.

Alternative:

- Install everything manually on the machine.

Why Docker was chosen:

- Reproducible environment.
- Easy database setup.
- Easier deployment.

## Common Mistakes

### Mistake 1: Trying to Build Everything at Once

Problem:

The project has many parts. Building all parts at once causes confusion.

Fix:

Build one layer at a time:

1. Environment.
2. Backend foundation.
3. Database.
4. Auth.
5. Repository ingestion.
6. RAG.
7. Agents.
8. ML.
9. Frontend.
10. Docker.

### Mistake 2: Not Understanding the Folder Structure

Problem:

Files end up in the wrong place.

Fix:

Before creating any file, ask:

- Is this backend?
- Is this frontend?
- Is this configuration?
- Is this documentation?
- Is this test code?

### Mistake 3: Copying Code Without Understanding

Problem:

You can run the project but cannot explain it in an interview.

Fix:

Manually type code and explain every line.

### Mistake 4: Ignoring Errors

Problem:

Small errors grow into confusing failures.

Fix:

Read the first error message carefully. Fix one error at a time.

## Debugging

No code is running yet, so debugging in this lesson is about environment awareness.

Potential issue:

VS Code opens the wrong folder.

Diagnosis:

Explorer does not show `backend`, `frontend`, `docs`, or `docker`.

Fix:

Use:

```text
File -> Open Folder
```

and select the correct project folder.

Potential issue:

Terminal opens in the wrong directory.

Diagnosis:

The terminal prompt does not show the project path.

Fix:

In VS Code, open the correct folder first, then open a new terminal.

## Verification

Verify these items before moving to the next lesson:

1. VS Code is open.
2. The correct project folder is open.
3. Explorer is visible.
4. You can open the terminal using:

```text
Ctrl + `
```

5. You can explain the difference between frontend and backend.
6. You can explain why the project needs a database.
7. You can explain the basic idea of RAG.
8. You can explain what Docker is used for.

## Summary

In this lesson, you learned the purpose of the project and the major technologies involved.

You learned that the project is a full-stack application with:

- React frontend.
- FastAPI backend.
- SQL database.
- ChromaDB vector search.
- RAG chat.
- LangGraph agents.
- ML predictions.
- Docker deployment.
- GitHub Actions CI.

You also learned how to orient yourself in VS Code.

## Revision Questions

Answer these in your own words before continuing:

1. What is a full-stack application?
2. What is the frontend responsible for?
3. What is the backend responsible for?
4. Why does this project need a database?
5. What is an API?
6. What does RAG mean?
7. What is a vector database used for?
8. What is an AI agent in this project?
9. Why do we use Docker?
10. What does the VS Code Explorer panel do?
11. What does the VS Code terminal do?
12. Why should we build the project one lesson at a time?

## Homework

Do this manually:

1. Open VS Code.
2. Open the project folder.
3. Open the Explorer panel.
4. Open the Terminal panel.
5. Read the root folder names.
6. Say out loud what each folder is probably responsible for.

Do not write project code yet.

## Stop Point

Stop here.

Before continuing to Lesson 02, confirm that:

- You opened VS Code.
- You opened the correct folder.
- You understand the basic project goal.
- You understand the difference between frontend and backend.
- You are ready to learn the full architecture and folder structure next.

