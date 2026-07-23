from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd


AGE_ORDER = [
    "Under 18 years old",
    "18-24 years old",
    "25-34 years old",
    "35-44 years old",
    "45-54 years old",
    "55-64 years old",
    "65 years or older",
    "Prefer not to say",
]

AGE_MID_MAP = {
    "Under 18 years old": 17,
    "18-24 years old": 21,
    "25-34 years old": 29.5,
    "35-44 years old": 39.5,
    "45-54 years old": 49.5,
    "55-64 years old": 59.5,
    "65 years or older": 70,
    "Prefer not to say": None,
}
EXPERIENCE_BAND_ORDER = [
    "0-2 years",
    "3-5 years",
    "6-10 years",
    "11-15 years",
    "16+ years",
]
REMOTE_WORK_LABELS = {
    "Remote": "Remote",
    "Hybrid (some remote, some in-person)": "Hybrid",
    "In-person": "In-person",
}
DOMINANT_IMPUTED_SALARY_SHARE = 0.15
DOMINANT_IMPUTED_SALARY_MIN_COUNT = 25

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COUNTRY_CENTROIDS_PATH = PROJECT_ROOT / "dashboard_panel_bokeh" / "assets" / "country_centroids.csv"
COUNTRY_NAME_ALIASES = {
    "Brunei Darussalam": "Brunei",
    "Congo, Republic of the...": "Congo [Republic]",
    "Democratic Republic of the Congo": "Congo [DRC]",
    "Hong Kong (S.A.R.)": "Hong Kong",
    "Iran, Islamic Republic of...": "Iran",
    "Myanmar": "Myanmar [Burma]",
    "Palestine": "Palestinian Territories",
    "Republic of Korea": "South Korea",
    "Republic of Moldova": "Moldova",
    "Republic of North Macedonia": "Macedonia [FYROM]",
    "Russian Federation": "Russia",
    "Syrian Arab Republic": "Syria",
    "United Republic of Tanzania": "Tanzania",
    "Venezuela, Bolivarian Republic of...": "Venezuela",
    "Viet Nam": "Vietnam",
}


def _clean_education_level(value: object) -> str:
    if pd.isna(value):
        return "Not specified"

    text = str(value).replace("ï¿½", "").replace("�", "").strip()
    lower = text.lower()

    if "bachelor" in lower:
        return "Bachelors degree"
    if "master" in lower:
        return "Masters degree"
    if "professional degree" in lower:
        return "Professional degree"
    if "associate degree" in lower:
        return "Associate degree"
    if "primary/elementary" in lower or lower == "primary school":
        return "Primary school"
    if "secondary school" in lower:
        return "Secondary school"
    if "some college" in lower:
        return "Some college/university study"
    if "something else" in lower:
        return "Something else"
    return text or "Not specified"


def load_dataset(dataset_path: Path) -> pd.DataFrame:
    df = pd.read_csv(dataset_path)
    df = df.copy()
    df["EdLevel"] = df["EdLevel"].map(_clean_education_level)
    df["Age_num"] = pd.to_numeric(df["Age"].map(AGE_MID_MAP), errors="coerce")
    df["WorkExp_num"] = pd.to_numeric(df["WorkExp"], errors="coerce")
    return df


@lru_cache(maxsize=1)
def load_country_centroids() -> pd.DataFrame:
    centroids = pd.read_csv(COUNTRY_CENTROIDS_PATH, usecols=["name", "latitude", "longitude"])
    centroids = centroids.rename(columns={"name": "country_lookup"})
    centroids["country_lookup"] = centroids["country_lookup"].astype(str).str.strip()
    return centroids


def split_multiselect(series: pd.Series) -> pd.Series:
    cleaned = series.dropna().astype(str).str.strip()
    cleaned = cleaned[~cleaned.isin(["", "Not specified"])]
    return cleaned.str.split(";").explode().str.strip()


def filter_dataset(
    df: pd.DataFrame,
    selected_ages: Iterable[str],
    selected_remote_modes: Iterable[str],
    country_scope: str,
    country_top_n: int = 10,
) -> pd.DataFrame:
    filtered = df.copy()

    selected_ages = list(selected_ages)
    selected_remote_modes = list(selected_remote_modes)

    if selected_ages:
        filtered = filtered[filtered["Age"].isin(selected_ages)]

    if selected_remote_modes:
        filtered = filtered[filtered["RemoteWork"].isin(selected_remote_modes)]

    if country_scope == "Top N countries":
        top_countries = df.loc[df["Country"] != "Nomadic", "Country"].value_counts().head(country_top_n).index.tolist()
        filtered = filtered[filtered["Country"].isin(top_countries)]

    return filtered


