import streamlit as st
import requests
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="LED Thermal Monitoring",
    page_icon="💡",
    layout="wide"
)

st.title("💡 LED Thermal Monitoring & Predictive Maintenance")
st.write("Real-time thermal monitoring and 15-minute temperature prediction")

st.divider()

# -----------------------------
# INPUT SECTION
# -----------------------------

st.subheader("🔧 Luminaire Sensor Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    luminaire_id = st.text_input("Luminaire ID", "LUM-101")
    ambient_temp = st.number_input(
        "Ambient Temperature (°C)",
        value=30.0
    )
    heatsink_temp = st.number_input(
        "Heat Sink Temperature (°C)",
        value=80.0
    )

with col2:
    current = st.number_input(
        "Current (A)",
        value=1.4
    )
    voltage = st.number_input(
        "Voltage (V)",
        value=48.0
    )
    dimming_pct = st.number_input(
        "Dimming (%)",
        value=90.0,
        min_value=0.0,
        max_value=100.0
    )

with col3:
    dT_dt = st.number_input(
        "Temperature Change (dT/dt)",
        value=0.5
    )
    heatsink_rolling_avg = st.number_input(
        "Heat Sink Rolling Average (°C)",
        value=78.0
    )
    power_rolling_avg = st.number_input(
        "Power Rolling Average (W)",
        value=65.0
    )

# Calculate power
power = current * voltage

st.info(f"⚡ Calculated Electrical Power: **{power:.2f} W**")

st.divider()

# -----------------------------
# PREDICTION BUTTON
# -----------------------------

if st.button("🔮 Predict Thermal Status", type="primary"):

    # Data sent to FastAPI
    payload = {
        "luminaire_id": luminaire_id,
        "ambient_temp": ambient_temp,
        "heatsink_temp": heatsink_temp,
        "current": current,
        "voltage": voltage,
        "dimming_pct": dimming_pct,
        "dT_dt": dT_dt,
        "heatsink_rolling_avg": heatsink_rolling_avg,
        "power_rolling_avg": power_rolling_avg
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/predict",
            json=payload
        )

        if response.status_code == 200:

            result = response.json()

            predicted_temp = result["predicted_junction_temp_15m"]
            alert_status = result["alert_status"]
            action = result["recommended_action"]

            st.success("Prediction completed successfully!")

            st.divider()

            # -----------------------------
            # RESULTS
            # -----------------------------

            st.subheader("📊 Thermal Prediction")

            r1, r2, r3 = st.columns(3)

            with r1:
                st.metric(
                    "Heat Sink Temperature",
                    f"{heatsink_temp:.2f} °C"
                )

            with r2:
                st.metric(
                    "Predicted Junction Temperature",
                    f"{predicted_temp:.2f} °C"
                )

            with r3:
                st.metric(
                    "Electrical Power",
                    f"{power:.2f} W"
                )

            st.divider()

            # -----------------------------
            # ALERT
            # -----------------------------

            st.subheader("🚨 Thermal Status")

            if alert_status == "CRITICAL":

                st.error(
                    f"🚨 CRITICAL\n\n"
                    f"Predicted temperature: {predicted_temp:.2f} °C"
                )

            elif alert_status == "WARNING":

                st.warning(
                    f"⚠️ WARNING\n\n"
                    f"Predicted temperature: {predicted_temp:.2f} °C"
                )

            else:

                st.success(
                    f"✅ NORMAL\n\n"
                    f"Predicted temperature: {predicted_temp:.2f} °C"
                )

            st.write("### Recommended Action")
            st.info(action)

            st.divider()

            # -----------------------------
            # INPUT SUMMARY
            # -----------------------------

            st.subheader("📋 Current Telemetry")

            telemetry = pd.DataFrame({
                "Parameter": [
                    "Luminaire ID",
                    "Ambient Temperature",
                    "Heat Sink Temperature",
                    "Current",
                    "Voltage",
                    "Power",
                    "Dimming"
                ],
                "Value": [
                    luminaire_id,
                    f"{ambient_temp:.2f} °C",
                    f"{heatsink_temp:.2f} °C",
                    f"{current:.2f} A",
                    f"{voltage:.2f} V",
                    f"{power:.2f} W",
                    f"{dimming_pct:.1f} %"
                ]
            })

            st.table(telemetry)

        else:

            st.error(
                f"API Error: {response.status_code}\n\n"
                f"{response.text}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to the FastAPI backend.\n\n"
            "Make sure 4_api.py is running in another terminal."
        )

# --------------------------------
# TEMPERATURE HISTORY
# --------------------------------

st.divider()

st.subheader("📈 Temperature History")

try:
    history_df = pd.read_csv("luminaire_telemetry.csv")

    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])

    history_df = history_df.tail(100)

    st.line_chart(
        history_df.set_index("timestamp")[
            ["ambient_temp", "heatsink_temp"]
        ]
    )

except Exception as e:
    st.error(f"Could not load temperature history: {e}")