import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib

# 1. Load processed data
df = pd.read_csv("processed_telemetry.csv")

print("Processed data loaded successfully.")
print("Total records:", len(df))

# 2. Select input features
features = [
    "ambient_temp",
    "heatsink_temp",
    "current",
    "voltage",
    "power",
    "dimming_pct",
    "dT_dt",
    "delta_T_ambient",
    "heatsink_rolling_avg",
    "power_rolling_avg"
]

# Input data
X = df[features]

# Target = junction temperature 15 minutes in the future
y = df["target_junction_temp_15m"]

# 3. Train/Test split
# First 80% = training
# Last 20% = testing
split_index = int(len(X) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# 4. Create XGBoost model
model = XGBRegressor(
    n_estimators=150,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

# 5. Train the model
print("\nTraining XGBoost model...")

model.fit(X_train, y_train)

print("Model training completed!")

# 6. Make predictions
predictions = model.predict(X_test)

# 7. Evaluate model

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

mae = mean_absolute_error(
    y_test,
    predictions
)

print("\n========== MODEL PERFORMANCE ==========")
print(f"RMSE: {rmse:.3f} °C")
print(f"MAE : {mae:.3f} °C")
print("========================================")

# 8. Show some predictions
print("\nSample predictions:")

for actual, predicted in zip(
    y_test.iloc[:10],
    predictions[:10]
):
    print(
        f"Actual: {actual:.2f} °C"
        f" | Predicted: {predicted:.2f} °C"
    )

# 9. Save trained model
joblib.dump(
    model,
    "thermal_prediction_xgb.joblib"
)

print("\nTrained model saved as:")
print("thermal_prediction_xgb.joblib")