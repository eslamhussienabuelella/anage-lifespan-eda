# AnAge Animal Lifespan Exploratory Data Analysis

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualisation-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-lightgrey)

A reproducible exploratory data analysis project using the AnAge animal ageing and longevity dataset. The project summarises animal class representation and explores whether larger animals tend to live longer by comparing adult body weight and maximum longevity for the four most represented animal classes.

This repository is based on **Task 3: Critically assess, select and apply data science tools (MLO3)** from the Coventry University Principles of Data Science portfolio.

---

## Project overview

The analysis answers two questions:

1. How many animal species/common names have maximum longevity data within each Animalia class?
2. For the four most represented classes, how does maximum longevity vary with adult body weight?

The project uses Python visualisation libraries to communicate patterns clearly for decision makers and ageing-research audiences.

---

## Dataset

The dataset is a tab-delimited AnAge export containing longevity and biological attributes for more than 4,000 organisms.

The analysis focuses on these fields:

| Field | Role |
|---|---|
| `Kingdom` | Filters the dataset to Animalia |
| `Class` | Groups species into animal classes |
| `Common name` | Species/common-name identifier used for counts and labels |
| `Adult weight (g)` | Body-size variable for scatter plots |
| `Maximum longevity (yrs)` | Lifespan variable for summary and scatter plots |

The included `data/anage_data.txt` file is the working tab-delimited dataset used by the script.

---

## Repository structure

```text
anage-lifespan-eda/
├── data/
│   └── anage_data.txt
├── src/
│   └── anage_lifespan_analysis.py
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── analysis_summary.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Methods

The workflow follows four reproducible stages:

1. Load the AnAge tab-delimited dataset using pandas.
2. Filter to `Kingdom == "Animalia"` and retain records with known maximum longevity.
3. Count species/common names by `Class` and visualise class representation.
4. Select the four most represented classes and plot `Maximum longevity (yrs)` against `Adult weight (g)` using log-scaled axes.

Additional outputs include class-level correlations on log-transformed variables and IQR-based outlier tables.

---

## Key results

The four most represented animal classes in this dataset are:

| Rank | Class | Species/common names with longevity data |
|---:|---|---:|
| 1 | Aves | 1394 |
| 2 | Mammalia | 1029 |
| 3 | Teleostei | 798 |
| 4 | Reptilia | 526 |

The log-log plots show that larger animals often live longer, but the pattern varies by class. The trend is generally clearer in mammals and birds than in fish and reptiles, where ecological strategy, physiology, captivity records, and exceptional species can weaken a simple body-size interpretation.

Notable outliers include very large mammals such as the blue whale, long-lived reptiles such as giant tortoises, and long-lived birds such as parrots and condors. These outliers are valuable for ageing research because they may reveal biological mechanisms associated with exceptional longevity, slower life-history strategies, or unusual resistance to age-related decline.

---

## Outputs

Running the analysis creates:

### Figures

- `outputs/figures/species_count_by_class.png`
- `outputs/figures/longevity_vs_adult_weight_top4_classes.png`
- `outputs/figures/class_specific_log_scatterplots.png`
- `outputs/figures/aves_outliers.png`
- `outputs/figures/mammalia_outliers.png`
- `outputs/figures/teleostei_outliers.png`
- `outputs/figures/reptilia_outliers.png`

### Tables

- `outputs/tables/species_count_by_class.csv`
- `outputs/tables/top4_classes_analysis_data.csv`
- `outputs/tables/class_level_weight_longevity_metrics.csv`
- `outputs/tables/iqr_outliers_top4_classes.csv`

---

## How to run

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Run the analysis from the repository root:

```bash
python src/anage_lifespan_analysis.py
```

---

## Decision-maker interpretation

Body size is useful but not sufficient for understanding lifespan. The visualisations suggest a broad positive association between adult weight and longevity, especially in mammals and birds, but several extreme species demonstrate that longevity is also shaped by physiology, ecology, evolutionary strategy, and data provenance. For ageing research, this means exceptionally long-lived species should not be treated only as statistical outliers; they may be biologically informative targets for comparative ageing studies.

---

## License and data note

This repository is provided for educational and portfolio purposes. Please check the AnAge/HAGR database terms before redistributing the dataset externally.
