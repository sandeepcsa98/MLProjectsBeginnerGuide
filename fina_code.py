import pandas as pd
import numpy as np

n_samples = 1000

# Calculate sync drift (difference between Stream A and Stream B)


# Generate input features
df = pd.DataFrame({
    'encoder_latency_ms_A': np.random.uniform(30, 80, n_samples),
    'cpu_usage_percent_A': np.random.uniform(40, 90, n_samples),
    'packet_loss_percent_A': np.random.uniform(0, 3, n_samples),
    'jitter_ms_A': np.random.uniform(2, 8, n_samples),
    'current_fps_A': np.random.choice([30, 60], n_samples),
    'current_resolution_A': np.random.choice([2, 3], n_samples),  # 2=1080p, 3=4K
    'avg_interval_A_ms' : np.random.uniform(15, 40, n_samples),

    'encoder_latency_ms_B': np.random.uniform(40, 100, n_samples),
    'cpu_usage_percent_B': np.random.uniform(50, 95, n_samples),
    'packet_loss_percent_B': np.random.uniform(2, 7, n_samples),
    'jitter_ms_B': np.random.uniform(5, 12, n_samples),
    'current_fps_B': np.random.choice([15, 24], n_samples),
    'current_resolution_B': np.random.choice([0, 1], n_samples),  # 0=480p, 1=720p
    'avg_interval_B_ms' : np.random.uniform(30, 70, n_samples),

    'network_latency_ms': np.random.uniform(50, 120, n_samples)
})

# Calculate sync_drift_ms as the absolute difference between the intervals of Stream A and Stream B
df['sync_drift_ms'] = np.abs(df['avg_interval_A_ms'] - df['avg_interval_B_ms'])

# Define logic for targets
def decide_adjustments(row, stream='A'):
    if stream == 'A':
        if row['encoder_latency_ms_A'] > 60 or row['cpu_usage_percent_A'] > 75:
            return 30, 1500, 2  # drop to 30fps, 1080p
        else:
            return 60, 3000, 3  # stay at high
    else:
        if row['encoder_latency_ms_B'] > 70 or row['cpu_usage_percent_B'] > 85 or row['jitter_ms_B'] > 10:
            return 15, 1000, 0  # drop to 480p
        else:
            return 24, 1800, 1  # keep at 720p

# Apply logic
adjustments_A = df.apply(lambda row: decide_adjustments(row, 'A'), axis=1)
adjustments_B = df.apply(lambda row: decide_adjustments(row, 'B'), axis=1)

df[['adjust_fps_A', 'adjust_bitrate_kbps_A', 'adjust_resolution_A']] = pd.DataFrame(adjustments_A.tolist(), index=df.index)
df[['adjust_fps_B', 'adjust_bitrate_kbps_B', 'adjust_resolution_B']] = pd.DataFrame(adjustments_B.tolist(), index=df.index)

# Save to CSV
df.to_csv("heterogeneous_stream_dataset_v2.csv", index=False)
print("✅ Smart dataset generated and saved as 'heterogeneous_stream_dataset_v2.csv'")

