from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

from themis.adapters import BlackBoxAuditor


@pytest.fixture
def mock_model():
    model = MagicMock()
    model.predict_proba.return_value = np.array([[0.3, 0.7], [0.8, 0.2]])
    return model


@pytest.fixture
def auditor(mock_model):
    return BlackBoxAuditor(mock_model, feature_names=["income", "loan_amount"])


def test_predict_proba_strips_extra_columns(auditor, mock_model):
    df = pd.DataFrame(
        {"income": [50000, 60000], "loan_amount": [200000, 150000], "extra": [1, 2]}
    )
    auditor.predict_proba(df)
    called_X = mock_model.predict_proba.call_args[0][0]
    assert list(called_X.columns) == ["income", "loan_amount"]


def test_predict_proba_raises_on_missing_column(auditor):
    df = pd.DataFrame({"income": [50000]})
    with pytest.raises(ValueError, match="Missing required columns"):
        auditor.predict_proba(df)


def test_predict_returns_binary_array(auditor):
    df = pd.DataFrame({"income": [50000, 60000], "loan_amount": [200000, 150000]})
    preds = auditor.predict(df)
    assert set(preds).issubset({0, 1})


def test_predict_threshold_is_0_5(auditor, mock_model):
    mock_model.predict_proba.return_value = np.array([[0.4, 0.6], [0.6, 0.4]])
    df = pd.DataFrame({"income": [1, 2], "loan_amount": [1, 2]})
    preds = auditor.predict(df)
    assert preds[0] == 1
    assert preds[1] == 0


def test_feature_names_stored_correctly(auditor):
    assert auditor.feature_names == ["income", "loan_amount"]
