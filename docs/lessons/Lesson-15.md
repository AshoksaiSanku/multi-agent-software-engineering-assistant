# Lesson-15: Machine Learning Training, Metrics, Prediction API

## Objective

Implement ML model training, metric estimation, prediction, and history.

## Files Created

```text
backend/app/ml/__init__.py
backend/app/ml/training.py
backend/app/ml/predictor.py
backend/app/ml/metrics.py
backend/app/api/routes/ml.py
backend/scripts/train_models.py
```

## Knowledge Required

- **Feature**: Input value for ML model.
- **Classifier**: Model that predicts categories/probabilities.
- **Regressor**: Model that predicts numbers.
- **XGBoost**: Gradient-boosting ML library.
- **RandomForestRegressor**: scikit-learn regression model using many decision trees.
- **ROC-AUC**: Classification quality metric.
- **MAE**: Mean absolute error for regression.
- **joblib**: Saves/loads model files.

## Data Flow

Metrics -> DataFrame -> bug model predicts probability -> quality model predicts score -> recommendations generated -> prediction saved.

## Common Mistakes

- Treating synthetic model as production-grade.
- Mismatched feature order.
- Blocking event loop during prediction.

## Verification

Call `/api/v1/ml/predict` and verify probability is between 0 and 1.

