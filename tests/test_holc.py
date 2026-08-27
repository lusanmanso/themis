"""Smoke tests for the themis package."""

import geopandas as gpd
import pandas as pd
import pytest

from themis import extract_dominant, load_raw
from themis.holc import GRADE_MAP


def test_imports():
    """Package exposes the public API."""
    assert callable(load_raw)
    assert callable(extract_dominant)


def test_grade_map():
    """Grade map has expected structure."""
    assert GRADE_MAP == {"A": 0, "B": 1, "C": 2, "D": 3}


def test_extract_dominant_on_synthetic_data():
    """extract_dominant keeps the highest pct_tract per GEOID."""
    data = {
        "GEOID": ["11001", "11001", "11002"],
        "grade": ["A", "C", "D"],
        "pct_tract": [0.3, 0.7, 0.9],
        "area_id": [1, 2, 3],
        "city": ["DC", "DC", "DC"],
        "state": ["DC", "DC", "DC"],
    }
    gdf = gpd.GeoDataFrame(data)

    result = extract_dominant(gdf)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    # GEOID 11001 should keep grade C (pct_tract 0.7 > 0.3)
    row_11001 = result[result["GEOID"] == "11001"].iloc[0]
    assert row_11001["grade"] == "C"
    assert row_11001["redlining_score"] == 2
    # GEOID 11002 should keep grade D
    row_11002 = result[result["GEOID"] == "11002"].iloc[0]
    assert row_11002["grade"] == "D"
    assert row_11002["redlining_score"] == 3


def test_extract_dominant_drops_ungraded():
    """Rows with grades not in GRADE_MAP are excluded."""
    data = {
        "GEOID": ["11001", "11002"],
        "grade": ["A", "E"],  # E is not a valid HOLC grade
        "pct_tract": [0.5, 0.8],
    }
    gdf = gpd.GeoDataFrame(data)

    result = extract_dominant(gdf)

    assert len(result) == 1
    assert result.iloc[0]["GEOID"] == "11001"


def test_extract_dominant_missing_columns():
    """extract_dominant raises ValueError when required columns are missing."""
    data = {
        "GEOID": ["11001"],
        "pct_tract": [0.5],
        # "grade" is missing
    }
    gdf = gpd.GeoDataFrame(data)

    with pytest.raises(ValueError, match="missing required columns"):
        extract_dominant(gdf)
