from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(ORMModel):
    id: str
    email: EmailStr
    full_name: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class RepositoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    github_url: HttpUrl


class RepositoryResponse(ORMModel):
    id: str
    name: str
    github_url: str
    default_branch: str | None
    status: str
    file_count: int
    summary: dict
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class SemanticSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=2000)
    limit: int = Field(default=5, ge=1, le=12)


class SearchResult(BaseModel):
    file_path: str
    content: str
    score: float


class ChatRequest(BaseModel):
    repository_id: str | None = None
    question: str = Field(min_length=2, max_length=6000)


class ChatMessage(ORMModel):
    id: str
    repository_id: str | None
    role: str
    content: str
    created_at: datetime


class ChatResponse(BaseModel):
    answer: str
    sources: list[SearchResult] = Field(default_factory=list)


class CodeMetrics(BaseModel):
    cyclomatic_complexity: float = Field(ge=0, le=500)
    file_size: float = Field(ge=0, le=2_000_000)
    dependency_count: float = Field(ge=0, le=1000)
    commit_frequency: float = Field(ge=0, le=10000)


class PredictionRequest(BaseModel):
    repository_id: str | None = None
    file_path: str = Field(min_length=1, max_length=500)
    metrics: CodeMetrics


class PredictionResponse(ORMModel):
    id: str
    repository_id: str | None
    file_path: str
    features: dict
    bug_probability: float
    maintainability_score: float
    recommendations: list[str]
    created_at: datetime


class RepositoryMetricEstimate(BaseModel):
    repository_id: str
    file_path: str
    metrics: CodeMetrics
    available_files: list[str] = Field(default_factory=list)


class AgentRunRequest(BaseModel):
    repository_id: str | None = None
    project_name: str = Field(min_length=2, max_length=200)
    requirements: str = Field(min_length=10, max_length=12000)


class AgentRunAccepted(BaseModel):
    run_id: str
    status: str = "queued"


class AgentLogResponse(ORMModel):
    id: str
    run_id: str
    repository_id: str | None
    agent_name: str
    status: str
    message: str
    payload: dict
    created_at: datetime


class GeneratedProjectResponse(ORMModel):
    id: str
    name: str
    requirements: str
    files: dict
    created_at: datetime
