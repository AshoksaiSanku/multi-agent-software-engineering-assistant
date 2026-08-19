from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, roc_auc_score
from xgboost import XGBClassifier


FEATURES = ["cyclomatic_complexity", "file_size", "dependency_count", "commit_frequency"]


def sample_training_data(rows: int = 1400) -> pd.DataFrame:
    """Create repeatable seed training data until a team supplies labeled history."""
    rng = np.random.default_rng(42)
    frame = pd.DataFrame(
        {
            "cyclomatic_complexity": rng.gamma(2.5, 6, rows),
            "file_size": rng.gamma(2.0, 210, rows),
            "dependency_count": rng.poisson(7, rows),
            "commit_frequency": rng.gamma(2.0, 4, rows),
        }
    )
    risk = (
        0.09 * frame["cyclomatic_complexity"]
        + 0.002 * frame["file_size"]
        + 0.12 * frame["dependency_count"]
        + 0.045 * frame["commit_frequency"]
        + rng.normal(0, 0.9, rows)
    )
    frame["bug_prone"] = (risk > np.quantile(risk, 0.62)).astype(int)
    frame["maintainability"] = np.clip(
        100
        - 1.25 * frame["cyclomatic_complexity"]
        - 0.018 * frame["file_size"]
        - 1.1 * frame["dependency_count"]
        + rng.normal(0, 4, rows),
        0,
        100,
    )
    return frame


def train_models(output_dir: Path, csv_path: Path | None = None) -> dict[str, float]:
    output_dir.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(csv_path) if csv_path else sample_training_data()
    train, test = train_test_split(data, test_size=0.2, random_state=42)
    bug_model = XGBClassifier(
        n_estimators=160,
        max_depth=4,
        learning_rate=0.06,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
    )
    quality_model = RandomForestRegressor(n_estimators=150, random_state=42)
    bug_model.fit(train[FEATURES], train["bug_prone"])
    quality_model.fit(train[FEATURES], train["maintainability"])
    probabilities = bug_model.predict_proba(test[FEATURES])[:, 1]
    quality = quality_model.predict(test[FEATURES])
    metrics = {
        "bug_auc": round(float(roc_auc_score(test["bug_prone"], probabilities)), 4),
        "maintainability_mae": round(
            float(mean_absolute_error(test["maintainability"], quality)), 4
        ),
    }
    joblib.dump(bug_model, output_dir / "bug_prediction.joblib")
    joblib.dump(quality_model, output_dir / "quality_prediction.joblib")
    joblib.dump({"features": FEATURES, "metrics": metrics}, output_dir / "metadata.joblib")
    return metrics

