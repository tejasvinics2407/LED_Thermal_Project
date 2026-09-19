import pandas as pd
import numpy as np

# 1. Load the generated telemetry data
df = pd.read_csv("luminaire_telemetry.csv")

# Convert timestamp into datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort data by time
df = df.sort_values("timestamp").reset_index(drop=True)

print("Original records:", len(df))

# 2. Feature Engineering

# Temperature change between consecutive readings
df["dT_dt"] = df["heatsink_temp"].diff()

# Difference between heat sink and ambient temperature
df["delta_T_ambient"] = (
    df["heatsink_temp"] - df["ambient_temp"]
)

# Rolling average of heat sink temperature
# 30 readings × 10 seconds = 5 minutes
df["heatsink_rolling_avg"] = (
    df["heatsink_temp"]
    .rolling(window=30)
    .mean()
)

# Rolling average of power
df["power_rolling_avg"] = (
    df["power"]
    .rolling(window=30)
    .mean()
)

# 3. Create the ML target
# 90 readings × 10 seconds = 15 minutes
FORECAST_STEPS = 90

df["target_junction_temp_15m"] = (
    df["junction_temp_true"].shift(-FORECAST_STEPS)
)

# 4. Remove rows containing incomplete values
df_clean = df.dropna().reset_index(drop=True)

print("Processed records:", len(df_clean))

# 5. Save the processed dataset
df_clean.to_csv(
    "processed_telemetry.csv",
    index=False
)

print("Preprocessing completed!")
print("File created: processed_telemetry.csv")

# Display important columns
print("\nProcessed data preview:")
print(
    df_clean[
        [
            "timestamp",
            "ambient_temp",
            "heatsink_temp",
            "dT_dt",
            "delta_T_ambient",
            "heatsink_rolling_avg",
            "power_rolling_avg",
            "target_junction_temp_15m"
        ]
    ].head()
)