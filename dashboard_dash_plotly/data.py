from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "survey_data_cleaned_reduced.csv"
COUNTRY_CENTROIDS_PATH = PROJECT_ROOT / "dashboard_dash_plotly" / "assets" / "country_centroids.csv"

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
AGE_SHORT_LABELS = {
    "Under 18 years old": "<18",
    "18-24 years old": "18-24",
    "25-34 years old": "25-34",
    "35-44 years old": "35-44",
    "45-54 years old": "45-54",
    "55-64 years old": "55-64",
    "65 years or older": "65+",
    "Prefer not to say": "Undeclared",
}
EXPERIENCE_BAND_ORDER = ["0-2 years", "3-5 years", "6-10 years", "11-15 years", "16+ years"]
REMOTE_WORK_LABELS = {
    "Remote": "Remote",
    "Hybrid (some remote, some in-person)": "Hybrid",
    "In-person": "In-person",
}
DEVTYPE_MACRO_GROUPS = {
    "Developer, full-stack": "Core software development",
    "Developer, back-end": "Core software development",
    "Developer, front-end": "Core software development",
    "Developer, desktop or enterprise applications": "Core software development",
    "Developer, mobile": "Core software development",
    "Developer, embedded applications or devices": "Core software development",
    "Developer, game or graphics": "Core software development",
    "Developer, QA or test": "Core software development",
    "Developer, AI": "Data, analytics & AI",
    "Data engineer": "Data, analytics & AI",
    "Data scientist or machine learning specialist": "Data, analytics & AI",
    "Data or business analyst": "Data, analytics & AI",
    "Scientist": "Data, analytics & AI",
    "DevOps specialist": "Infrastructure, cloud & operations",
    "Cloud infrastructure engineer": "Infrastructure, cloud & operations",
    "Engineer, site reliability": "Infrastructure, cloud & operations",
    "System administrator": "Infrastructure, cloud & operations",
    "Database administrator": "Infrastructure, cloud & operations",
    "Blockchain": "Infrastructure, cloud & operations",
    "Hardware Engineer": "Infrastructure, cloud & operations",
    "Engineering manager": "Leadership & product",
    "Senior Executive (C-Suite, VP, etc.)": "Leadership & product",
    "Project manager": "Leadership & product",
    "Product manager": "Leadership & product",
    "Research & Development role": "Research & education",
    "Academic researcher": "Research & education",
    "Educator": "Research & education",
    "Student": "Research & education",
    "Developer Experience": "Developer relations & experience",
    "Developer Advocate": "Developer relations & experience",
    "Security professional": "Security",
    "Designer": "Design & commercial",
    "Marketing or sales professional": "Design & commercial",
    "Other (please specify):": "Unspecified",
}
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
TECH_FAMILIES = {
    "Languages": {
        "label": "technology",
        "current": "LanguageHaveWorkedWith",
        "future": "LanguageWantToWorkWith",
        "description": "Programming, scripting, and markup languages developers use to build software.",
    },
    "Databases": {
        "label": "technology",
        "current": "DatabaseHaveWorkedWith",
        "future": "DatabaseWantToWorkWith",
        "description": "Database engines and persistence tools used to store and query application data.",
    },
    "Platforms": {
        "label": "technology",
        "current": "PlatformHaveWorkedWith",
        "future": "PlatformWantToWorkWith",
        "description": "Cloud, operating, and deployment platforms where developers run workloads.",
    },
    "Frameworks": {
        "label": "technology",
        "current": "WebframeHaveWorkedWith",
        "future": "WebframeWantToWorkWith",
        "description": "Web frameworks developers use to build user-facing and backend applications.",
    },
}


@lru_cache(maxsize=1)
def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["ConvertedCompYearly"] = pd.to_numeric(df["ConvertedCompYearly"], errors="coerce")
    df["WorkExp_num"] = pd.to_numeric(df["WorkExp"], errors="coerce")
    return df


@lru_cache(maxsize=1)
def load_country_centroids() -> pd.DataFrame:
    centroids = pd.read_csv(COUNTRY_CENTROIDS_PATH, usecols=["name", "latitude", "longitude"])
    return centroids.rename(columns={"name": "country_lookup"})


