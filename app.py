import streamlit as st
import pandas as pd
import re
from collections import Counter

# Load log data
def load_logs(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines

# Parse logs into structured data
def parse_logs(log_lines):
    data = []
    for line in log_lines:
        parts = line.strip().split()
        timestamp = f"{parts[0]} {parts[1]}"
        status = parts[2]
        message = " ".join(parts[3:])
        ip_match = re.search(r"IP (\d+\.\d+\.\d+\.\d+)", line)
        ip = ip_match.group(1) if ip_match else "Unknown"
        data.append({"Timestamp": timestamp, "Status": status, "Message": message, "IP": ip})
    return pd.DataFrame(data)

# Load and parse logs
log_lines = load_logs("sample_logs.txt")
df = parse_logs(log_lines)

# Streamlit dashboard
st.title("🔐 Mini SIEM Dashboard")
st.write("A simple dashboard to visualize login activity from logs.")

# Metrics
st.metric("Total Events", len(df))
st.metric("Failed Logins", sum(df["Status"] == "ERROR"))
st.metric("Successful Logins", sum(df["Status"] == "INFO"))

# Top IPs
top_ips = Counter(df["IP"])
st.subheader("📊 Top IPs by Activity")
st.bar_chart(pd.DataFrame.from_dict(top_ips, orient="index", columns=["Count"]))

# Timeline
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
st.subheader("🕒 Event Timeline")
st.line_chart(df["Timestamp"].value_counts().sort_index())
