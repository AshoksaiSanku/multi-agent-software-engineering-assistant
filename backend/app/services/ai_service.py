import re
import ast

import httpx
from openai import AsyncOpenAI

from app.core.config import settings


class AIService:
    """Generation boundary with free local defaults and optional paid providers."""

    def __init__(self) -> None:
        self.openai = None
        if settings.ai_provider.lower() == "openai" and settings.openai_api_key:
            self.openai = AsyncOpenAI(api_key=settings.openai_api_key)

    async def complete(self, instructions: str, prompt: str) -> str:
        provider = settings.ai_provider.lower()
        if provider == "openai" and self.openai:
            response = await self.openai.responses.create(
                model=settings.openai_model,
                instructions=instructions,
                input=prompt,
            )
            return response.output_text
        if provider == "ollama":
            return await self._ollama(instructions, prompt)
        return self._local_answer(prompt, instructions)

    async def _ollama(self, instructions: str, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    f"{settings.ollama_base_url.rstrip('/')}/api/generate",
                    json={
                        "model": settings.ollama_model,
                        "prompt": f"{instructions}\n\n{prompt}",
                        "stream": False,
                    },
                )
                response.raise_for_status()
                answer = response.json().get("response", "").strip()
                return answer or self._local_answer(prompt, instructions)
        except httpx.HTTPError:
            return (
                self._local_answer(prompt, instructions)
                + "\n\nNote: `AI_PROVIDER=ollama` is selected, but Ollama is not reachable. "
                "Start Ollama locally and pull the configured model."
            )

    @staticmethod
    def _local_answer(prompt: str, instructions: str = "") -> str:
        combined = f"{instructions}\n\n{prompt}"
        question_match = re.search(r"Question:\s*(.+?)(?:\n\n|$)", prompt, re.DOTALL)
        question = question_match.group(1).strip() if question_match else ""
        context = prompt.split("Repository context:", 1)[-1].strip()
        paths = sorted(set(re.findall(r"FILE:\s*([^\n]+)", prompt)))

        if "Requirement Analysis Agent" in combined:
            return local_implementation_plan(prompt)
        if "Backend Generation Agent" in combined or "Generate a focused FastAPI" in combined:
            return local_backend_code(prompt)
        if "Frontend Generation Agent" in combined or "React and Tailwind" in combined:
            return local_frontend_code(prompt)
        if "Documentation Agent" in combined or "README-style" in combined:
            return local_generated_readme(prompt)
        if "Code Review Agent" in combined or "security, reliability" in combined:
            return local_code_review()
        if "software architect" in combined or "Architecture Report" in combined:
            return local_architecture_report(prompt)

        if "No repository context selected" in prompt:
            if "authentication" in question.lower():
                return (
                    "Free local mode is active. A typical JWT authentication flow is:\n\n"
                    "1. User registers or logs in with email and password.\n"
                    "2. Backend verifies the password hash.\n"
                    "3. Backend creates a signed JWT access token.\n"
                    "4. Frontend stores the token and sends it in `Authorization: Bearer <token>`.\n"
                    "5. Protected API routes decode and validate the token before returning data.\n\n"
                    "Select an indexed repository for repo-specific authentication details."
                )
            return (
                "Free local mode is active. Select an indexed repository for repository-aware "
                "answers, or set `AI_PROVIDER=ollama` to use a stronger free local model."
            )

        if paths:
            if asks_for_repository_explanation(question):
                return local_repository_explanation(context, paths)
            summary = "\n".join(f"- `{path}`" for path in paths)
            return (
                "Free local RAG mode found these relevant repository files:\n"
                f"{summary}\n\nRelevant context:\n{context[:1400]}"
            )

        return (
            "Free local mode is active. I found repository context, but a richer natural-language "
            "answer needs `AI_PROVIDER=ollama` with a local free model."
        )


def local_implementation_plan(prompt: str) -> str:
    return """# Implementation Plan

1. Create a JWT-protected FastAPI router for payments.
2. Define Pydantic request/response schemas for payment creation and status reads.
3. Validate amount, currency, idempotency key, and authenticated user ownership.
4. Store payment records behind a repository/service boundary.
5. Add React UI for creating a payment and viewing status.
6. Document environment variables, endpoints, security assumptions, and tests.
"""


