# ===============================
# 1. IMPORT LIBRARIES
# ===============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ===============================
# 2. SETUP OUTPUT FOLDERS
# ===============================
os.makedirs("outputs/charts", exist_ok=True)

# ===============================
# 3. LOAD DATA
# ===============================
df = pd.read_csv("data/Atlantic_Spain.csv")
df['date'] = pd.to_datetime(df['date'])

# ===============================
# 4. DATA CLEANING
# ===============================
df = df.drop_duplicates(subset=['date', 'song', 'artist'])
df['song_id'] = df['song'] + " - " + df['artist']

# Validate playlist size
daily_counts = df.groupby('date').size()
print("Daily counts check:\n", daily_counts.value_counts())

# ===============================
# 5. LIFECYCLE CREATION
# ===============================
lifecycle = df.groupby('song_id').agg(
    entry_date=('date', 'min'),
    exit_date=('date', 'max'),
    days_on_playlist=('date', 'nunique'),
    peak_position=('position', 'min')
).reset_index()

# Merge lifecycle
df = df.merge(lifecycle, on='song_id', how='left')

# ===============================
# 6. TIME TO PEAK
# ===============================
peak_dates = df[df['position'] == df['peak_position']] \
    .groupby('song_id')['date'].min().reset_index()

peak_dates.columns = ['song_id', 'peak_date']

lifecycle = lifecycle.merge(peak_dates, on='song_id')
lifecycle['time_to_peak'] = (lifecycle['peak_date'] - lifecycle['entry_date']).dt.days

# ===============================
# 7. IMPROVED LIFECYCLE STAGE
# ===============================
df = df.sort_values(['song_id', 'date'])

df['prev_position'] = df.groupby('song_id')['position'].shift(1)

def classify_stage(row):
    days = (row['date'] - row['entry_date']).days

    if days <= 7:
        return 'New'
    elif row['position'] <= 10:
        return 'Peak'
    elif pd.notnull(row['prev_position']) and row['position'] < row['prev_position']:
        return 'Growth'
    elif row['position'] <= 25:
        return 'Mature'
    else:
        return 'Decline'

df['lifecycle_stage'] = df.apply(classify_stage, axis=1)

# ===============================
# 8. TRUE CHURN ANALYSIS
# ===============================
df = df.sort_values('date')

daily_song_sets = df.groupby('date')['song_id'].apply(set)

dates = daily_song_sets.index

entries = []
exits = []

for i in range(1, len(dates)):
    today = daily_song_sets.iloc[i]
    yesterday = daily_song_sets.iloc[i-1]

    entries.append(len(today - yesterday))
    exits.append(len(yesterday - today))

churn_df = pd.DataFrame({
    'date': dates[1:],
    'entries': entries,
    'exits': exits
})

churn_df['churn_rate'] = churn_df['entries'] / 50

# ===============================
# 9. CONTENT ANALYSIS
# ===============================
explicit_analysis = df.groupby('is_explicit')['days_on_playlist'].mean()
album_analysis = df.groupby('album_type')['days_on_playlist'].mean()

df['duration_bin'] = pd.qcut(df['duration_ms'], 4, duplicates='drop')
duration_analysis = df.groupby('duration_bin')['days_on_playlist'].mean()

# ===============================
# 10. KPI CALCULATION
# ===============================
kpis = {
    "Avg Days": lifecycle['days_on_playlist'].mean(),
    "Avg Time to Peak": lifecycle['time_to_peak'].mean(),
    "Avg Peak Position": lifecycle['peak_position'].mean(),
    "Avg Churn Rate": churn_df['churn_rate'].mean()
}

print("\nKPIs:\n", kpis)

# ===============================
# 11. VISUALIZATIONS
# ===============================

# Lifecycle Distribution
plt.figure()
lifecycle['days_on_playlist'].hist()
plt.title("Lifecycle Distribution")
plt.savefig("outputs/charts/lifecycle_distribution.png")
plt.show()

# Time to Peak
plt.figure()
lifecycle['time_to_peak'].hist()
plt.title("Time to Peak")
plt.savefig("outputs/charts/time_to_peak.png")
plt.show()

# Avg Position Over Time
plt.figure()
df.groupby('date')['position'].mean().plot()
plt.title("Avg Position Over Time")
plt.savefig("outputs/charts/avg_position.png")
plt.show()

# Churn Rate
plt.figure()
plt.plot(churn_df['date'], churn_df['churn_rate'])
plt.title("Churn Rate")
plt.savefig("outputs/charts/churn_rate.png")
plt.show()

# Explicit vs Clean
plt.figure()
explicit_analysis.plot(kind='bar')
plt.title("Explicit vs Clean")
plt.savefig("outputs/charts/explicit_vs_clean.png")
plt.show()

# Album vs Single
plt.figure()
album_analysis.plot(kind='bar')
plt.title("Album vs Single")
plt.savefig("outputs/charts/album_vs_single.png")
plt.show()

# ===============================
# 12. SAVE OUTPUTS
# ===============================
lifecycle.to_csv("outputs/src/lifecycle_summary.csv", index=False)
df.to_csv("outputs/src/processed_data.csv", index=False)
churn_df.to_csv("outputs/src/churn_analysis.csv", index=False)

print("Completed Successfully")