def filter_dataset(df: pd.DataFrame, ages: Iterable[str] | None, workstyles: Iterable[str] | None) -> pd.DataFrame:
    filtered = df.copy()
    selected_ages = list(ages or [])
    selected_workstyles = list(workstyles or [])
    if selected_ages:
        filtered = filtered[filtered["Age"].isin(selected_ages)]
    if selected_workstyles:
        filtered = filtered[filtered["RemoteWork"].isin(selected_workstyles)]
    return filtered


def observed_compensation(df: pd.DataFrame) -> pd.Series:
    salary = pd.to_numeric(df["ConvertedCompYearly"], errors="coerce").dropna()
    if salary.empty:
        return salary

    counts = salary.value_counts()
    dominant_value = counts.index[0]
    dominant_count = int(counts.iloc[0])
    dominant_share = dominant_count / len(salary)
    median_value = salary.median()
    looks_imputed = dominant_count >= 25 and dominant_share >= 0.15 and abs(float(dominant_value) - float(median_value)) < 0.01
    return salary[salary != dominant_value] if looks_imputed else salary


def build_kpis(full_df: pd.DataFrame, filtered_df: pd.DataFrame, countries_on_map: int) -> dict:
    full_salary = observed_compensation(full_df)
    filtered_salary = observed_compensation(filtered_df)
    return {
        "respondents_total": len(full_df),
        "respondents_filtered": len(filtered_df),
        "countries_total": full_df.loc[full_df["Country"] != "Nomadic", "Country"].nunique(),
        "countries_on_map": countries_on_map,
        "salary_total": float(full_salary.mean()) if not full_salary.empty else 0.0,
        "salary_filtered": float(filtered_salary.mean()) if not filtered_salary.empty else 0.0,
    }


def split_multiselect(series: pd.Series) -> pd.Series:
    cleaned = series.dropna().astype(str).str.strip()
    cleaned = cleaned[~cleaned.isin(["", "Not specified"])]
    return cleaned.str.split(";").explode().str.strip()


def top_multiselect_counts(df: pd.DataFrame, column: str, top_n: int, label: str) -> pd.DataFrame:
    counts = split_multiselect(df[column]).value_counts().head(top_n)
    result = counts.rename_axis(label).reset_index(name="count")
    result["share_pct"] = result["count"] / max(len(df), 1) * 100
    return result


def devtype_distribution(df: pd.DataFrame) -> pd.DataFrame:
    roles = split_multiselect(df["DevType"])
    mapped = pd.DataFrame({"role": roles})
    mapped["devtype_group"] = mapped["role"].map(DEVTYPE_MACRO_GROUPS).fillna("Unspecified")
    counts = mapped.groupby("devtype_group").size().sort_values(ascending=False)

    top_roles = (
        mapped.groupby(["devtype_group", "role"])
        .size()
        .reset_index(name="role_mentions")
        .sort_values(["devtype_group", "role_mentions"], ascending=[True, False])
        .groupby("devtype_group")["role"]
        .apply(lambda values: "; ".join(values.head(2)))
    )
    result = counts.rename_axis("devtype_group").reset_index(name="count")
    result["roles_included"] = result["devtype_group"].map(top_roles).fillna("")
    result["role_count"] = mapped.groupby("devtype_group")["role"].nunique().reindex(result["devtype_group"]).to_numpy()
    result["share_pct"] = result["count"] / max(result["count"].sum(), 1) * 100
    return result


def comparison_table(df: pd.DataFrame, current_col: str, future_col: str, top_n: int, label: str) -> pd.DataFrame:
    current = top_multiselect_counts(df, current_col, top_n * 2, label)
    future = top_multiselect_counts(df, future_col, top_n * 2, label)
    merged = current.merge(future, on=label, how="outer", suffixes=("_current", "_future")).fillna(0)
    merged["score"] = merged[["count_current", "count_future"]].max(axis=1)
    merged["delta"] = merged["count_future"] - merged["count_current"]
    return merged.sort_values(["score", "delta"], ascending=False).head(top_n).reset_index(drop=True)


