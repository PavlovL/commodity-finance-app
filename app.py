
import streamlit as st
import pandas as pd
import json
import os
import uuid

# File paths
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "deals.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize data file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# Load data
with open(DATA_FILE, "r") as f:
    try:
        deals = json.load(f)
    except json.JSONDecodeError:
        deals = []

# Utility function to save deals
def save_deals(deals):
    with open(DATA_FILE, "w") as f:
        json.dump(deals, f, indent=4)

# Sidebar: Add or Edit
st.sidebar.title("Manage Deal")
mode = st.sidebar.radio("Choose Action", ["Add Deal", "Edit Deal", "Delete Deal"])

# Add Deal
if mode == "Add Deal":
    st.sidebar.subheader("New Deal")
    commodity = st.sidebar.text_input("Commodity")
    volume = st.sidebar.number_input("Volume (tonnes)", min_value=0.0)
    price = st.sidebar.number_input("Price per tonne (USD)", min_value=0.0)
    buyer = st.sidebar.text_input("End Buyer")
    sblc_provider = st.sidebar.text_input("SBLC Provider")
    status = st.sidebar.selectbox("Status", ["Draft", "Approved", "Shipped", "Paid"])

    if st.sidebar.button("Save Deal"):
        new_deal = {
            "id": str(uuid.uuid4()),
            "commodity": commodity,
            "volume": volume,
            "price": price,
            "buyer": buyer,
            "sblc_provider": sblc_provider,
            "status": status
        }
        deals.append(new_deal)
        save_deals(deals)
        st.sidebar.success("Deal saved successfully.")

# Edit Deal
elif mode == "Edit Deal":
    deal_options = {f"{d['commodity']} to {d['buyer']}": d["id"] for d in deals}
    if deal_options:
        selection = st.sidebar.selectbox("Select deal to edit", list(deal_options.keys()))
        selected_id = deal_options[selection]
        selected_deal = next((d for d in deals if d["id"] == selected_id), None)

        if selected_deal:
            commodity = st.sidebar.text_input("Commodity", selected_deal["commodity"])
            volume = st.sidebar.number_input("Volume", value=selected_deal["volume"])
            price = st.sidebar.number_input("Price", value=selected_deal["price"])
            buyer = st.sidebar.text_input("End Buyer", selected_deal["buyer"])
            sblc_provider = st.sidebar.text_input("SBLC Provider", selected_deal["sblc_provider"])
            status = st.sidebar.selectbox("Status", ["Draft", "Approved", "Shipped", "Paid"], index=["Draft", "Approved", "Shipped", "Paid"].index(selected_deal["status"]))

            if st.sidebar.button("Update Deal"):
                selected_deal.update({
                    "commodity": commodity,
                    "volume": volume,
                    "price": price,
                    "buyer": buyer,
                    "sblc_provider": sblc_provider,
                    "status": status
                })
                save_deals(deals)
                st.sidebar.success("Deal updated successfully.")
    else:
        st.sidebar.info("No deals to edit.")

# Delete Deal
elif mode == "Delete Deal":
    deal_options = {f"{d['commodity']} to {d['buyer']}": d["id"] for d in deals}
    if deal_options:
        selection = st.sidebar.selectbox("Select deal to delete", list(deal_options.keys()))
        selected_id = deal_options[selection]

        if st.sidebar.button("Delete Deal"):
            deals = [d for d in deals if d["id"] != selected_id]
            save_deals(deals)
            st.sidebar.success("Deal deleted successfully.")
    else:
        st.sidebar.info("No deals to delete.")

# Display Dashboard
st.title("📦 Commodity Export Finance Deals")

if deals:
    df = pd.DataFrame(deals)
    df["value_usd"] = df["volume"] * df["price"]
    st.dataframe(df[["commodity", "volume", "price", "value_usd", "buyer", "sblc_provider", "status"]])
    st.metric("Total Deals", len(deals))
    st.metric("Total Value (USD)", f"${df['value_usd'].sum():,.2f}")
else:
    st.info("No deals found. Use the sidebar to add a deal.")
