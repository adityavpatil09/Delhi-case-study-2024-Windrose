# Delhi Air Pollution Case Study: Wind Rose Analysis

## Project Overview
This project performs an automated, end-to-end analysis of air pollution in Delhi, focusing on the correlation between meteorological factors (specifically wind) and various pollutants (e.g., PM2.5, PM10). The analysis utilizes Python's data science ecosystem to build a reproducible pipeline that cleans data, performs statistical analysis, and generates publication-quality Wind Rose diagrams without relying on traditional tools such as R or OpenAir.

## Folder Structure
```
Delhi_WindRose_CaseStudy/
├── data/
│      Delhi pollutant data.csv
│      Delhi meteorological data.csv
├── output/
│      cleaned_data/
│      figures/
│      tables/
│      reports/
├── analysis.py
├── windrose.py
├── report.py
├── utils.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation
Ensure you have Python 3.8+ installed. It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

## Usage
Simply run the main script to execute the entire analysis pipeline:

```bash
python main.py
```

## Expected Outputs
The pipeline automatically provisions the `output/` directory with the following assets:
- **cleaned_data/**: `Delhi_Combined.csv` containing the merged and engineered dataset.
- **figures/**: 15 publication-quality graphs including scatter plots, monthly distributions, and seasonal wind rose diagrams (e.g., `Figure_1_Monthly_PM25.png`, `Figure_8_WindRose_Annual.png`).
- **reports/**: `Summary_Report.txt` encapsulating a comprehensive statistical and observational report based on the case study.

## Libraries Used
- **pandas, numpy**: Data manipulation and statistical calculations.
- **matplotlib, seaborn**: Standard visualization libraries used alongside styling for publication-quality output.
- **windrose**: Creation of advanced wind rose diagrams entirely in Python.
- **scipy**: Statistical correlations.
- **plotly** & **openpyxl**: Supplementary data structuring dependencies.

## Methodology & Case Study Explanation
The case study bridges Civil Engineering and Environmental Engineering domains by evaluating pollutant dispersion against climatic variables.
1. **Data Fusion**: We load both hourly meteorological and pollutant datasets and merge them temporally.
2. **Analysis**: Core pollutants (PM2.5, PM10) are tracked month-over-month. Seasonality parameters (Winter, Summer, Monsoon, Post-Monsoon) are introduced to study pollutant variance. 
3. **Wind Rose Evaluation**: We model wind speed against direction vector distributions across seasons applying Sector Frequency metrics.
4. **Automated Documentation**: Lastly, we compile all statistical descriptors into a singular summary report linking atmospheric attributes to pollution peaks/valleys, acting as a complete analytical conclusion for the case study.
