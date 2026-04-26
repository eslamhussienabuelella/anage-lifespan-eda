"""
AnAge Animal Lifespan Exploratory Data Analysis
================================================

This script reproduces the Task 3 analysis from the Principles of Data Science
portfolio. It reads the AnAge tab-delimited dataset, summarises the number of
Animalia species with maximum longevity data by class, and explores the
relationship between adult body weight and maximum longevity for the four most
represented animal classes.

Run from the repository root:
    python src/anage_lifespan_analysis.py
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "anage_data.txt"
FIG_DIR = ROOT / "outputs" / "figures"
TABLE_DIR = ROOT / "outputs" / "tables"

RELEVANT_COLUMNS = [
    "Kingdom",
    "Class",
    "Common name",
    "Adult weight (g)",
    "Maximum longevity (yrs)",
]


def load_anage(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the tab-delimited AnAge dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path, sep="\t")


def prepare_animalia(df: pd.DataFrame) -> pd.DataFrame:
    """Keep relevant columns, Animalia records, and known longevity values."""
    missing = [col for col in RELEVANT_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    anage = df[RELEVANT_COLUMNS].copy()
    animalia = anage.loc[
        (anage["Kingdom"] == "Animalia")
        & anage["Maximum longevity (yrs)"].notna()
    ].copy()
    return animalia


def summarise_species_by_class(animalia: pd.DataFrame) -> pd.DataFrame:
    """Count species/common names per animal class with longevity data."""
    summary = (
        animalia.groupby("Class", as_index=False)["Common name"]
        .count()
        .rename(columns={"Common name": "species_count"})
        .sort_values("species_count", ascending=False)
    )
    return summary


def get_top_four_analysis_data(animalia: pd.DataFrame, class_summary: pd.DataFrame) -> pd.DataFrame:
    """Filter to the four most represented classes and complete weight/longevity records."""
    top_four = class_summary.head(4)["Class"].tolist()
    return animalia.loc[animalia["Class"].isin(top_four)].dropna(
        subset=["Adult weight (g)", "Maximum longevity (yrs)"]
    ).copy()


def compute_class_metrics(scatter_df: pd.DataFrame) -> pd.DataFrame:
    """Compute descriptive statistics and log-scale correlation by class."""
    rows = []
    for animal_class, group in scatter_df.groupby("Class"):
        log_weight = np.log10(group["Adult weight (g)"])
        log_longevity = np.log10(group["Maximum longevity (yrs)"])
        corr = float(np.corrcoef(log_weight, log_longevity)[0, 1])
        slope = float(np.polyfit(log_weight, log_longevity, deg=1)[0])
        rows.append(
            {
                "Class": animal_class,
                "n": len(group),
                "median_adult_weight_g": group["Adult weight (g)"].median(),
                "median_max_longevity_yrs": group["Maximum longevity (yrs)"].median(),
                "max_adult_weight_species": group.loc[group["Adult weight (g)"].idxmax(), "Common name"],
                "max_adult_weight_g": group["Adult weight (g)"].max(),
                "max_longevity_species": group.loc[group["Maximum longevity (yrs)"].idxmax(), "Common name"],
                "max_longevity_yrs": group["Maximum longevity (yrs)"].max(),
                "log10_weight_longevity_corr": corr,
                "log10_weight_longevity_slope": slope,
            }
        )
    return pd.DataFrame(rows).sort_values("n", ascending=False)


def compute_iqr_outliers(scatter_df: pd.DataFrame) -> pd.DataFrame:
    """Identify class-level IQR outliers in adult weight and/or maximum longevity."""
    rows = []
    for animal_class, group in scatter_df.groupby("Class"):
        q1_weight, q3_weight = group["Adult weight (g)"].quantile([0.25, 0.75])
        q1_age, q3_age = group["Maximum longevity (yrs)"].quantile([0.25, 0.75])
        iqr_weight = q3_weight - q1_weight
        iqr_age = q3_age - q1_age
        upper_weight = q3_weight + 1.5 * iqr_weight
        upper_age = q3_age + 1.5 * iqr_age

        outliers = group.loc[
            (group["Adult weight (g)"] > upper_weight)
            | (group["Maximum longevity (yrs)"] > upper_age)
        ].copy()
        outliers["weight_outlier"] = outliers["Adult weight (g)"] > upper_weight
        outliers["longevity_outlier"] = outliers["Maximum longevity (yrs)"] > upper_age
        outliers["weight_upper_threshold_g"] = upper_weight
        outliers["longevity_upper_threshold_yrs"] = upper_age
        rows.append(outliers)

    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True)[
        [
            "Class",
            "Common name",
            "Adult weight (g)",
            "Maximum longevity (yrs)",
            "weight_outlier",
            "longevity_outlier",
            "weight_upper_threshold_g",
            "longevity_upper_threshold_yrs",
        ]
    ].sort_values(["Class", "Maximum longevity (yrs)", "Adult weight (g)"], ascending=[True, False, False])


def save_class_count_plot(class_summary: pd.DataFrame) -> None:
    """Create horizontal bar chart of species counts by class."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plot_df = class_summary.sort_values("species_count", ascending=True)
    plt.figure(figsize=(10, 8))
    plt.barh(plot_df["Class"], plot_df["species_count"])
    plt.xscale("log")
    plt.xlabel("Number of species/common names with longevity data (log scale)")
    plt.ylabel("Animal class")
    plt.title("Animalia species represented in AnAge by class")
    for i, row in enumerate(plot_df.itertuples(index=False)):
        plt.text(row.species_count * 1.03, i, f"{row.species_count}", va="center", fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "species_count_by_class.png", dpi=300)
    plt.close()


