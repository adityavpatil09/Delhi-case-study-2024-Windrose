import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import save_figure

def load_and_clean_data(base_dir: str) -> pd.DataFrame:
    print("Loading datasets...")
    pollutant_path = os.path.join(base_dir, "data", "Delhi pollutant data.csv")
    met_path = os.path.join(base_dir, "data", "Delhi meteorological data.csv")
    
    df_pollutant = pd.read_csv(pollutant_path)
    df_met = pd.read_csv(met_path)
    
    # Clean column names
    df_pollutant.columns = df_pollutant.columns.str.strip()
    df_met.columns = df_met.columns.str.strip()
    
    df_pollutant['Timestamp'] = pd.to_datetime(df_pollutant['Timestamp'], errors='coerce')
    df_met['time'] = pd.to_datetime(df_met['time'], errors='coerce')
    
    print("Datasets Loaded")
    print(f"{len(df_pollutant)} observations")
    
    print("Merging...")
    df_combined = pd.merge(df_pollutant, df_met, left_on='Timestamp', right_on='time', how='inner')
    
    print("Completed")
    return df_combined

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df['Month'] = df['Timestamp'].dt.month
    df['Month_Name'] = df['Timestamp'].dt.strftime('%B')
    df['Hour'] = df['Timestamp'].dt.hour
    
    def get_season(month: int) -> str:
        if month in [12, 1, 2]: return 'Winter'
        elif month in [3, 4, 5]: return 'Summer'
        elif month in [6, 7, 8, 9]: return 'Monsoon'
        else: return 'Post-Monsoon'
    
    df['Season'] = df['Month'].apply(get_season)
    return df

def generate_monthly_analysis(df: pd.DataFrame):
    print("Generating Monthly Analysis...")
    sns.set_theme(style="whitegrid")
    
    metrics = [
        ('PM2.5 (µg/m³)', 'Figure_1_Monthly_PM25.png'),
        ('PM10 (µg/m³)', 'Figure_2_Monthly_PM10.png'),
        ('WS (m/s)', 'Figure_3_WindSpeed.png'),
        ('AT (°C)', 'Figure_4_Temperature.png'),
        ('RH (%)', 'Figure_5_Humidity.png')
    ]
    
    months_order = ["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"]
                    
    for col, filename in metrics:
        if col in df.columns:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Month_Name', y=col, data=df, order=months_order, errorbar=None, color='teal')
            plt.title(f"Monthly Average of {col}")
            plt.xlabel("Month")
            plt.ylabel(col)
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            save_figure(filename)
    print("Completed")

def generate_scatter_plots(df: pd.DataFrame):
    if 'WS (m/s)' in df.columns and 'PM2.5 (µg/m³)' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.regplot(x='WS (m/s)', y='PM2.5 (µg/m³)', data=df, scatter_kws={'alpha': 0.3}, line_kws={'color': 'red', 'label': 'Regression Line'})
        plt.title("PM2.5 vs Wind Speed")
        plt.xlabel("Wind Speed (m/s)")
        plt.ylabel("PM2.5 (µg/m³)")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        save_figure("Figure_6_PM25_vs_WS.png")

def generate_correlation_heatmap(df: pd.DataFrame):
    print("Generating Heatmap...")
    cols = ['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'NO2 (µg/m³)', 'SO2 (µg/m³)', 'CO (mg/m³)', 'WS (m/s)', 'AT (°C)', 'RH (%)']
    available_cols = [c for c in cols if c in df.columns]
    
    if available_cols:
        corr = df[available_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
        plt.title("Correlation Heatmap")
        save_figure("Figure_7_Correlation.png")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        corr.to_csv(os.path.join(base_dir, "output", "tables", "Correlation_Matrix.csv"))
        
        stats = df[available_cols].describe()
        stats.to_csv(os.path.join(base_dir, "output", "tables", "Summary_Statistics.csv"))
    print("Completed")

def run_analysis(base_dir: str) -> pd.DataFrame:
    df = load_and_clean_data(base_dir)
    df = add_features(df)
    
    output_csv = os.path.join(base_dir, "output", "cleaned_data", "Delhi_Combined.csv")
    df.to_csv(output_csv, index=False)
    
    generate_monthly_analysis(df)
    generate_scatter_plots(df)
    generate_correlation_heatmap(df)
    
    return df
