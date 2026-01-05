"""
Industrial Anomaly Detection Script
-----------------------------------
Author: Ahmed Hussien
Role: Engineering Data Analyst

Purpose:
- Load industrial sensor time-series data
- Compute rolling statistics
- Detect abnormal operating conditions
- Save results for further analysis or reporting
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


# =========================
# Configuration
# =========================
DATA_PATH = Path("data/sensor_data.csv")
OUTPUT_PATH = Path("data/anomaly_results.csv")
ROLLING_WINDOW = 30          # samples (minutes)
Z_THRESHOLD = 3.0


# =========================
# Load Data
# =========================
def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    df = pd.read_csv(path, parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df


# =========================
# Feature Engineering
# =========================
def compute_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["current_mean"] = df["current_A"].rolling(ROLLING_WINDOW).mean()
    df["current_std"] = df["current_A"].rolling(ROLLING_WINDOW).std()

    df["temperature_mean"] = df["temperature_C"].rolling(ROLLING_WINDOW).mean()
    df["vibration_mean"] = df["vibration_mm_s"].rolling(ROLLING_WINDOW).mean()

    return df


# =========================
# Anomaly Detection
# =========================
def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["current_z"] = (
        (df["current_A"] - df["current_mean"]) / df["current_std"]
    )

    df["anomaly"] = (df["current_z"].abs() > Z_THRESHOLD).astype(int)

    return df

# =========================
# Plotting
# =========================
def save_anomaly_plot(df: pd.DataFrame, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 4))
    plt.plot(df.index, df["current_A"], label="Motor Current")

    anomalies = df[df["anomaly"] == 1]
    plt.scatter(
        anomalies.index,
        anomalies["current_A"],
        color="red",
        s=15,
        label="Detected Anomaly"
    )

    plt.legend()
    plt.title("Motor Current Anomaly Detection")
    plt.tight_layout()

    plot_path = output_dir / "current_anomalies.png"
    plt.savefig(plot_path)
    plt.close()

    print(f"Anomaly plot saved to: {plot_path}")

# =========================
# Main Pipeline
# =========================
def main():
    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Computing rolling statistics...")
    df = compute_rolling_features(df)

    print("Detecting anomalies...")
    df = detect_anomalies(df)
    
    print("Saving anomaly plot...")
    save_anomaly_plot(df, Path("reports"))


    print("Saving results...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH)

    anomaly_count = df["anomaly"].sum()
    print(f"Analysis complete. Detected {anomaly_count} anomalies.")
    print(f"Results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