def save_overall_scatter(scatter_df: pd.DataFrame) -> None:
    """Create combined scatter plot for the four most represented classes."""
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=scatter_df,
        x="Adult weight (g)",
        y="Maximum longevity (yrs)",
        hue="Class",
        style="Class",
        alpha=0.55,
        s=35,
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", linewidth=0.3)
    plt.xlabel("Adult weight (g, log scale)")
    plt.ylabel("Maximum longevity (years, log scale)")
    plt.title("Maximum longevity vs adult weight for the four most represented classes")

    # Annotate the most important overall extremes.
    extremes = pd.concat([
        scatter_df.nlargest(4, "Maximum longevity (yrs)"),
        scatter_df.nlargest(4, "Adult weight (g)"),
        scatter_df.nsmallest(2, "Maximum longevity (yrs)"),
        scatter_df.nsmallest(2, "Adult weight (g)"),
    ]).drop_duplicates()
    for _, row in extremes.iterrows():
        plt.annotate(
            row["Common name"],
            xy=(row["Adult weight (g)"], row["Maximum longevity (yrs)"]),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7,
        )
    plt.tight_layout()
    plt.savefig(FIG_DIR / "longevity_vs_adult_weight_top4_classes.png", dpi=300)
    plt.close()


def save_faceted_scatter(scatter_df: pd.DataFrame) -> None:
    """Create faceted log-log scatter plots by class."""
    classes = list(scatter_df["Class"].drop_duplicates())
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=False, sharey=False)
    axes = axes.ravel()
    for ax, animal_class in zip(axes, classes):
        group = scatter_df[scatter_df["Class"] == animal_class]
        ax.scatter(group["Adult weight (g)"], group["Maximum longevity (yrs)"], alpha=0.45, s=18)
        x = np.log10(group["Adult weight (g)"])
        y = np.log10(group["Maximum longevity (yrs)"])
        slope, intercept = np.polyfit(x, y, deg=1)
        xs = np.linspace(x.min(), x.max(), 100)
        ax.plot(10 ** xs, 10 ** (intercept + slope * xs), linewidth=1)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(True, which="both", linestyle="--", linewidth=0.3)
        ax.set_title(animal_class)
        ax.set_xlabel("Adult weight (g, log scale)")
        ax.set_ylabel("Maximum longevity (years, log scale)")
    fig.suptitle("Class-specific relationships between adult weight and longevity", y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "class_specific_log_scatterplots.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_outlier_tables_and_plots(scatter_df: pd.DataFrame) -> pd.DataFrame:
    """Save IQR outlier table and a compact plot for each class."""
    outliers = compute_iqr_outliers(scatter_df)
    outliers.to_csv(TABLE_DIR / "iqr_outliers_top4_classes.csv", index=False)

    for animal_class, group in scatter_df.groupby("Class"):
        q1_weight, q3_weight = group["Adult weight (g)"].quantile([0.25, 0.75])
        q1_age, q3_age = group["Maximum longevity (yrs)"].quantile([0.25, 0.75])
        upper_weight = q3_weight + 1.5 * (q3_weight - q1_weight)
        upper_age = q3_age + 1.5 * (q3_age - q1_age)

        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=group,
            x="Adult weight (g)",
            y="Maximum longevity (yrs)",
            alpha=0.55,
            s=22,
        )
        plt.axvline(upper_weight, linestyle="--", linewidth=1, label="Weight outlier threshold")
        plt.axhline(upper_age, linestyle="--", linewidth=1, label="Longevity outlier threshold")
        plt.xscale("log")
        plt.yscale("log")
        plt.grid(True, which="both", linestyle="--", linewidth=0.3)
        plt.title(f"{animal_class}: adult weight vs maximum longevity")
        plt.xlabel("Adult weight (g, log scale)")
        plt.ylabel("Maximum longevity (years, log scale)")

        label_df = pd.concat([
            group.nlargest(3, "Maximum longevity (yrs)"),
            group.nlargest(3, "Adult weight (g)"),
            group.nsmallest(2, "Maximum longevity (yrs)"),
            group.nsmallest(2, "Adult weight (g)"),
        ]).drop_duplicates()
        for _, row in label_df.iterrows():
            plt.annotate(row["Common name"], (row["Adult weight (g)"], row["Maximum longevity (yrs)"]),
                         xytext=(4, 4), textcoords="offset points", fontsize=7)
        plt.legend(fontsize=8)
        plt.tight_layout()
        safe_name = animal_class.lower().replace(" ", "_").replace("/", "_")
        plt.savefig(FIG_DIR / f"{safe_name}_outliers.png", dpi=300)
        plt.close()

    return outliers


def write_summary_markdown(raw_df: pd.DataFrame, class_summary: pd.DataFrame, metrics: pd.DataFrame, outliers: pd.DataFrame) -> None:
    """Write a compact findings summary for GitHub and decision makers."""
    top_four = class_summary.head(4)
    strongest = metrics.loc[metrics["log10_weight_longevity_corr"].idxmax()]
    weakest = metrics.loc[metrics["log10_weight_longevity_corr"].idxmin()]
    summary = f"""# Analysis summary

## Dataset inspection

- Raw dataset shape: **{raw_df.shape[0]:,} rows × {raw_df.shape[1]:,} columns**.
- Animalia records with known maximum longevity: **{class_summary['species_count'].sum():,}**.
- Four most represented classes: **{', '.join(top_four['Class'].tolist())}**.

## Species representation by class

{top_four.to_markdown(index=False)}

## Weight–longevity relationship

The log-log scatter plots show a generally positive association between adult body weight and maximum longevity, but the strength varies by class. Larger animals often live longer, especially within mammals and birds, although the relationship is not deterministic and several biological exceptions appear.

The strongest class-level log-scale correlation in this run is **{strongest['Class']}** (r = {strongest['log10_weight_longevity_corr']:.3f}), while the weakest is **{weakest['Class']}** (r = {weakest['log10_weight_longevity_corr']:.3f}).

## Class-level metrics

{metrics.to_markdown(index=False)}

## Notable outliers

The IQR rule identifies unusually large or long-lived species within each class. Key examples include long-lived birds such as parrots and condors, very large mammals such as whales, and long-lived reptiles such as giant tortoises. These species are useful for ageing research because they may highlight biological mechanisms linked to slow ageing, body-size scaling, metabolic strategy, and exceptional longevity.

The complete outlier table is saved at `outputs/tables/iqr_outliers_top4_classes.csv`.
"""
    (ROOT / "outputs" / "analysis_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = load_anage()
    animalia = prepare_animalia(raw_df)
    class_summary = summarise_species_by_class(animalia)
    scatter_df = get_top_four_analysis_data(animalia, class_summary)
    metrics = compute_class_metrics(scatter_df)

    class_summary.to_csv(TABLE_DIR / "species_count_by_class.csv", index=False)
    scatter_df.to_csv(TABLE_DIR / "top4_classes_analysis_data.csv", index=False)
    metrics.to_csv(TABLE_DIR / "class_level_weight_longevity_metrics.csv", index=False)

    save_class_count_plot(class_summary)
    save_overall_scatter(scatter_df)
    save_faceted_scatter(scatter_df)
    outliers = save_outlier_tables_and_plots(scatter_df)
    write_summary_markdown(raw_df, class_summary, metrics, outliers)

    print("Analysis complete.")
    print(f"Tables saved to: {TABLE_DIR}")
    print(f"Figures saved to: {FIG_DIR}")
    print("Top four classes:")
    print(class_summary.head(4).to_string(index=False))
    print("\nClass-level metrics:")
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
