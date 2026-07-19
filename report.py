import os
import pandas as pd

def generate_report(df: pd.DataFrame, base_dir: str):
    print("Generating Report...")
    report_path = os.path.join(base_dir, "output", "reports", "Summary_Report.txt")
    
    pm25 = 'PM2.5 (µg/m³)'
    ws = 'WS (m/s)'
    
    if pm25 in df.columns and ws in df.columns:
        monthly_pm25 = df.groupby('Month_Name')[pm25].mean()
        high_pm25_month = monthly_pm25.idxmax()
        low_pm25_month = monthly_pm25.idxmin()
        
        monthly_ws = df.groupby('Month_Name')[ws].mean()
        high_ws_month = monthly_ws.idxmax()
        low_ws_month = monthly_ws.idxmin()
        
        corr_pm25_ws = df[pm25].corr(df[ws])
        
        stats_pm25 = df[pm25].describe()
        stats_ws = df[ws].describe()
        
        content = f"""======================================
Delhi Air Pollution Case Study Report
======================================

1. Dataset Summary
------------------
Total observations: {len(df)}
Time period covered: {df['Timestamp'].min()} to {df['Timestamp'].max()}

2. Pollution Highlights (PM2.5)
-------------------------------
Highest PM2.5 month: {high_pm25_month} ({monthly_pm25[high_pm25_month]:.2f} µg/m³)
Lowest PM2.5 month: {low_pm25_month} ({monthly_pm25[low_pm25_month]:.2f} µg/m³)

Mean: {stats_pm25['mean']:.2f}
Median: {stats_pm25['50%']:.2f}
Maximum: {stats_pm25['max']:.2f}
Minimum: {stats_pm25['min']:.2f}
Standard deviation: {stats_pm25['std']:.2f}

3. Wind Observations
--------------------
Highest Wind Speed month: {high_ws_month} ({monthly_ws[high_ws_month]:.2f} m/s)
Lowest Wind Speed month: {low_ws_month} ({monthly_ws[low_ws_month]:.2f} m/s)

Mean: {stats_ws['mean']:.2f}
Median: {stats_ws['50%']:.2f}
Maximum: {stats_ws['max']:.2f}
Minimum: {stats_ws['min']:.2f}
Standard deviation: {stats_ws['std']:.2f}

4. Correlation
--------------
Correlation between PM2.5 and Wind Speed: {corr_pm25_ws:.4f}

5. Important Conclusions
------------------------
- Wind speed tends to influence the dispersion of PM2.5.
- Analysis shows a specific seasonal trend depending on the dominant wind directions plotted in the wind rose diagrams.
- Higher wind speeds often result in lower PM2.5 concentrations due to increased atmospheric mixing.

======================================
"""
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Completed")
    else:
        print("Required columns missing for report generation.")
