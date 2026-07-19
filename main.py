import os
import sys

from utils import ensure_directories
from analysis import load_and_clean_data, add_features, generate_monthly_analysis, generate_scatter_plots, generate_correlation_heatmap
from windrose import run_windrose_analysis
from report import generate_report

def main():
    print("======================================")
    print("Delhi Air Pollution Case Study")
    print("======================================")
    
    ensure_directories()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Load, clean, and merge data (prints Loading datasets... Datasets Loaded... Merging... Completed)
    df = load_and_clean_data(base_dir)
    
    # 2. Add features and save combined CSV
    df = add_features(df)
    output_csv = os.path.join(base_dir, "output", "cleaned_data", "Delhi_Combined.csv")
    df.to_csv(output_csv, index=False)
    
    # 3. Monthly Analysis (prints Generating Monthly Analysis... Completed)
    generate_monthly_analysis(df)
    
    # Generate scatter plot quietly as it wasn't strictly in the logger example
    generate_scatter_plots(df)
    
    # 4. Wind Rose Analysis (prints Generating Wind Rose... Completed)
    run_windrose_analysis(df)
    
    # 5. Correlation Heatmap (prints Generating Heatmap... Completed)
    generate_correlation_heatmap(df)
    
    # 6. Report (prints Generating Report... Completed)
    generate_report(df, base_dir)
    
    print("======================================")
    print("Project Completed Successfully")
    print("Output saved to")
    print("output/")
    print("======================================")

if __name__ == "__main__":
    main()
