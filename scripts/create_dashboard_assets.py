from pathlib import Path
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
PRIMARY_INPUT_FILE = DATA_DIR / "cleaned_outputs" / "survey_data_cleaned_reduced.csv"
FALLBACK_INPUT_FILE = DATA_DIR / "survey_data_updated.csv"
OUTPUT_DIR = DATA_DIR / "dashboard_assets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def split_multiselect(series: pd.Series) -> pd.Series:
    cleaned = series.dropna().astype(str).str.strip()
    cleaned = cleaned[~cleaned.isin(["", "Not specified"])]
    return cleaned.str.split(";").explode().str.strip()


def top_counts(df: pd.DataFrame, column: str, top_n: int = 10, label: str = "item") -> pd.DataFrame:
    counts = (
        split_multiselect(df[column])
        .value_counts()
        .head(top_n)
        .rename_axis(label)
        .reset_index(name="count")
    )
    counts["rank"] = range(1, len(counts) + 1)
    counts["share_pct"] = (counts["count"] / counts["count"].sum() * 100).round(2)
    return counts


def bubble_table(df: pd.DataFrame, column: str, label: str) -> pd.DataFrame:
    counts = top_counts(df, column, top_n=10, label=label).copy()
    counts["x"] = counts["rank"]
    counts["y"] = counts["count"]
    counts["bubble_size"] = counts["count"]
    return counts[[label, "rank", "count", "share_pct", "x", "y", "bubble_size"]]


def save_csv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(OUTPUT_DIR / name, index=False)


def build_wide_top10(
    left: pd.DataFrame,
    left_dim: str,
    left_prefix: str,
    right: pd.DataFrame,
    right_dim: str,
    right_prefix: str,
    third: pd.DataFrame,
    third_dim: str,
    third_prefix: str,
    fourth: pd.DataFrame,
    fourth_dim: str,
    fourth_prefix: str,
) -> pd.DataFrame:
    wide = pd.DataFrame({"rank": range(1, 11)})
    for data, dim_col, prefix in [
        (left, left_dim, left_prefix),
        (right, right_dim, right_prefix),
        (third, third_dim, third_prefix),
        (fourth, fourth_dim, fourth_prefix),
    ]:
        temp = data.copy()
        wide = wide.merge(
            temp.rename(
                columns={
                    dim_col: prefix,
                    "count": f"{prefix}_count",
                    "share_pct": f"{prefix}_share_pct",
                }
            )[
                ["rank", prefix, f"{prefix}_count", f"{prefix}_share_pct"]
            ],
            on="rank",
            how="left",
        )
    return wide


def build_demographics_wide(
    age_counts: pd.DataFrame,
    country_counts: pd.DataFrame,
    edlevel_counts: pd.DataFrame,
    age_edlevel: pd.DataFrame,
) -> pd.DataFrame:
    max_rows = max(len(age_counts), len(country_counts), len(edlevel_counts), len(age_edlevel))
    wide = pd.DataFrame({"row_id": range(1, max_rows + 1)})

    age_df = age_counts.copy().reset_index(drop=True)
    age_df.insert(0, "row_id", range(1, len(age_df) + 1))
    age_df = age_df.rename(columns={"age": "demographics_age", "respondent_count": "demographics_age_count"})

    country_df = country_counts.copy().reset_index(drop=True)
    country_df.insert(0, "row_id", range(1, len(country_df) + 1))
    country_df = country_df.rename(columns={"country": "demographics_country", "respondent_count": "demographics_country_count"})

    ed_df = edlevel_counts.copy().reset_index(drop=True)
    ed_df.insert(0, "row_id", range(1, len(ed_df) + 1))
    ed_df = ed_df.rename(
        columns={
            "education_level": "demographics_education_level",
            "respondent_count": "demographics_education_count",
            "line_value": "demographics_education_line_value",
        }
    )

    stacked_df = age_edlevel.copy().reset_index(drop=True)
    stacked_df.insert(0, "row_id", range(1, len(stacked_df) + 1))
    stacked_df = stacked_df.rename(
        columns={
            "age": "stacked_age",
            "education_level": "stacked_education_level",
            "respondent_count": "stacked_respondent_count",
        }
    )

    for temp in [age_df, country_df, ed_df, stacked_df]:
        wide = wide.merge(temp, on="row_id", how="left")

    return wide


