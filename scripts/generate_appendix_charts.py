from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_DIR = ROOT_DIR / "assets" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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
    "Not specified": None,
}


def load_dataset() -> pd.DataFrame:
    preferred = DATA_DIR / "survey_data_correlation_ready.csv"
    fallback = DATA_DIR / "survey_data_updated.csv"
    source = preferred if preferred.exists() else fallback
    return pd.read_csv(source)


def split_multiselect(series: pd.Series) -> pd.Series:
    cleaned = series.dropna().astype(str).str.strip()
    cleaned = cleaned[~cleaned.isin(["", "Not specified"])]
    return cleaned.str.split(";").explode().str.strip()


def plot_box_compensation_by_employment(df: pd.DataFrame) -> None:
    top_employment = df["Employment"].value_counts().head(6).index.tolist()
    plot_df = df[df["Employment"].isin(top_employment)][["Employment", "ConvertedCompYearly"]].dropna()
    groups = [plot_df.loc[plot_df["Employment"] == category, "ConvertedCompYearly"].values for category in top_employment]

    plt.figure(figsize=(12, 6))
    plt.boxplot(groups, labels=top_employment, patch_artist=True)
    plt.title("ConvertedCompYearly by Employment Type")
    plt.xlabel("Employment")
    plt.ylabel("Converted Compensation Yearly")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "appendix_compensation_by_employment.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_box_compensation_by_devtype(df: pd.DataFrame) -> None:
    top_devtypes = split_multiselect(df["DevType"]).value_counts().head(5).index.tolist()
    exploded = (
        df[["DevType", "ConvertedCompYearly"]]
        .dropna(subset=["DevType", "ConvertedCompYearly"])
        .assign(DevType=lambda d: d["DevType"].str.split(";"))
        .explode("DevType")
    )
    exploded["DevType"] = exploded["DevType"].str.strip()
    exploded = exploded[exploded["DevType"].isin(top_devtypes)]
    groups = [exploded.loc[exploded["DevType"] == category, "ConvertedCompYearly"].values for category in top_devtypes]

    plt.figure(figsize=(12, 6))
    plt.boxplot(groups, labels=top_devtypes, patch_artist=True)
    plt.title("ConvertedCompYearly for Top Developer Types")
    plt.xlabel("Developer Type")
    plt.ylabel("Converted Compensation Yearly")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "appendix_compensation_by_devtype.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_mean_median_jobsat_by_age(df: pd.DataFrame) -> None:
    plot_df = df.copy()
    plot_df = plot_df[plot_df["Age"].isin(AGE_ORDER[:-1])]
    summary = (
        plot_df.groupby("Age")["JobSatPoints_6"]
        .agg(["mean", "median"])
        .reindex(AGE_ORDER[:-1])
        .reset_index()
    )

    x = list(range(len(summary)))
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar([i - width / 2 for i in x], summary["mean"], width=width, label="Mean")
    plt.bar([i + width / 2 for i in x], summary["median"], width=width, label="Median")
    plt.title("Mean vs Median Job Satisfaction by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("JobSatPoints_6")
    plt.xticks(x, summary["Age"], rotation=35, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "appendix_mean_median_jobsat_by_age.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_age_vs_workexp_scatter(df: pd.DataFrame) -> None:
    plot_df = df.copy()
    plot_df["Age_num"] = plot_df["Age"].map(AGE_MID_MAP)
    plot_df = plot_df[["Age_num", "WorkExp"]].dropna()
    if len(plot_df) > 3000:
        plot_df = plot_df.sample(3000, random_state=42)

    plt.figure(figsize=(10, 6))
    plt.scatter(plot_df["Age_num"], plot_df["WorkExp"], alpha=0.35)
    plt.title("Age vs Work Experience")
    plt.xlabel("Age")
    plt.ylabel("Work Experience")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "appendix_age_vs_workexp.png", dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    plt.style.use("ggplot")
    df = load_dataset()
    plot_box_compensation_by_employment(df)
    plot_box_compensation_by_devtype(df)
    plot_mean_median_jobsat_by_age(df)
    plot_age_vs_workexp_scatter(df)
    print(f"Charts saved to: {OUTPUT_DIR}")
    print("- appendix_compensation_by_employment.png")
    print("- appendix_compensation_by_devtype.png")
    print("- appendix_mean_median_jobsat_by_age.png")
    print("- appendix_age_vs_workexp.png")


if __name__ == "__main__":
    main()
