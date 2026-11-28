# Startup Funding & Sector Investment Dashboard

An interactive Data Science project to analyze startup funding patterns, explore sector-wise investments, and predict startup industry categories using Machine Learning.

## 1. Problem Statement

Startup funding data contains valuable information about investment patterns, industries, cities, and investors. However, the data may contain missing values, inconsistent formats, and unstructured entries.

The objective of this project is to clean Indian startup funding data using Python and Regular Expressions (Regex), analyze funding trends across different sectors and cities, and develop an interactive Streamlit dashboard for investors and funding exploration.

## 2. Project Objectives

- Clean and preprocess startup funding data using Python and Regex.
- Analyze startup funding trends across different years.
- Identify industries receiving the highest investments.
- Explore funding distribution across different cities.
- Analyze investment types and frequently listed investors.
- Perform statistical analysis to identify relationships and differences.
- Build and compare machine learning classification models.
- Develop an interactive Streamlit dashboard for funding exploration and industry prediction.

## 3. Dataset Description

This project uses a startup funding dataset containing information about startup companies and their funding activities.

| Dataset Information | Details |
|---|---|
| Total Records | 3,044 |
| Original Columns | 10 |
| Time Period | 2015–2020 |
| Data Type | Startup funding records |

### Dataset Attributes

| Column | Description |
|---|---|
| Sr No | Serial number of the record |
| Date dd/mm/yyyy | Date of funding |
| Startup Name | Name of the startup |
| Industry Vertical | Main industry of the startup |
| SubVertical | Specific industry category |
| City Location | Location of the startup |
| Investors Name | Names of the investors |
| InvestmentnType | Type of investment |
| Amount in USD | Funding amount in USD |
| Remarks | Additional funding details |

**Dataset Source:** Add the original dataset URL here: `[Insert dataset link]`

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Scikit-learn | Machine learning and evaluation |
| Streamlit | Interactive dashboard |
| Plotly | Interactive charts |
| Joblib | Saving and loading the trained model |
| Jupyter Notebook | Data analysis and model development |
| Git and GitHub | Version control |
| VS Code | Development environment |

## 5. Project Workflow

The project follows these steps:

1. Data Collection
2. Data Cleaning and Preprocessing
3. Exploratory Data Analysis (EDA)
4. Statistical Analysis
5. Feature Engineering
6. Machine Learning Model Building
7. Model Evaluation and Comparison
8. Streamlit Dashboard Development

## 6. Data Cleaning and Preprocessing

Data cleaning was performed using Pandas and Regular Expressions (Regex).

The following operations were carried out:

- Standardized date values and corrected invalid date entries.
- Cleaned funding amount values and converted them into numeric format.
- Identified approximate funding amounts.
- Standardized city names and industry categories.
- Cleaned investment types and investor names.
- Handled missing categorical values using appropriate methods, including `"Unknown"`.
- Checked duplicate records.
- Detected funding amount outliers using the Interquartile Range (IQR) method.
- Created an outlier indicator without removing the detected outliers.

**Final feature-engineered dataset:** 3,044 records and 26 columns.

## 7. Exploratory Data Analysis (EDA)

EDA was performed to understand funding patterns and identify useful insights.

The analysis includes:

- Year-wise funding distribution.
- Industry-wise funding analysis.
- City-wise startup funding analysis.
- Investment type analysis.
- Investor frequency analysis.
- Funding amount distribution.
- Identification of funding trends and patterns.

### Key Observations

- Bengaluru recorded the highest total funding among the cities.
- Ecommerce recorded the highest total funding among the industry categories.
- Private Equity contributed the highest total funding among investment types.
- Seed Funding was the most frequent investment type by number of records.
- Funding amounts showed a highly right-skewed distribution.

## 8. Statistical Analysis

Statistical methods were used to examine relationships and differences in the funding data.

### Correlation Analysis

| Test | Correlation | P-value |
|---|---:|---:|
| Pearson Correlation | 0.1000 | 5.29 × 10⁻⁶ |
| Spearman Correlation | 0.1810 | 1.15 × 10⁻¹⁶ |

Both tests indicated a weak positive relationship between funding year and funding amount. The p-values were below 0.05, indicating statistical significance.

### Kruskal-Wallis Test

- H-statistic: 64.7611
- P-value: 1.61 × 10⁻¹⁰

The result indicates a statistically significant difference in funding amount distributions across at least some of the industry groups tested.

## 9. Feature Engineering

Feature engineering was performed to prepare the dataset for machine learning.

