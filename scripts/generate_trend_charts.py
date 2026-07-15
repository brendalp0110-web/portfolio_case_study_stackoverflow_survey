from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "data" / "dashboard_assets"
OUTPUT_DIR = ROOT_DIR / "assets" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_dual_bar_chart(
    left_df: pd.DataFrame,
    left_label_col: str,
    left_value_col: str,
    left_title: str,
    right_df: pd.DataFrame,
    right_label_col: str,
    right_value_col: str,
    right_title: str,
    output_name: str,
    color_left: str = "#4C78A8",
    color_right: str = "#59A14F",
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    axes[0].bar(left_df[left_label_col], left_df[left_value_col], color=color_left)
    axes[0].set_title(left_title)
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Count")
    axes[0].tick_params(axis="x", rotation=35)
    for i, value in enumerate(left_df[left_value_col]):
        axes[0].text(i, value + max(left_df[left_value_col]) * 0.01, f"{value:,}", ha="center", va="bottom", fontsize=8)

    axes[1].bar(right_df[right_label_col], right_df[right_value_col], color=color_right)
    axes[1].set_title(right_title)
    axes[1].set_xlabel("")
    axes[1].set_ylabel("Count")
    axes[1].tick_params(axis="x", rotation=35)
    for i, value in enumerate(right_df[right_value_col]):
        axes[1].text(i, value + max(right_df[right_value_col]) * 0.01, f"{value:,}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / output_name, dpi=300, bbox_inches="tight")
    plt.close()


def generate_language_trends_chart() -> None:
    current_df = pd.read_csv(ASSETS_DIR / "current_top10_languages_used.csv")
    future_df = pd.read_csv(ASSETS_DIR / "future_top10_languages_desired.csv")

    plot_dual_bar_chart(
        current_df,
        "language",
        "count",
        "Top 10 Programming Languages Used",
        future_df,
        "language",
        "count",
        "Top 10 Programming Languages Desired Next Year",
        "slide_9_programming_language_trends.png",
    )


def generate_database_trends_chart() -> None:
    current_df = pd.read_csv(ASSETS_DIR / "current_top10_databases_used.csv")
    future_df = pd.read_csv(ASSETS_DIR / "future_top10_databases_desired.csv")

    plot_dual_bar_chart(
        current_df,
        "database",
        "count",
        "Top 10 Databases Used",
        future_df,
        "database",
        "count",
        "Top 10 Databases Desired Next Year",
        "slide_11_database_trends.png",
        color_left="#F28E2B",
        color_right="#E15759",
    )


def main() -> None:
    plt.style.use("ggplot")
    generate_language_trends_chart()
    generate_database_trends_chart()
    print(f"Charts saved to: {OUTPUT_DIR}")
    print("- slide_9_programming_language_trends.png")
    print("- slide_11_database_trends.png")


if __name__ == "__main__":
    main()
