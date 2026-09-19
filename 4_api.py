from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(
    title="LED Thermal Monitoring API"
)

# Load the trained ML model
try:
    model = joblib.load(
        "thermal_prediction_xgb.joblib"
    )
    print("ML model loaded successfully!")

except Exception as e:
    model = None
    print("Model could not be loaded:", e)


# Data received by the API
class TelemetryPayload(BaseModel):

    luminaire_id: str

    ambient_temp: float
    heatsink_temp: float

    current: float
    voltage: float

    dimming_pct: float

    dT_dt: float

    heatsink_rolling_avg: float
    power_rolling_avg: float


# Prediction endpoint
@app.post("/api/v1/predict")
def predict_thermal_status(
    payload: TelemetryPayload
):

    # Check whether model is available
    if model is None:

        raise HTTPException(
            status_code=500,
            detail="ML model not loaded."
        )

    # Calculate electrical power
    power = (
        payload.current
        * payload.voltage
    )

    # Temperature difference
    delta_T_ambient = (
        payload.heatsink_temp
        - payload.ambient_temp
    )

    # Create input for ML model
    input_features = pd.DataFrame([
        {
            "ambient_temp":
                payload.ambient_temp,

            "heatsink_temp":
                payload.heatsink_temp,

            "current":
                payload.current,

            "voltage":
                payload.voltage,

            "power":
                power,

            "dimming_pct":
                payload.dimming_pct,

            "dT_dt":
                payload.dT_dt,

            "delta_T_ambient":
                delta_T_ambient,

            "heatsink_rolling_avg":
                payload.heatsink_rolling_avg,

            "power_rolling_avg":
                payload.power_rolling_avg
        }
    ])

    # Ask ML model for prediction
    predicted_temp = float(
        model.predict(input_features)[0]
    )

    # -----------------------------
    # Alert system
    # -----------------------------

    if predicted_temp >= 105:

        alert_status = "CRITICAL"

        action = (
            "Reduce power immediately "
            "or switch off the luminaire."
        )

    elif predicted_temp >= 85:

        alert_status = "WARNING"

        action = (
            "Reduce power to maintain "
            "thermal safety."
        )

    else:

        alert_status = "NORMAL"

        action = "No action required."

    # Return result
    return {

        "luminaire_id":
            payload.luminaire_id,

        "current_heatsink_temp":
            round(
                payload.heatsink_temp,
                2
            ),

        "predicted_junction_temp_15m":
            round(
                predicted_temp,
                2
            ),

        "alert_status":
            alert_status,

        "recommended_action":
            action
    }


# Start the server
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )