# 📦 Commodity Export Finance Fund App

This is a Streamlit web application that helps structure and track trade finance deals for commodity exports from Zimbabwe. The app is built to support a fund-based model where investors and stakeholders can monitor transactions involving SBLC-backed exports.

## 🌍 Purpose

Zimbabwe faces challenges in securing pre-export financing due to limited credit facilities and perceived country risk. This app demonstrates a structured finance solution using cash-backed Standby Letters of Credit (SBLCs) to:

- Unlock capital for exporters
- Reduce counterparty risk
- Improve transparency and deal tracking
- Provide fund managers with centralized visibility on deals

## ✅ Features

- Add and manage export deals (commodity, volume, price, buyer, SBLC provider, etc.)
- Automatic calculation of deal value (USD)
- Track deal status from Draft to Paid
- Dynamic dashboard showing total number and value of deals

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – App framework
- [Pandas](https://pandas.pydata.org/) – Data manipulation
- [JSON](https://www.json.org/) – Lightweight deal storage

## 🚀 How to Run Locally

```bash
git clone https://github.com/PavlovL/commodity-finance-app.git
cd commodity-finance-app
pip install -r requirements.txt
streamlit run app.py
