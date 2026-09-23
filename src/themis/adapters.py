from __future__ import annotations

from typing import Protocol

import numpy as np
import pandas as pd


class PredictProbaProtocol(Protocol):
    def predict_proba(self, X) -> np.ndarray: ...


class BlackBoxAuditor:
    """Wrap any `predict_proba`-compatible model for auditing without internals."""

    def __init__(self, model: PredictProbaProtocol, feature_names: list[str]):
        self._model = model
        self.feature_names = list(feature_names)

    def validate_schema(self, df: pd.DataFrame) -> None:
        missing = set(self.feature_names) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        self.validate_schema(X)
        return self._model.predict_proba(X[self.feature_names])

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        proba = self.predict_proba(X)
        return (proba[:, 1] >= 0.5).astype(int)
