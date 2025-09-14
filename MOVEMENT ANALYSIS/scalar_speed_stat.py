import h5py
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

filename = r'path/to/your/file.h5'
target_ID = 'Your_Sensor_ID' # Sensor ID for the Head

if not os.path.exists(filename):
    print(f"File '{filename}' not found in the current directory.")
    print("Please upload your H5 file to proceed.")
    filename = None 

if filename:

    with h5py.File(filename, 'r') as f:
        if target_ID not in f['Sensors']:
            raise KeyError(f"Sensor ID {target_ID} not found. Available IDs: {list(f['Sensors'].keys())}")

        base_path = f'Sensors/{target_ID}'
        if 'Accelerometer' not in f[base_path] or 'Time' not in f[base_path]:
            raise KeyError(f"Missing Accelerometer or Time data for Sensor {target_ID}")

        acc_data = np.array(f[f'{base_path}/Accelerometer'][:], dtype=np.float64)
        time_raw = np.array(f[f'{base_path}/Time'][:], dtype=np.float64)
        time_dt = np.array([datetime.datetime.fromtimestamp(t * 1e-6) for t in time_raw])

    # Convert to seconds relative to start
    time_sec = (time_raw - time_raw[0]) * 1e-6 
    delta_t = np.gradient(time_sec)

    # Magnitude of acceleration
    acc_mag = np.linalg.norm(acc_data, axis=1)

    # Integrate (approximate) to estimate scalar speed
    speed_est = np.cumsum(acc_mag * delta_t)

    df = pd.DataFrame({'timestamp': time_dt, 'speed_est': speed_est}).set_index('timestamp')

    # Epoch-based stats
    epoch_features = df['speed_est'].resample('30s').agg(['mean', 'std', 'min', 'max']).dropna()

    if epoch_features.empty:
        raise ValueError("No data available to calculate epoch statistics.")

    print("\n--- Estimated Scalar Speed Stats ---")
    print(epoch_features.head())

    output_csv_name = f"{os.path.splitext(filename)[0]}_speed_stats.csv"
    epoch_features.to_csv(output_csv_name)
    print(f"\nSaved speed statistics to {output_csv_name}")

    # --- Plot ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(15, 7))

    plt.plot(epoch_features.index, epoch_features['mean'], label='Mean Estimated Speed', color='darkorange')

    plt.fill_between(epoch_features.index,
                     epoch_features['min'],
                     epoch_features['max'],
                     color='moccasin',
                     alpha=0.5,
                     label='Min-Max Range')

    plt.title('Estimated Scalar Speed Over Time', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Estimated Speed (m/s)', fontsize=12)

    # ✅ Format x-axis with time only + rotate ticks
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)

    plt.legend()
    plt.tight_layout()

    output_plot_name = f"{os.path.splitext(filename)[0]}_speed_plot.png"
    plt.savefig(output_plot_name)
    print(f"Successfully generated and saved {output_plot_name}")

