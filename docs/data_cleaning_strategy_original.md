# Data Cleaning Strategy

Base dataset used:

- `survey-data-normalized.csv`

Files generated:

- `survey-data-missing-handled.csv`
- `survey-data-missing-handled-reduced.csv`

## 1. Missing-value handling strategy

### Numeric variables

Strategy used:

- Keep identifier columns unchanged.
- Impute numeric analysis variables with the median.

Reasoning:

- The survey contains highly skewed compensation and rating-style fields.
- Median imputation is more robust than the mean when extreme values are present.
- This avoids dropping large portions of the dataset.

Numeric columns imputed with median:

- `CompTotal`
- `WorkExp`
- `JobSatPoints_1`
- `JobSatPoints_4`
- `JobSatPoints_5`
- `JobSatPoints_6`
- `JobSatPoints_7`
- `JobSatPoints_8`
- `JobSatPoints_9`
- `JobSatPoints_10`
- `JobSatPoints_11`
- `JobSat`

Numeric columns preserved without additional imputation:

- `ResponseId`
- `ConvertedCompYearly`
- `ConvertedCompYearly_MinMax`
- `ConvertedCompYearly_Zscore`

Note:

- `ConvertedCompYearly` and its derived normalization columns were already part of the prior workflow and were recomputed consistently in the new output.

### Categorical variables

Strategy used:

- Low-cardinality categorical columns: impute with mode.
- High-cardinality / free-text / multi-select columns: impute with `Not specified`.

Reasoning:

- For structured single-choice variables, mode imputation preserves the dominant category.
- For multi-select and text-heavy fields, mode imputation would over-impose a specific answer pattern.
- `Not specified` keeps the distinction between observed answers and imputed absence.

Examples imputed with mode:

- `EdLevel`
- `OrgSize`
- `PurchaseInfluence`
- `BuildvsBuy`
- `SOVisitFreq`
- `SOAccount`
- `SOPartFreq`
- `SOComm`
- `AISelect`
- `AISent`
- `AIAcc`
- `AIComplex`
- `AIThreat`
- `TBranch`
- `ICorPM`
- `Knowledge_1` to `Knowledge_9`
- `Frequency_1` to `Frequency_3`
- `TimeSearching`
- `TimeAnswering`
- `ProfessionalCloud`
- `ProfessionalQuestion`
- `Industry`
- `SurveyLength`
- `SurveyEase`

Examples imputed with `Not specified`:

- `LearnCode`
- `LearnCodeOnline`
- `TechDoc`
- `YearsCode`
- `YearsCodePro`
- `DevType`
- `BuyNewTool`
- `TechEndorse`
- `Country`
- `Currency`
- `LanguageHaveWorkedWith`
- `LanguageWantToWorkWith`
- `LanguageAdmired`
- `DatabaseHaveWorkedWith`
- `DatabaseWantToWorkWith`
- `DatabaseAdmired`
- `PlatformHaveWorkedWith`
- `PlatformWantToWorkWith`
- `PlatformAdmired`
- `WebframeHaveWorkedWith`
- `WebframeWantToWorkWith`
- `WebframeAdmired`
- `EmbeddedHaveWorkedWith`
- `EmbeddedWantToWorkWith`
- `EmbeddedAdmired`
- `MiscTechHaveWorkedWith`
- `MiscTechWantToWorkWith`
- `MiscTechAdmired`
- `ToolsTechHaveWorkedWith`
- `ToolsTechWantToWorkWith`
- `ToolsTechAdmired`
- `NEWCollabToolsHaveWorkedWith`
- `NEWCollabToolsWantToWorkWith`
- `NEWCollabToolsAdmired`
- `OpSysPersonal use`
- `OpSysProfessional use`
- `OfficeStackAsyncHaveWorkedWith`
- `OfficeStackAsyncWantToWorkWith`
- `OfficeStackAsyncAdmired`
- `OfficeStackSyncHaveWorkedWith`
- `OfficeStackSyncWantToWorkWith`
- `OfficeStackSyncAdmired`
- `AISearchDevHaveWorkedWith`
- `AISearchDevWantToWorkWith`
- `AISearchDevAdmired`
- `NEWSOSites`
- `SOHow`
- `AIBen`
- `AIToolCurrently Using`
- `AIToolInterested in Using`
- `AIToolNot interested in Using`
- `AINextMuch more integrated`
- `AINextNo change`
- `AINextMore integrated`
- `AINextLess integrated`
- `AINextMuch less integrated`
- `AIEthics`
- `AIChallenges`
- `Frustration`
- `ProfessionalTech`

Result:

- `survey-data-missing-handled.csv` has `0` missing values remaining.

## 2. Reduced-copy strategy

The reduced copy was created from `survey-data-missing-handled.csv`, but the decision to drop columns with excessive missingness was based on the original missingness profile of `survey-data-normalized.csv`.

Columns dropped because they had more than 80% missing values before imputation:

- `AINextLess integrated`
- `AINextMuch less integrated`
- `AINextNo change`

Columns dropped as irrelevant for broad downstream analysis:

- `Check`

Reasoning:

- `Check` is constant and therefore contributes no analytical signal.
- The three `AINext*` fields above had extremely sparse coverage and would add more noise than value in a compact modeling/analysis copy.

Result:

- `survey-data-missing-handled-reduced.csv` has `0` missing values remaining.
- Final shape: `65437 x 112`

## 3. Softened outlier-removal strategy

Base dataset used for this stage:

- `survey-data-outliers-removed.csv`

Output generated:

- `survey-data-correlation-ready.csv`

Strategy used:

- Keep the outlier analysis visible for all numeric columns.
- Remove rows only when they contain extreme outliers in the continuous, comparable variables used downstream:
  - `ConvertedCompYearly`
  - `WorkExp`
- Use a softer threshold than the previous version:
  - `EXTREME_IQR`: `Q1 - 3*IQR` and `Q3 + 3*IQR`
  - `4_STD`: `mean ± 4 * std` when `IQR = 0` or quartiles are unstable

Why the strategy was softened:

- The previous notebook version removed any row flagged in any numeric column, which was too aggressive.
- Several numeric fields are bounded scales or were previously median-imputed, so their concentrated distributions can produce misleading “outliers”.
- `CompTotal` is raw compensation in local currency and is not directly comparable across countries, so it is useful for diagnostics but not for row deletion.
- The derived columns `ConvertedCompYearly_MinMax` and `ConvertedCompYearly_Zscore` contain the same signal already represented by `ConvertedCompYearly`.

Columns analyzed but not used to drop rows:

- `CompTotal`
- `JobSat`
- `JobSatPoints_1`
- `JobSatPoints_4`
- `JobSatPoints_5`
- `JobSatPoints_6`
- `JobSatPoints_7`
- `JobSatPoints_8`
- `JobSatPoints_9`
- `JobSatPoints_10`
- `JobSatPoints_11`
- `ConvertedCompYearly_MinMax`
- `ConvertedCompYearly_Zscore`

Reasoning:

- Satisfaction variables are bounded ordinal/rating fields where extreme valid answers should be preserved.
- Median imputation compresses quartiles and can make normal values look abnormal under strict IQR logic.
- Using only `ConvertedCompYearly` and `WorkExp` focuses the cleanup on interpretable continuous variables that matter directly for the correlation analysis.

Result:

- `survey-data-correlation-ready.csv` is the softened output for the correlation-ready stage.
- This version preserves substantially more rows while still removing the most extreme values.