The following features were created or transformed:

- **Year:** Extracted from the cleaned funding date.
- **Month:** Extracted from the cleaned funding date.
- **City_Grouped:** Grouped cities with fewer than 20 records into `"Other"`, while retaining `"Unknown"`.
- **Industry_Grouped:** Preserved the actual cleaned industry names. Missing industry values were represented as `"Unknown"`.
- **Investment_Type_Grouped:** Grouped less frequent investment categories.
- **SubVertical_Grouped:** Grouped rare sub-vertical categories.

For machine learning, industries with fewer than 10 records and the `"Unknown"` category were excluded from the model training dataset. This resulted in 1,990 records across 11 industry categories.

## 10. Machine Learning Model

The project uses **multiclass classification** to predict the industry category of a startup based on its funding-related information.

### Target Variable

- `Industry_Grouped`

### Input Features

1. Year
2. Month
3. City_Grouped
4. Investment_Type_Grouped
5. Amount_Cleaned
6. SubVertical_Cleaned

### Models Trained

Three classification algorithms were trained and compared:

1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier

### Model Evaluation Results

| Model | Accuracy | Macro F1-score | Weighted F1-score | ROC-AUC |
|---|---:|---:|---:|---:|
| Logistic Regression | 39.70% | 0.1694 | 0.4276 | 0.6669 |
| Decision Tree | 34.92% | 0.1362 | 0.3459 | 0.5499 |
| Random Forest | 50.00% | 0.1125 | 0.4108 | 0.6859 |

Random Forest achieved the highest accuracy and ROC-AUC among the three models. Logistic Regression achieved the highest Macro F1-score and Weighted F1-score.

The model performance is affected by class imbalance because some industries have significantly more records than others. Therefore, the models perform differently across industry categories.

The selected Random Forest pipeline was saved using Joblib and integrated into the Streamlit dashboard.

**Note:** Predictions are experimental and should be interpreted with care, particularly for industries with fewer training records.

## 11. Streamlit Dashboard Features

An interactive Streamlit dashboard was developed to explore startup funding information and predict industry categories.

The dashboard contains seven pages:

1. **Overview:** Displays key statistics, yearly trends, industry distribution, top cities, and funding records.
2. **Trends:** Shows year-wise funding patterns and funding record counts.
3. **By Industry:** Explores industry-wise funding distribution and startup records.
4. **By City:** Displays city-wise funding trends and startup distribution.
5. **Top Investors:** Identifies frequently listed investors and their funding records.
6. **Prediction:** Predicts a startup's industry category using the trained Random Forest model.
7. **Funding Explorer:** Allows users to search and filter startup funding records.

The dashboard uses interactive charts, tables, and filters to make funding information easier to explore.

## 12. Project Folder Structure

```text
ds-startup-funding-analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_cleaning_and_eda.ipynb
│   ├── 02_correlation_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_building.ipynb
│
├── models/
│   └── random_forest_model.joblib
│
├── src/
├── docs/
│
├── app.py
├── README.md
└── .gitignore
```

**Note:** Dataset CSV files are excluded from GitHub using `.gitignore`. Obtain the dataset from the source listed above and place the required files in the appropriate folders before running the application.

## 13. How to Run the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/mallasrujana45-hub/ds-startup-funding-analysis.git
```

### Step 2: Open the Project Folder

```bash
cd ds-startup-funding-analysis
```

### Step 3: Install Required Libraries

```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit plotly joblib
```

### Step 4: Run the Streamlit Dashboard

```bash
streamlit run app.py
```

### Step 5: Open the Dashboard

After running the command, Streamlit will provide a local URL. Open that URL in your browser to access the dashboard.

Make sure the required processed dataset files and trained model file are available in their respective project folders.

## 14. Conclusion

The Startup Funding & Sector Investment Dashboard provides an interactive platform to explore startup funding patterns and investment trends.

Through data cleaning, exploratory data analysis, statistical analysis, feature engineering, and machine learning, this project identifies useful insights from startup funding records.

The Streamlit dashboard enables users to explore funding information by year, industry, city, and investors. It also provides an industry prediction feature using a trained Random Forest classifier.

This project demonstrates how Data Science and Machine Learning can be applied to real-world startup funding data to support analysis and investment exploration.

## 15. Future Scope

- Include more recent startup funding data.
- Improve model performance using additional features and class imbalance handling.
- Explore additional machine learning algorithms.
- Add more interactive visualizations and analytical features.
- Deploy the dashboard publicly for wider access.