def main() -> None:
    input_file = PRIMARY_INPUT_FILE if PRIMARY_INPUT_FILE.exists() else FALLBACK_INPUT_FILE
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found. Checked: {PRIMARY_INPUT_FILE} and {FALLBACK_INPUT_FILE}")

    df = pd.read_csv(input_file)

    current_language = top_counts(df, "LanguageHaveWorkedWith", label="language")
    current_database = top_counts(df, "DatabaseHaveWorkedWith", label="database")
    current_platform = top_counts(df, "PlatformHaveWorkedWith", label="platform")
    current_webframe = bubble_table(df, "WebframeHaveWorkedWith", label="web_framework")

    future_language = top_counts(df, "LanguageWantToWorkWith", label="language")
    future_database = top_counts(df, "DatabaseWantToWorkWith", label="database")
    future_platform = top_counts(df, "PlatformWantToWorkWith", label="platform")
    future_webframe = bubble_table(df, "WebframeWantToWorkWith", label="web_framework")

    age_counts = (
        df["Age"]
        .dropna()
        .loc[lambda s: ~s.astype(str).isin(["", "Not specified"])]
        .value_counts()
        .rename_axis("age")
        .reset_index(name="respondent_count")
    )

    country_counts = (
        df["Country"]
        .dropna()
        .loc[lambda s: ~s.astype(str).isin(["", "Not specified"])]
        .value_counts()
        .rename_axis("country")
        .reset_index(name="respondent_count")
    )

    edlevel_counts = (
        df["EdLevel"]
        .dropna()
        .loc[lambda s: ~s.astype(str).isin(["", "Not specified"])]
        .value_counts()
        .rename_axis("education_level")
        .reset_index(name="respondent_count")
    )
    edlevel_counts["line_value"] = edlevel_counts["respondent_count"]

    age_edlevel = (
        df.loc[
            df["Age"].notna()
            & df["EdLevel"].notna()
            & ~df["Age"].astype(str).isin(["", "Not specified"])
            & ~df["EdLevel"].astype(str).isin(["", "Not specified"]),
            ["Age", "EdLevel"],
        ]
        .value_counts()
        .rename("respondent_count")
        .reset_index()
        .rename(columns={"Age": "age", "EdLevel": "education_level"})
    )

    current_technologies_grouped = build_wide_top10(
        current_language,
        "language",
        "current_language",
        current_database,
        "database",
        "current_database",
        current_platform,
        "platform",
        "current_platform",
        current_webframe,
        "web_framework",
        "current_web_framework",
    )

    future_technologies_grouped = build_wide_top10(
        future_language,
        "language",
        "future_language",
        future_database,
        "database",
        "future_database",
        future_platform,
        "platform",
        "future_platform",
        future_webframe,
        "web_framework",
        "future_web_framework",
    )

    demographics_grouped = build_demographics_wide(age_counts, country_counts, edlevel_counts, age_edlevel)

    save_csv(current_language, "current_top10_languages_used.csv")
    save_csv(current_database, "current_top10_databases_used.csv")
    save_csv(current_platform, "current_top10_platforms_used.csv")
    save_csv(current_webframe, "current_top10_webframeworks_used_bubble.csv")

    save_csv(future_language, "future_top10_languages_desired.csv")
    save_csv(future_database, "future_top10_databases_desired.csv")
    save_csv(future_platform, "future_top10_platforms_desired.csv")
    save_csv(future_webframe, "future_top10_webframeworks_desired_bubble.csv")

    save_csv(age_counts, "demographics_respondents_by_age.csv")
    save_csv(country_counts, "demographics_respondent_count_by_country.csv")
    save_csv(edlevel_counts, "demographics_distribution_by_education_level.csv")
    save_csv(age_edlevel, "demographics_respondent_count_by_age_and_education.csv")
    save_csv(current_technologies_grouped, "current_technologies_grouped.csv")
    save_csv(future_technologies_grouped, "future_technologies_grouped.csv")
    save_csv(demographics_grouped, "demographics_grouped.csv")

    summary = pd.DataFrame(
        [
            {"file": str(input_file.relative_to(ROOT_DIR)).replace("\\", "/"), "rows": len(df), "purpose": "Source dataset used to generate all auxiliary files"},
            {"file": "current_top10_languages_used.csv", "rows": len(current_language), "purpose": "Current Technology Usage - Top 10 Languages Used"},
            {"file": "current_top10_databases_used.csv", "rows": len(current_database), "purpose": "Current Technology Usage - Top 10 Databases Used"},
            {"file": "current_top10_platforms_used.csv", "rows": len(current_platform), "purpose": "Current Technology Usage - Top 10 Platforms Used"},
            {"file": "current_top10_webframeworks_used_bubble.csv", "rows": len(current_webframe), "purpose": "Current Technology Usage - Top 10 Web Frameworks Used"},
            {"file": "future_top10_languages_desired.csv", "rows": len(future_language), "purpose": "Future Technology Trends - Top 10 Languages Desired Next Year"},
            {"file": "future_top10_databases_desired.csv", "rows": len(future_database), "purpose": "Future Technology Trends - Top 10 Databases Desired Next Year"},
            {"file": "future_top10_platforms_desired.csv", "rows": len(future_platform), "purpose": "Future Technology Trends - Top 10 Desired Platforms"},
            {"file": "future_top10_webframeworks_desired_bubble.csv", "rows": len(future_webframe), "purpose": "Future Technology Trends - Top 10 Desired Web Frameworks"},
            {"file": "demographics_respondents_by_age.csv", "rows": len(age_counts), "purpose": "Demographics - Respondents by Age"},
            {"file": "demographics_respondent_count_by_country.csv", "rows": len(country_counts), "purpose": "Demographics - Respondent Count by Country"},
            {"file": "demographics_distribution_by_education_level.csv", "rows": len(edlevel_counts), "purpose": "Demographics - Respondent Distribution by Education Level"},
            {"file": "demographics_respondent_count_by_age_and_education.csv", "rows": len(age_edlevel), "purpose": "Demographics - Respondent Count by Age, Classified by Education Level"},
            {"file": "current_technologies_grouped.csv", "rows": len(current_technologies_grouped), "purpose": "Grouped asset for Current Technology Usage dashboard"},
            {"file": "future_technologies_grouped.csv", "rows": len(future_technologies_grouped), "purpose": "Grouped asset for Future Technology Trend dashboard"},
            {"file": "demographics_grouped.csv", "rows": len(demographics_grouped), "purpose": "Grouped asset for Demographics dashboard"},
        ]
    )
    save_csv(summary, "looker_assets_manifest.csv")

    print(f"Source dataset: {input_file}")
    print(f"Generated {len(summary) - 1} auxiliary CSV files in: {OUTPUT_DIR}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
