import os
import sys

# Workaround for name shadowing of windrose library due to this filename
_temp_mod = sys.modules.pop('windrose', None)
_paths_removed = []
for p in list(sys.path):
    if p == '' or p == os.path.dirname(os.path.abspath(__file__)):
        sys.path.remove(p)
        _paths_removed.append(p)

import windrose as real_windrose
from windrose import WindroseAxes

if _temp_mod:
    sys.modules['windrose'] = _temp_mod
for p in _paths_removed:
    sys.path.insert(0, p)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import save_figure


def generate_annual_wind_rose(df: pd.DataFrame):
    if 'WD (deg)' not in df.columns or 'WS (m/s)' not in df.columns:
        return
    plt.figure(figsize=(8, 8))
    ax = WindroseAxes.from_ax()
    ax.bar(df['WD (deg)'], df['WS (m/s)'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    plt.title("Annual Wind Rose", y=1.08)
    save_figure("Figure_8_WindRose_Annual.png")

def generate_seasonal_wind_roses(df: pd.DataFrame):
    if 'WD (deg)' not in df.columns or 'WS (m/s)' not in df.columns or 'Season' not in df.columns:
        return
    seasons = [
        ('Winter', 'Figure_9_WindRose_Winter.png'),
        ('Summer', 'Figure_10_WindRose_Summer.png'),
        ('Monsoon', 'Figure_11_WindRose_Monsoon.png'),
        ('Post-Monsoon', 'Figure_12_WindRose_PostMonsoon.png')
    ]
    for season, filename in seasons:
        season_df = df[df['Season'] == season]
        if season_df.empty:
            continue
        plt.figure(figsize=(8, 8))
        ax = WindroseAxes.from_ax()
        ax.bar(season_df['WD (deg)'], season_df['WS (m/s)'], normed=True, opening=0.8, edgecolor='white')
        ax.set_legend()
        plt.title(f"Wind Rose - {season}", y=1.08)
        save_figure(filename)

def run_windrose_analysis(df: pd.DataFrame):
    print("Generating Wind Rose...")
    generate_annual_wind_rose(df)
    generate_seasonal_wind_roses(df)
    
    if 'WD (deg)' in df.columns:
        plt.figure(figsize=(10, 6))
        
        sectors = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
                   'S','SSW','SW','WSW','W','WNW','NW','NNW']
        bins = np.arange(11.25, 360 + 22.5, 22.5)
        
        categories = pd.cut(df['WD (deg)'] % 360, bins, labels=sectors[1:] + ['N'])
        df_dir = pd.DataFrame({'dir': categories})
        df_dir['dir'] = df_dir['dir'].fillna('N')
        
        sns.countplot(x='dir', data=df_dir, order=sectors, color='steelblue')
        plt.title("Wind Direction Frequency")
        plt.xlabel("Compass Sector")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle='--', alpha=0.7)
        save_figure("Figure_13_WindDirectionFrequency.png")
        
    if 'WS (m/s)' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df['WS (m/s)'].dropna(), bins=30, kde=True, color='skyblue')
        plt.title("Wind Speed Distribution (Histogram)")
        plt.xlabel("Wind Speed (m/s)")
        plt.ylabel("Frequency")
        plt.grid(True, linestyle='--', alpha=0.7)
        save_figure("Figure_14_WindHistogram.png")
        
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=df['WS (m/s)'].dropna(), color='lightgreen')
        plt.title("Wind Speed Boxplot")
        plt.ylabel("Wind Speed (m/s)")
        plt.grid(True, linestyle='--', alpha=0.7)
        save_figure("Figure_15_WindBoxplot.png")
        
    print("Completed")
