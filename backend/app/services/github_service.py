from dataclasses import dataclass
from urllib.parse import urlparse

import httpx

from app.core.config import settings


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".css",
    ".html",
    ".md",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".sql",
    ".sh",
    ".dockerfile",
}
SKIP_PATHS = {"node_modules", "dist", "build", ".git", "vendor", "coverage", ".next"}


@dataclass
class GitHubFile:
    path: str
    content: str
    size: int


class GitHubRepositoryClient:
    def __init__(self) -> None:
        self.headers = {"Accept": "application/vnd.github+json"}
        if settings.github_token:
            self.headers["Authorization"] = f"Bearer {settings.github_token}"

    @staticmethod
    def parse_repository_url(github_url: str) -> tuple[str, str]:
        parsed = urlparse(github_url)
        if parsed.hostname not in {"github.com", "www.github.com"}:
            raise ValueError("Only github.com repository URLs are supported")
        pieces = [part for part in parsed.path.strip("/").split("/") if part]
        if len(pieces) < 2:
            raise ValueError("A GitHub URL must contain an owner and repository")
        return pieces[0], pieces[1].removesuffix(".git")

    async def fetch_files(self, github_url: str) -> tuple[str, list[GitHubFile]]:
        owner, repository = self.parse_repository_url(github_url)
        async with httpx.AsyncClient(
            base_url="https://api.github.com", headers=self.headers, timeout=30
        ) as client:
            metadata = await client.get(f"/repos/{owner}/{repository}")
            self._raise_for_github_error(metadata, f"{owner}/{repository}")
            default_branch = metadata.json()["default_branch"]
            tree_response = await client.get(
                f"/repos/{owner}/{repository}/git/trees/{default_branch}",
                params={"recursive": "1"},
            )
            self._raise_for_github_error(tree_response, f"{owner}/{repository}")
            candidates = [
                node
                for node in tree_response.json().get("tree", [])
                if node.get("type") == "blob" and self._supported(node["path"], node["size"])
            ][: settings.max_repository_files]
            files: list[GitHubFile] = []
        async with httpx.AsyncClient(timeout=30) as raw_client:
            for node in candidates:
                raw_url = (
                    f"https://raw.githubusercontent.com/{owner}/{repository}/"
                    f"{default_branch}/{node['path']}"
                )
                response = await raw_client.get(raw_url)
                if response.status_code == 404:
                    continue
                if response.status_code == 403:
                    raise RuntimeError(
                        "GitHub raw content rate limit was reached. Add a free "
                        "`GITHUB_TOKEN` in `.env`, restart the backend, and try again."
                    )
                response.raise_for_status()
                try:
                    content = response.text
                    content.encode("utf-8")
                except UnicodeError:
                    continue
                files.append(GitHubFile(node["path"], content, node["size"]))
        return default_branch, files

    @staticmethod
    def _supported(path: str, size: int) -> bool:
        lower_path = path.lower()
        if any(part in SKIP_PATHS for part in lower_path.split("/")):
            return False
        if size > 250_000:
            return False
        if lower_path.endswith("dockerfile"):
            return True
        return any(lower_path.endswith(extension) for extension in ALLOWED_EXTENSIONS)

    @staticmethod
    def _raise_for_github_error(response: httpx.Response, repository: str) -> None:
        if response.status_code == 403:
            remaining = response.headers.get("x-ratelimit-remaining")
            if remaining == "0" or "rate limit" in response.text.lower():
                raise RuntimeError(
                    "GitHub API rate limit exceeded while indexing "
                    f"`{repository}`. Create a free GitHub personal access token, set "
                    "`GITHUB_TOKEN=...` in `.env`, restart the backend, and retry. "
                    "This is not a paid AI API key."
                )
        if response.status_code == 404:
            raise RuntimeError(
                f"GitHub repository `{repository}` was not found or is not accessible."
            )
        response.raise_for_status()
