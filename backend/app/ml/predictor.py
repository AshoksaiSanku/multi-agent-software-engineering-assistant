from functools import lru_cache

import joblib
import pandas as pd

from app.core.config import settings
from app.ml.training import FEATURES, train_models


class ModelRegistry:
    def __init__(self) -> None:
        self.bug_path = settings.ml_model_path / "bug_prediction.joblib"
        self.quality_path = settings.ml_model_path / "quality_prediction.joblib"

    def ensure_ready(self) -> None:
        if not self.bug_path.exists() or not self.quality_path.exists():
            train_models(settings.ml_model_path)

    def predict(self, features: dict[str, float]) -> tuple[float, float, list[str]]:
        self.ensure_ready()
        frame = pd.DataFrame([features], columns=FEATURES)
        bug_model = joblib.load(self.bug_path)
        quality_model = joblib.load(self.quality_path)
        probability = float(bug_model.predict_proba(frame)[0][1])
        score = max(0.0, min(100.0, float(quality_model.predict(frame)[0])))
        return round(probability, 4), round(score, 2), recommendations(features, probability)


def recommendations(features: dict[str, float], probability: float) -> list[str]:
    suggestions: list[str] = []
    if features["cyclomatic_complexity"] > 18:
        suggestions.append("Split high-complexity functions and add branch-focused tests.")
    if features["file_size"] > 700:
        suggestions.append("Extract cohesive modules to reduce file size and review surface.")
    if features["dependency_count"] > 14:
        suggestions.append("Review dependency boundaries and introduce narrow interfaces.")
    if features["commit_frequency"] > 25:
        suggestions.append("Protect this hotspot with CI checks and ownership review.")
    if probability > 0.65:
        suggestions.append("Prioritize integration tests and static security scanning.")
    return suggestions or ["Maintain current structure and continue monitoring code churn."]


@lru_cache
def model_registry() -> ModelRegistry:
    return ModelRegistry()

