"""Compare simple regressors for the exploratory symptom score."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import joblib
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "responses_clean.csv"
MODEL_OUTPUT = PROJECT_ROOT / "models" / "eyeguard_ridge.joblib"

TARGET = "exploratory_symptom_score"
FEATURES = [
    "age_group",
    "screen_time_category",
    "sleep_category",
    "breaks_per_hour_category",
    "primary_device",
    "vision_correction",
]


def _group_identical_rows(features: pd.DataFrame, target: pd.Series) -> pd.Series:
    """Keep identical feature-and-target records in the same CV fold."""
    row_keys = [
        tuple(row)
        for row in pd.concat([features, target.rename(TARGET)], axis=1).itertuples(
            index=False, name=None
        )
    ]
    row_keys = pd.Series(row_keys, index=features.index, dtype="object")
    codes, _ = pd.factorize(row_keys, sort=True)
    return pd.Series(codes, index=features.index)


def _make_pipeline(estimator) -> Pipeline:
    preprocessing = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                FEATURES,
            )
        ],
        remainder="drop",
    )
    return Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("model", estimator),
        ]
    )


def _negative_clipped_mae(estimator, X: pd.DataFrame, y: pd.Series) -> float:
    predictions = estimator.predict(X)
    predictions = [min(15.0, max(0.0, float(value))) for value in predictions]
    return -float(mean_absolute_error(y, predictions))


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Prepared file not found: {INPUT_PATH}. Run prepare_data.py first."
        )

    data = pd.read_csv(INPUT_PATH)
    required = set(FEATURES + [TARGET, "duplicate_candidate"])
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Prepared file is missing columns: {sorted(missing)}")
    if data[FEATURES + [TARGET]].isna().any().any():
        raise ValueError("Model inputs or target contain blank values.")

    features = data[FEATURES].astype("string")
    target = pd.to_numeric(data[TARGET], errors="raise")
    groups = _group_identical_rows(features, target)
    group_count = int(groups.nunique())
    if group_count < 5:
        raise ValueError(
            "Five-fold group cross-validation needs at least five distinct "
            f"feature-and-score patterns; found {group_count}."
        )

    duplicate_group_count = int(groups.value_counts().gt(1).sum())
    cv = GroupKFold(n_splits=5)
    models = {
        "Mean baseline": _make_pipeline(DummyRegressor(strategy="mean")),
        "Ridge regression": _make_pipeline(Ridge(alpha=5.0)),
        "Random Forest": _make_pipeline(
            RandomForestRegressor(
                n_estimators=300,
                max_depth=5,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=1,
            )
        ),
    }
    ridge_importance: dict[str, list[float]] = {feature: [] for feature in FEATURES}
    metrics_by_model: dict[str, dict[str, float]] = {}

    print("Exploratory regression on the project-created symptom score")
    print(f"Responses retained: {len(data)}")
    print(f"Distinct feature-and-score groups: {group_count}")
    print(f"Repeated groups kept together during cross-validation: {duplicate_group_count}")
    print("Metrics use five folds. Lower MAE and RMSE indicate smaller prediction errors.")
    print("R-squared can be negative when a model performs worse than the fold mean.")
    print("\nModel                    MAE (mean ± SD)   RMSE (mean ± SD)   R² (mean ± SD)")

    for name, prototype in models.items():
        fold_results: list[tuple[float, float, float]] = []
        for fold_number, (train_indices, test_indices) in enumerate(
            cv.split(features, target, groups), start=1
        ):
            model = clone(prototype)
            X_train = features.iloc[train_indices]
            X_test = features.iloc[test_indices]
            y_train = target.iloc[train_indices]
            y_test = target.iloc[test_indices]

            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            predictions = [min(15.0, max(0.0, float(value))) for value in predictions]

            mae = mean_absolute_error(y_test, predictions)
            rmse = mean_squared_error(y_test, predictions) ** 0.5
            r2 = r2_score(y_test, predictions)
            fold_results.append((float(mae), float(rmse), float(r2)))

            if name == "Ridge regression":
                importance = permutation_importance(
                    model,
                    X_test,
                    y_test,
                    scoring=_negative_clipped_mae,
                    n_repeats=30,
                    random_state=42 + fold_number,
                    n_jobs=1,
                )
                for feature, value in zip(FEATURES, importance.importances_mean):
                    ridge_importance[feature].append(float(value))

        results = pd.DataFrame(fold_results, columns=["MAE", "RMSE", "R2"])
        metrics_by_model[name] = {
            "mae_mean": float(results["MAE"].mean()),
            "mae_sd": float(results["MAE"].std(ddof=0)),
            "rmse_mean": float(results["RMSE"].mean()),
            "rmse_sd": float(results["RMSE"].std(ddof=0)),
            "r2_mean": float(results["R2"].mean()),
            "r2_sd": float(results["R2"].std(ddof=0)),
        }
        print(
            f"{name:<24} "
            f"{results['MAE'].mean():5.2f} ± {results['MAE'].std(ddof=0):4.2f}       "
            f"{results['RMSE'].mean():5.2f} ± {results['RMSE'].std(ddof=0):4.2f}       "
            f"{results['R2'].mean():5.2f} ± {results['R2'].std(ddof=0):4.2f}"
        )

    print("\nRidge permutation importance on held-out folds")
    print("Feature                         Mean MAE increase   SD across folds   Positive folds")
    ordered_importance = sorted(
        ridge_importance.items(),
        key=lambda item: sum(item[1]) / len(item[1]),
        reverse=True,
    )
    for feature, values in ordered_importance:
        fold_mean = sum(values) / len(values)
        fold_sd = pd.Series(values).std(ddof=0)
        positive_folds = sum(value > 0 for value in values)
        print(
            f"{feature.replace('_', ' '):<32} "
            f"{fold_mean:8.3f}            {fold_sd:8.3f}          "
            f"{positive_folds}/5"
        )

    print(
        "\nThese results are exploratory. The target is not a validated clinical "
        "score, and the sample is small and concentrated in one student population."
    )
    print(
        "Permutation importance is the change in held-out MAE after shuffling one "
        "input. Positive values mean the fitted Ridge model relied on that input; "
        "they do not show cause and effect."
    )

    final_model = clone(models["Ridge regression"])
    final_model.fit(features, target)
    MODEL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": final_model,
            "features": FEATURES,
            "target": TARGET,
            "cv_metrics": metrics_by_model["Ridge regression"],
        },
        MODEL_OUTPUT,
    )
    print("\nSaved local demo model: models/eyeguard_ridge.joblib")


if __name__ == "__main__":
    main()
