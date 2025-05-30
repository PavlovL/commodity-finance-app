import streamlit as st
import pandas as pd
import json
import os

DATA_FILE = "data/deals.json"

st.set_page_config(page_title="Commodity Export Finance Fund", layout="wide")
st.title("📦 Commodity Export Finance Fund")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

with open(DATA_FILE, "r") as f:
    deals = json.load(f)

st.sidebar.header("Add New Deal")
with st.sidebar.form("deal_form", clear_on_submit=True):
    name = st.text_input("Deal Name")
    commodity = st.text_input("Commodity")
    volume = st.number_input("Volume (MT)", step=1.0)
    price = st.number_input("Unit Price (USD/MT)", step=0.1)
    end_buyer = st.text_input("End Buyer")
    sblc_provider = st.text_input("SBLC Provider")
    status = st.selectbox("Status", ["Draft", "SBLC Issued", "Monetized", "Exported", "Paid"])
    submitted = st.form_submit_button("Add Deal")

    if submitted:
        deals.append({
            "name": name,
            "commodity": commodity,
            "volume": volume,
            "price": price,
            "end_buyer": end_buyer,
            "sblc_provider": sblc_provider,
            "status": status
        })
        with open(DATA_FILE, "w") as f:
            json.dump(deals, f, indent=2)
        st.success("Deal added!")

st.subheader("📊 Deal Overview")
if deals:
    df = pd.DataFrame(deals)
    df["Value (USD)"] = df["volume"] * df["price"]
    st.dataframe(df)
    st.metric("Total Deals", len(df))
    st.metric("Total Value (USD)", f"${df['Value (USD)'].sum():,.2f}")
else:
    st.info("No deals added yet.")
