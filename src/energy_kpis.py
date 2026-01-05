"""
Industrial Energy & KPI Analysis Script
--------------------------------------
Author: Ahmed Hussien
Role: Engineering Data Analyst

Purpose:
- Compute energy consumption and operational KPIs
- Analyze load behavior and peak demand
- Generate summary metrics for reporting
"""

import pandas as pd
from pathlib import Path


# =========================
# Configuration
# =========================
DATA_PATH = Path("data/sensor_data.csv")
OUTPUT_PATH = Path("data/energy_kpis.csv")

NOMINAL_VOLTAGE = 400          # Volts
POWER_FACTOR = 0.85            # assumed
SAMPLING_MINUTES = 1           # data resolution


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
# Energy Calculations
# =========================
def compute_power_energy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Instantaneous power (kW) – simplified three-phase approximation
    df["power_kW"] = (
        (df["voltage_V"] * df["current_A"] * POWER_FACTOR) / 1000
    )

    # Energy per sample (kWh)
    df["energy_kWh"] = df["power_kW"] * (SAMPLING_MINUTES / 60)

    return df


# =========================
# KPI Calculation
# =========================
def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    kpis = {
        "total_energy_kWh": df["energy_kWh"].sum(),
        "average_power_kW": df["power_kW"].mean(),
        "peak_power_kW": df["power_kW"].max(),
        "average_load_pct": df["load_pct"].mean(),
        "max_load_pct": df["load_pct"].max(),
        "average_temperature_C": df["temperature_C"].mean(),
        "average_vibration_mm_s": df["vibration_mm_s"].mean(),
        "operating_hours": len(df) * (SAMPLING_MINUTES / 60),
    }

    return pd.DataFrame([kpis])


# =========================
# Main Pipeline
# =========================
def main():
    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Computing power and energy...")
    df = compute_power_energy(df)

    print("Calculating KPIs...")
    kpi_df = compute_kpis(df)

    print("Saving KPI results...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    kpi_df.to_csv(OUTPUT_PATH, index=False)

    print("Energy & KPI analysis complete.")
    print(kpi_df)


if __name__ == "__main__":
    main()