def age_distribution(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["Age"].value_counts().reindex(AGE_ORDER, fill_value=0)
    result = counts.rename_axis("age").reset_index(name="count")
    result["age_short"] = result["age"].map(AGE_SHORT_LABELS)
    result["share_pct"] = result["count"] / max(len(df), 1) * 100
    return result[result["count"] > 0]


def age_education_distribution(df: pd.DataFrame) -> pd.DataFrame:
    top_levels = df["EdLevel"].value_counts().head(4).index.tolist()
    grouped = (
        df.assign(EducationGroup=df["EdLevel"].where(df["EdLevel"].isin(top_levels), "Other"))
        .groupby(["Age", "EducationGroup"])
        .size()
        .reset_index(name="count")
    )
    pivot = grouped.pivot(index="Age", columns="EducationGroup", values="count").fillna(0)
    pivot = pivot.reindex(AGE_ORDER, fill_value=0)
    pivot = pivot[pivot.sum(axis=1) > 0]
    normalized = pivot.div(pivot.sum(axis=1), axis=0) * 100
    normalized = normalized.reset_index().rename(columns={"Age": "age"})
    normalized["age_short"] = normalized["age"].map(AGE_SHORT_LABELS)
    return normalized


def compensation_records(df: pd.DataFrame) -> pd.DataFrame:
    salary = observed_compensation(df)
    records = df.loc[salary.index, ["RemoteWork", "WorkExp_num"]].copy()
    records["ConvertedCompYearly"] = salary
    records["workstyle"] = records["RemoteWork"].replace(REMOTE_WORK_LABELS)
    records["experience_band"] = pd.cut(
        records["WorkExp_num"],
        bins=[-0.1, 2, 5, 10, 15, float("inf")],
        labels=EXPERIENCE_BAND_ORDER,
    )
    return records.dropna(subset=["workstyle", "experience_band", "ConvertedCompYearly"])


def compensation_box_summary(records: pd.DataFrame) -> pd.DataFrame:
    summaries: list[dict] = []
    for workstyle in REMOTE_WORK_LABELS.values():
        for band in EXPERIENCE_BAND_ORDER:
            values = records.loc[
                (records["workstyle"] == workstyle) & (records["experience_band"] == band),
                "ConvertedCompYearly",
            ].dropna()
            if values.empty:
                continue

            q1 = values.quantile(0.25)
            q2 = values.quantile(0.50)
            q3 = values.quantile(0.75)
            iqr = q3 - q1
            summaries.append(
                {
                    "workstyle": workstyle,
                    "experience_band": band,
                    "experience_short": str(band).replace(" years", ""),
                    "q1": q1,
                    "q2": q2,
                    "q3": q3,
                    "lower": max(values.min(), q1 - 1.5 * iqr),
                    "upper": min(values.max(), q3 + 1.5 * iqr),
                    "mean": values.mean(),
                    "count": len(values),
                }
            )
    return pd.DataFrame(summaries)


def job_satisfaction_by_experience(df: pd.DataFrame) -> pd.DataFrame:
    records = df[["RemoteWork", "WorkExp_num", "JobSat"]].copy()
    records["JobSat_num"] = pd.to_numeric(records["JobSat"], errors="coerce")
    records["workstyle"] = records["RemoteWork"].replace(REMOTE_WORK_LABELS)
    records["experience_band"] = pd.cut(
        records["WorkExp_num"],
        bins=[-0.1, 2, 5, 10, 15, float("inf")],
        labels=EXPERIENCE_BAND_ORDER,
    )
    records = records.dropna(subset=["workstyle", "experience_band", "JobSat_num"])
    if records.empty:
        return pd.DataFrame(columns=["workstyle", "experience_band", "experience_short", "mean", "median", "count"])

    summary = (
        records.groupby(["workstyle", "experience_band"], observed=False)["JobSat_num"]
        .agg(mean="mean", median="median", count="size")
        .reset_index()
    )
    summary["experience_short"] = summary["experience_band"].astype(str).str.replace(" years", "", regex=False)
    return summary


def country_map_distribution(df: pd.DataFrame, top_n: int | None) -> pd.DataFrame:
    counts = df.loc[df["Country"] != "Nomadic", "Country"].value_counts()
    denominator = max(int(counts.sum()), 1)
    if top_n is not None:
        counts = counts.head(top_n)
    countries = counts.rename_axis("country").reset_index(name="count")
    countries["share_pct"] = countries["count"] / denominator * 100
    countries["country_lookup"] = countries["country"].replace(COUNTRY_NAME_ALIASES)
    merged = countries.merge(load_country_centroids(), on="country_lookup", how="left")
    return merged.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)