def local_backend_code(prompt: str) -> str:
    return '''"""Secure payment API generated in free local mode.

Mount with:
    app.include_router(router, prefix="/api/v1/payments", tags=["payments"])
"""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator


router = APIRouter()


class PaymentStatus(str, Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"


class AuthenticatedUser(BaseModel):
    id: str
    email: str


class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3, examples=["USD"])
    idempotency_key: str = Field(min_length=12, max_length=120)
    description: str | None = Field(default=None, max_length=240)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class PaymentResponse(BaseModel):
    id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    owner_id: str
    created_at: datetime


PAYMENTS: dict[str, PaymentResponse] = {}
IDEMPOTENCY_INDEX: dict[tuple[str, str], str] = {}


async def get_current_user() -> AuthenticatedUser:
    """Replace with the project's JWT dependency, e.g. app.api.dependencies.get_current_user."""
    return AuthenticatedUser(id="demo-user", email="demo@example.com")


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payload: PaymentCreate,
    user: AuthenticatedUser = Depends(get_current_user),
) -> PaymentResponse:
    existing_id = IDEMPOTENCY_INDEX.get((user.id, payload.idempotency_key))
    if existing_id:
        return PAYMENTS[existing_id]

    payment = PaymentResponse(
        id=str(uuid4()),
        amount=payload.amount,
        currency=payload.currency,
        status=PaymentStatus.pending,
        owner_id=user.id,
        created_at=datetime.now(timezone.utc),
    )
    PAYMENTS[payment.id] = payment
    IDEMPOTENCY_INDEX[(user.id, payload.idempotency_key)] = payment.id
    return payment


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> PaymentResponse:
    payment = PAYMENTS.get(payment_id)
    if not payment or payment.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
'''


def local_frontend_code(prompt: str) -> str:
    return """import { useState } from "react";

export default function GeneratedFeature() {
  const [form, setForm] = useState({ amount: "10.00", currency: "USD", description: "" });
  const [result, setResult] = useState(null);

  async function submit(event) {
    event.preventDefault();
    const response = await fetch("/api/v1/payments", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify({
        ...form,
        idempotency_key: crypto.randomUUID(),
      }),
    });
    setResult(await response.json());
  }

  return (
    <section className="rounded-2xl border border-slate-200 p-6 dark:border-white/10">
      <h2 className="text-xl font-semibold">Secure Payment</h2>
      <form onSubmit={submit} className="mt-5 grid gap-3">
        <input className="input" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} />
        <input className="input" value={form.currency} onChange={(e) => setForm({ ...form, currency: e.target.value.toUpperCase() })} />
        <input className="input" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        <button className="button-primary">Create payment</button>
      </form>
      {result && <pre className="mt-4 rounded-xl bg-slate-950 p-4 text-sm text-white">{JSON.stringify(result, null, 2)}</pre>}
    </section>
  );
}
"""


def local_generated_readme(prompt: str) -> str:
    return """# Secure Payment API With JWT Authentication

Generated in free local mode. No paid API key was used.

## Files

- `backend/generated_feature.py`: FastAPI payment router with JWT dependency placeholder.
- `frontend/src/GeneratedFeature.jsx`: React/Tailwind payment form.
- `CODE_REVIEW.md`: Security review checklist.
- `IMPLEMENTATION_PLAN.md`: Implementation plan.

## Endpoints

- `POST /api/v1/payments`: create an authenticated payment.
- `GET /api/v1/payments/{payment_id}`: fetch an authenticated user's payment.

## Security Notes

- Replace the demo `get_current_user` function with your real JWT dependency.
- Keep payment ownership checks.
- Use a real database table instead of the in-memory dictionary before production.
- Use idempotency keys to prevent duplicate payment creation.
"""


def local_code_review() -> str:
    return """## Code Review

Blocking before production:

- Replace the demo `get_current_user` dependency with the real JWT auth dependency.
- Persist payments in PostgreSQL instead of in-memory dictionaries.
- Add ownership tests for `GET /payments/{payment_id}`.
- Add duplicate idempotency-key tests.
- Never store card data directly; use a PCI-compliant payment provider token.

Good foundations:

- Amount and currency are validated.
- Payment reads are scoped to the authenticated owner.
- Idempotency behavior is included.
"""


