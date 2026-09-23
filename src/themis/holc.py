import geopandas as gpd
import pandas as pd

HOLC_URL = (
    "https://raw.githubusercontent.com/americanpanorama/"
    "mapping-inequality-census-crosswalk/main/"
    "MIv3Areas_2020TractCrosswalk.geojson"
)

GRADE_MAP = {"A": 0, "B": 1, "C": 2, "D": 3}

_KEEP_COLS = [
    "area_id",
    "GEOID",
    "GISJOIN",
    "grade",
    "pct_tract",
    "calc_area",
    "city",
    "state",
    "label",
    "res",
    "com",
    "ind",
]


def load_raw(url: str = HOLC_URL) -> gpd.GeoDataFrame:
    """Download the HOLC-to-census-tract crosswalk GeoJSON."""
    return gpd.read_file(url)


_REQUIRED_COLS = {"GEOID", "grade", "pct_tract"}


def extract_dominant(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """One row per GEOID with the highest-coverage HOLC grade.

    Raises ValueError if GEOID, grade, or pct_tract columns are missing.
    """
    missing = _REQUIRED_COLS - set(gdf.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {sorted(missing)}")

    cols = [c for c in _KEEP_COLS if c in gdf.columns]
    df = gdf[cols].copy()
    df = df[df["grade"].isin(GRADE_MAP)]
    df = df.sort_values(["GEOID", "pct_tract"], ascending=[True, False])
    df = df.drop_duplicates(subset="GEOID", keep="first").copy()
    df["redlining_score"] = df["grade"].map(GRADE_MAP)
    return df.reset_index(drop=True)
