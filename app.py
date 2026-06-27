import streamlit as st
from datetime import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt

# Core imports
from decision_records.decision_record import load_decisions, learn_from_outcomes

st.subheader("🔁 Learning Loop & Approval")

# Show current weight if it exists
try:
    with open("weights.json", "r") as f:
        current_weights = json.load(f)
        st.caption(f"Current w1: {current_weights.get('w1', 25)}")
except:
    st.caption("Current w1: 25 (default)")

decisions = load_decisions()
if decisions:
    learning = learn_from_outcomes()
    st.json(learning)
    
    if "Increase w1" in learning.get("recommendation", ""):
        if st.button("✅ Approve & Apply w1 Increase"):
            new_w1 = 31
            with open("weights.json", "w") as f:
                json.dump({"w1": new_w1}, f)
            st.success(f"w1 increased to {new_w1} and saved persistently.")
            with open("logs/audit.log", "a") as f:
                f.write(f"{datetime.now()} | Approved w1 increase to {new_w1}\n")
else:
    st.info("Run test cycles first to generate data")