def metric_column(metric_mode: str) -> str:
    return "share_pct" if metric_mode == "Share of respondents" else "count"


def top_multiselect_counts(
    df: pd.DataFrame,
    column: str,
    top_n: int,
    label: str,
) -> pd.DataFrame:
    counts = split_multiselect(df[column]).value_counts().head(top_n)
    result = counts.rename_axis(label).reset_index(name="count")
    denominator = max(len(df), 1)
    result["share_pct"] = (result["count"] / denominator * 100).round(2)
    result["rank"] = range(1, len(result) + 1)
    return result


def build_comparison_table(
    df: pd.DataFrame,
    current_column: str,
    future_column: str,
    label: str,
    top_n: int,
) -> pd.DataFrame:
    current_counts = top_multiselect_counts(df, current_column, top_n * 2, label)
    future_counts = top_multiselect_counts(df, future_column, top_n * 2, label)

    merged = current_counts.merge(
        future_counts,
        on=label,
        how="outer",
        suffixes=("_current", "_future"),
    ).fillna(0)

    merged["delta_count"] = merged["count_future"] - merged["count_current"]
    merged["delta_share_pct"] = (merged["share_pct_future"] - merged["share_pct_current"]).round(2)
    merged["comparison_score"] = merged[["count_current", "count_future"]].max(axis=1)
    merged = merged.sort_values(["comparison_score", "delta_count"], ascending=False).head(top_n).reset_index(drop=True)
    return merged


def top_country_distribution(df: pd.DataFrame, top_n: Optional[int] = 10) -> pd.DataFrame:
    counts = df.loc[df["Country"] != "Nomadic", "Country"].value_counts()
    denominator = max(int(counts.sum()), 1)
    if top_n is not None:
        counts = counts.head(top_n)
    result = counts.rename_axis("country").reset_index(name="count")
    result["share_pct"] = (result["count"] / denominator * 100).round(2)
    return result


def country_map_distribution(df: pd.DataFrame, top_n: Optional[int] = 10) -> pd.DataFrame:
    countries = top_country_distribution(df, top_n=top_n).copy()
    countries["country_lookup"] = countries["country"].replace(COUNTRY_NAME_ALIASES)
    countries = countries[countries["country"] != "Nomadic"]
    merged = countries.merge(load_country_centroids(), on="country_lookup", how="left")
    return merged.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)


def _experience_band_series(work_exp: pd.Series) -> pd.Series:
    return pd.cut(
        pd.to_numeric(work_exp, errors="coerce"),
        bins=[-0.1, 2, 5, 10, 15, float("inf")],
        labels=EXPERIENCE_BAND_ORDER,
    )


def _observed_compensation_series(df: pd.DataFrame) -> pd.Series:
    """Remove the dominant median-imputed compensation spike from salary views."""
    salary = pd.to_numeric(df["ConvertedCompYearly"], errors="coerce").dropna()
    if salary.empty:
        return salary

    counts = salary.value_counts()
    dominant_value = counts.index[0]
    dominant_count = int(counts.iloc[0])
    dominant_share = dominant_count / len(salary)
    median_value = salary.median()
    looks_imputed = (
        dominant_count >= DOMINANT_IMPUTED_SALARY_MIN_COUNT
        and dominant_share >= DOMINANT_IMPUTED_SALARY_SHARE
        and abs(float(dominant_value) - float(median_value)) < 0.01
    )
    if not looks_imputed:
        return salary

    return salary[salary != dominant_value]