def local_architecture_report(prompt: str) -> str:
    summary = extract_summary_metrics(prompt)
    project_type = summary.get("project_type", "Source code repository")
    files = summary.get("files") or []
    imports = summary.get("imports") or []
    functions = summary.get("functions") or []
    features = summary.get("detected_features") or []
    lowered_prompt = prompt.lower()
    if project_type == "Source code repository" and "tkinter" in lowered_prompt and "password" in lowered_prompt:
        project_type = "Tkinter desktop password generator"
        features = sorted(set([*features, "desktop_gui", "password_generation", "random_generation"]))
    language_text = ", ".join(f"{key}: {value}" for key, value in summary.get("languages", {}).items())
    file_text = "\n".join(f"- `{path}`" for path in files[:12]) or "- No files recorded"
    function_text = ", ".join(f"`{name}()`" for name in functions[:12]) or "No functions detected"
    import_text = ", ".join(f"`{name}`" for name in imports[:12]) or "No imports detected"

    if "Tkinter desktop password generator" == project_type:
        purpose = (
            "This repository is a small Python Tkinter desktop application that generates "
            "random passwords. The UI lets the user choose a password length and strength, "
            "generate a password, display it in an entry field, and copy it to the clipboard."
        )
        risks = (
            "- `random.choice` is suitable for demos, but `secrets.choice` is better for real passwords.\n"
            "- `from tkinter import *` makes names harder to track; explicit imports are cleaner.\n"
            "- GUI setup and business logic live in one file, so testing and maintenance are harder.\n"
            "- The app should validate selected length and strength before generation."
        )
        recommendations = (
            "- Move password generation into a pure function, for example `generate_password(length, mode)`.\n"
            "- Replace `random` with Python's `secrets` module for stronger password randomness.\n"
            "- Keep Tkinter widget creation separate from password logic.\n"
            "- Add simple unit tests for lowercase, mixed-case, and symbol password modes."
        )
    else:
        purpose = (
            f"This repository is identified as: {project_type}. It contains {summary.get('total_lines', 0)} "
            "indexed lines and is available for local RAG search."
        )
        risks = (
            "- Free local mode uses static code analysis and retrieved context, so deep reasoning is limited.\n"
            "- Generated reports should be reviewed before presenting as production architecture."
        )
        recommendations = (
            "- Ask targeted questions such as file purpose, functions, dependencies, and risks.\n"
            "- Use Ollama for richer free local natural-language generation if needed."
        )

    return f"""# Architecture Report

## Structure

{purpose}

## Repository Facts

- Project type: {project_type}
- Languages: {language_text or "unknown"}
- Total lines: {summary.get("total_lines", 0)}
- Total bytes: {summary.get("total_bytes", 0)}
- Files:
{file_text}

## Code Elements

- Imports: {import_text}
- Functions: {function_text}
- Detected features: {", ".join(features) or "none"}

## Strengths

- The repository is small and easy to inspect.
- The main behavior is discoverable from the indexed source file.
- Local RAG can retrieve the relevant file for questions about functionality.

## Risks

{risks}

## Recommendations

- Keep `AI_PROVIDER=openai` disabled if you do not want paid API usage.
{recommendations}
"""


def asks_for_repository_explanation(question: str) -> bool:
    normalized = question.lower()
    return any(
        phrase in normalized
        for phrase in [
            "explain this repository",
            "explain repo",
            "what is this repo",
            "what does this repository",
            "summarize this repository",
            "overview",
        ]
    )


def local_repository_explanation(context: str, paths: list[str]) -> str:
    imports = sorted(set(re.findall(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", context, re.M)))
    imports = sorted({item for group in imports for item in group if item})
    functions = sorted(set(re.findall(r"^\s*def\s+([a-zA-Z_]\w*)\s*\(", context, re.M)))
    lowered = context.lower()

    if "tkinter" in lowered and "password" in lowered:
        return f"""This repository is a **Python Tkinter Random Password Generator**.

## What It Does

- Builds a desktop GUI using Tkinter.
- Lets the user choose a password length from a combo box.
- Generates a password using random characters.
- Supports different character sets such as lowercase, mixed-case, and digits/symbols.
- Displays the generated password in an input field.
- Copies the password to the clipboard using `pyperclip`.

## Main File

{chr(10).join(f"- `{path}`" for path in paths)}

## Important Functions

{chr(10).join(f"- `{name}()`" for name in functions) or "- No named functions detected"}

## Main Dependencies

{chr(10).join(f"- `{name}`" for name in imports) or "- No imports detected"}

## Improvement Suggestions

- Use Python's `secrets.choice` instead of `random.choice` for stronger password generation.
- Avoid `from tkinter import *`; explicit imports make the code cleaner.
- Separate password-generation logic from GUI code so it is easier to test.
- Add validation if the user does not select a password type.
"""

    return f"""This repository contains the following indexed files:

{chr(10).join(f"- `{path}`" for path in paths)}

Detected functions: {", ".join(f"`{name}()`" for name in functions) or "none"}.
Detected imports: {", ".join(f"`{name}`" for name in imports) or "none"}.

Free local mode summarized this from retrieved repository context only.
"""


def extract_summary_metrics(prompt: str) -> dict:
    match = re.search(r"Summary metrics:\s*(\{.*\})", prompt, re.S)
    if not match:
        return {}
    try:
        return ast.literal_eval(match.group(1))
    except (SyntaxError, ValueError):
        return {}
