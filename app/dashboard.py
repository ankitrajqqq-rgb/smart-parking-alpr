import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Smart Parking Dashboard", layout="wide")

st.title("🚗 AI Smart Parking System Dashboard")

# Connect DB
conn = sqlite3.connect("parking.db")

# Load data
df = pd.read_sql_query("SELECT * FROM parking", conn)

# ------------------ METRICS ------------------

total_vehicles = len(df)

active_vehicles = df[df["exit_time"].isnull()].shape[0]

total_revenue = df["amount"].fillna(0).sum()

# USER INPUT (same as system)
total_slots = st.number_input("Total Parking Slots", min_value=1, value=10)

available_slots = total_slots - active_vehicles

# ------------------ DISPLAY ------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("🚗 Total Vehicles", total_vehicles)
col2.metric("🅿️ Occupied Slots", active_vehicles)
col3.metric("✅ Available Slots", available_slots)
col4.metric("💰 Total Revenue (₹)", round(total_revenue, 2))

st.divider()

# ------------------ TABLE ------------------

st.subheader("📋 Parking Records")

st.dataframe(df, use_container_width=True)

# ------------------ REFRESH ------------------

if st.button("🔄 Refresh"):
    st.rerun()