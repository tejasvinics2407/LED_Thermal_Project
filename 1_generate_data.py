import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_luminaire_telemetry(
    luminaire_id="LUM-101",
    duration_hours=24,
    step_seconds=10
):

    # -----------------------------
    # Basic thermal parameters
    # -----------------------------

    base_ambient = 25.0
    thermal_resistance = 0.85
    thermal_time_constant = 300.0

    heatsink_temp = base_ambient

    # Start time
    start_time = datetime.now() - timedelta(
        hours=duration_hours
    )

    # Number of readings
    total_steps = int(
        (duration_hours * 3600) / step_seconds
    )

    records = []

    print("Generating telemetry...")
    print("Total readings to generate:", total_steps)

    # -----------------------------
    # Generate readings
    # -----------------------------

    for i in range(total_steps):

        # Timestamp
        current_time = (
            start_time
            + timedelta(seconds=i * step_seconds)
        )

        # -----------------------------
        # LED operating schedule
        # -----------------------------

        hour = current_time.hour

        if 8 <= hour <= 22:

            dimming = random.uniform(
                70.0,
                100.0
            )

        else:

            dimming = random.choice(
                [0.0, 10.0]
            )

        # -----------------------------
        # Electrical parameters
        # -----------------------------

        current = (
            dimming / 100.0
        ) * 1.5

        voltage = (
            48.0
            + random.uniform(-0.2, 0.2)
        )

        power = current * voltage

        # -----------------------------
        # Gradual thermal degradation
        # -----------------------------

        degradation_start = (
            total_steps * 0.5
        )

        if i > degradation_start:

            degradation_progress = (
                (i - degradation_start)
                /
                (total_steps - degradation_start)
            )

            current_thermal_resistance = (
                thermal_resistance
                * (
                    1
                    + 0.6
                    * degradation_progress
                )
            )

        else:

            current_thermal_resistance = (
                thermal_resistance
            )

        # -----------------------------
        # Ambient temperature
        # -----------------------------

        ambient_temp = (
            base_ambient
            + 3.0
            * np.sin(
                2
                * np.pi
                * i
                / total_steps
            )
            + random.uniform(
                -0.1,
                0.1
            )
        )

        # -----------------------------
        # Thermal calculation
        # -----------------------------

        temperature_change = (
            (
                power
                * current_thermal_resistance
                - (
                    heatsink_temp
                    - ambient_temp
                )
            )
            /
            (
                thermal_time_constant
                / step_seconds
            )
        )

        heatsink_temp += (
            temperature_change
            + random.uniform(
                -0.05,
                0.05
            )
        )

        # -----------------------------
        # Junction temperature
        # -----------------------------

        junction_temp = (
            heatsink_temp
            + (
                power
                * 0.75
                * 1.2
            )
        )

        # -----------------------------
        # Store record
        # -----------------------------

        records.append({

            "timestamp":
                current_time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "luminaire_id":
                luminaire_id,

            "ambient_temp":
                round(
                    ambient_temp,
                    2
                ),

            "heatsink_temp":
                round(
                    heatsink_temp,
                    2
                ),

            "junction_temp_true":
                round(
                    junction_temp,
                    2
                ),

            "current":
                round(
                    current,
                    3
                ),

            "voltage":
                round(
                    voltage,
                    2
                ),

            "power":
                round(
                    power,
                    2
                ),

            "dimming_pct":
                round(
                    dimming,
                    1
                )
        })

    # -----------------------------
    # Create DataFrame
    # -----------------------------

    df = pd.DataFrame(records)

    # -----------------------------
    # Save CSV
    # -----------------------------

    df.to_csv(
        "luminaire_telemetry.csv",
        index=False
    )

    print()
    print("Data generation completed!")
    print(
        f"Records generated: {len(df)}"
    )
    print(
        "File created: "
        "luminaire_telemetry.csv"
    )


# -----------------------------
# Start program
# -----------------------------

if __name__ == "__main__":
    generate_luminaire_telemetry()