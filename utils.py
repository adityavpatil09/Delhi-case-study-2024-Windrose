import os
import matplotlib.pyplot as plt

def ensure_directories():
    """Ensure all required output directories exist."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directories = [
        os.path.join(base_dir, "output", "cleaned_data"),
        os.path.join(base_dir, "output", "figures"),
        os.path.join(base_dir, "output", "tables"),
        os.path.join(base_dir, "output", "reports")
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def save_figure(filename: str):
    """Save the current matplotlib figure to the output/figures directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "output", "figures", filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
