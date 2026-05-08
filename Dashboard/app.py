# ===============================
# 1. IMPORTS
# ===============================
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Spain Top 50 Analytics", layout="wide")

# ===============================
# 2. LOAD DATA
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("Data/Atlantic_Spain.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['song_id'] = df['song'] + " - " + df['artist']
    return df

df = load_data()

# ===============================
# 3. LIFECYCLE
# ===============================
@st.cache_data
def create_lifecycle(df):
    lifecycle = df.groupby('song_id').agg(
        entry_date=('date', 'min'),
        exit_date=('date', 'max'),
        days_on_playlist=('date', 'nunique'),
        peak_position=('position', 'min')
    ).reset_index()

    peak_dates = df[df['position'] == df.groupby('song_id')['position'].transform('min')] \
        .groupby('song_id')['date'].min().reset_index()

    peak_dates.columns = ['song_id', 'peak_date']

    lifecycle = lifecycle.merge(peak_dates, on='song_id')
    lifecycle['time_to_peak'] = (lifecycle['peak_date'] - lifecycle['entry_date']).dt.days

    return lifecycle

lifecycle = create_lifecycle(df)

# Merge
df = df.merge(lifecycle, on='song_id', how='left')

# ===============================
# 4. SIDEBAR FILTERS
# ===============================
st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df['date'].min(), df['date'].max()]
)

explicit_filter = st.sidebar.selectbox("Explicit", ["All", True, False])
album_filter = st.sidebar.selectbox("Album Type", ["All"] + list(df['album_type'].dropna().unique()))

# Apply filters
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['date'] >= pd.to_datetime(date_range[0])) &
        (filtered_df['date'] <= pd.to_datetime(date_range[1]))
    ]

if explicit_filter != "All":
    filtered_df = filtered_df[filtered_df['is_explicit'] == explicit_filter]

if album_filter != "All":
    filtered_df = filtered_df[filtered_df['album_type'] == album_filter]

# ===============================
# 5. TITLE
# ===============================
st.title("🎧 Spain Top 50 Playlist Analytics")

# ===============================
# 6. KPIs (FILTERED)
# ===============================
filtered_lifecycle = filtered_df[['song_id', 'days_on_playlist', 'time_to_peak', 'peak_position']].drop_duplicates()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Days", round(filtered_lifecycle['days_on_playlist'].mean(), 2))
col2.metric("Time to Peak", round(filtered_lifecycle['time_to_peak'].mean(), 2))
col3.metric("Avg Peak Pos", round(filtered_lifecycle['peak_position'].mean(), 2))
col4.metric("Total Songs", filtered_df['song_id'].nunique())

# ===============================
# 7. CHARTS
# ===============================

# Lifecycle
st.subheader("📊 Lifecycle Distribution")
st.bar_chart(filtered_lifecycle['days_on_playlist'].value_counts().sort_index())

# Time to Peak
st.subheader("⏱ Time to Peak")
st.bar_chart(filtered_lifecycle['time_to_peak'].value_counts().sort_index())

# Avg Position
st.subheader("📉 Avg Position Over Time")
avg_pos = filtered_df.groupby('date')['position'].mean()
st.line_chart(avg_pos)

# ===============================
# 8. REAL CHURN ANALYSIS
# ===============================
st.subheader("🔄 Playlist Churn")

daily_sets = filtered_df.groupby('date')['song_id'].apply(set)
dates = daily_sets.index

entries = []
for i in range(1, len(dates)):
    today = daily_sets.iloc[i]
    yesterday = daily_sets.iloc[i-1]
    entries.append(len(today - yesterday))

churn_series = pd.Series(entries, index=dates[1:])
st.line_chart(churn_series)

# ===============================
# 9. CONTENT ANALYSIS
# ===============================
st.subheader("🎼 Content Insights")

col1, col2 = st.columns(2)

col1.bar_chart(filtered_df.groupby('is_explicit')['days_on_playlist'].mean())
col2.bar_chart(filtered_df.groupby('album_type')['days_on_playlist'].mean())

# ===============================
# 10. TOP SONGS
# ===============================
st.subheader("🏆 Top Songs")
top_songs = filtered_lifecycle.sort_values('days_on_playlist', ascending=False).head(10)
st.dataframe(top_songs)

# ===============================
# 11. DOWNLOAD BUTTON
# ===============================
st.download_button(
    "Download Lifecycle Data",
    filtered_lifecycle.to_csv(index=False),
    "lifecycle.csv"
)

# ===============================
# 12. RAW DATA
# ===============================
st.subheader("📄 Raw Data")
st.dataframe(filtered_df.head(100))