def _observed_compensation_df(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    observed_salary = _observed_compensation_series(df)
    result = df.loc[observed_salary.index, columns].copy()
    result["ConvertedCompYearly"] = observed_salary
    return result


def salary_remote_experience_box_summary(df: pd.DataFrame) -> pd.DataFrame:
    base = (
        _observed_compensation_df(df, ["RemoteWork", "WorkExp_num", "ConvertedCompYearly"])
        .dropna(subset=["RemoteWork", "WorkExp_num", "ConvertedCompYearly"])
        .copy()
    )
    base["experience_band"] = _experience_band_series(base["WorkExp_num"])
    base["remote_label"] = base["RemoteWork"].replace(REMOTE_WORK_LABELS)
    base = base.dropna(subset=["experience_band", "remote_label"])

    remote_order = [
        REMOTE_WORK_LABELS[value]
        for value in df["RemoteWork"].value_counts().index.tolist()
        if value in REMOTE_WORK_LABELS
    ]

    summaries: List[dict] = []
    for remote_label in remote_order:
        for experience_band in EXPERIENCE_BAND_ORDER:
            values = base.loc[
                (base["remote_label"] == remote_label) & (base["experience_band"] == experience_band),
                "ConvertedCompYearly",
            ].dropna()
            if values.empty:
                continue

            q1 = values.quantile(0.25)
            q2 = values.quantile(0.50)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            upper = min(values.max(), q3 + 1.5 * iqr)
            lower = max(values.min(), q1 - 1.5 * iqr)

            summaries.append(
                {
                    "remote_label": remote_label,
                    "experience_band": experience_band,
                    "factor": (remote_label, experience_band),
                    "q1": q1,
                    "q2": q2,
                    "q3": q3,
                    "upper": upper,
                    "lower": lower,
                    "mean": values.mean(),
                    "count": len(values),
                }
            )

    return pd.DataFrame(summaries)


def age_distribution(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["Age"].value_counts().reindex(AGE_ORDER, fill_value=0)
    result = counts.rename_axis("age").reset_index(name="count")
    result["share_pct"] = (result["count"] / max(len(df), 1) * 100).round(2)
    return result


def education_distribution(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["EdLevel"].value_counts().head(8)
    result = counts.rename_axis("education_level").reset_index(name="count")
    result["share_pct"] = (result["count"] / max(len(df), 1) * 100).round(2)
    return result


def age_education_distribution(df: pd.DataFrame) -> pd.DataFrame:
    top_education_levels = df["EdLevel"].value_counts().head(4).index.tolist()

    grouped = (
        df.assign(
            EducationGroup=df["EdLevel"].where(df["EdLevel"].isin(top_education_levels), "Other")
        )
        .groupby(["Age", "EducationGroup"])
        .size()
        .reset_index(name="count")
    )

    pivot = grouped.pivot(index="Age", columns="EducationGroup", values="count").fillna(0)
    pivot = pivot.reindex(AGE_ORDER, fill_value=0)
    pivot = pivot[pivot.sum(axis=1) > 0]
    return pivot.reset_index()


def salary_by_remote_summary(df: pd.DataFrame) -> pd.DataFrame:
    summaries: List[dict] = []
    order = df["RemoteWork"].value_counts().index.tolist()

    for category in order:
        values = df.loc[df["RemoteWork"] == category, "ConvertedCompYearly"].dropna()
        if values.empty:
            continue

        q1 = values.quantile(0.25)
        q2 = values.quantile(0.50)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        upper = min(values.max(), q3 + 1.5 * iqr)
        lower = max(values.min(), q1 - 1.5 * iqr)

        summaries.append(
            {
                "category": category,
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "upper": upper,
                "lower": lower,
                "mean": values.mean(),
                "count": len(values),
            }
        )

    return pd.DataFrame(summaries)


def age_workexp_sample(df: pd.DataFrame, sample_size: int = 3000) -> pd.DataFrame:
    scatter_df = df[["Age_num", "WorkExp", "Age", "RemoteWork"]].dropna()
    if len(scatter_df) > sample_size:
        scatter_df = scatter_df.sample(sample_size, random_state=42)
    return scatter_df


def build_kpis(df: pd.DataFrame) -> dict:
    observed_salary = _observed_compensation_series(df) if not df.empty else pd.Series(dtype="float64")
    median_salary = float(observed_salary.median()) if not observed_salary.empty else 0.0
    average_salary = float(observed_salary.mean()) if not observed_salary.empty else 0.0
    countries = df.loc[df["Country"] != "Nomadic", "Country"].nunique()
    return {
        "respondents": int(len(df)),
        "countries": int(countries),
        "median_salary": median_salary,
        "average_salary": average_salary,
    }
