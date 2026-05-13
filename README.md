# 📱 PhonePe Pulse Dashboard — India UPI Transaction Analytics (2018–2023)

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Folium](https://img.shields.io/badge/Folium-Maps-77B829?style=for-the-badge&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-Deployed-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/cloud)

> **A comprehensive interactive web dashboard for analysing PhonePe's UPI transaction data across India from 2018 to 2023 — covering transactions, insurance, and user behaviour, built on a real ETL pipeline from the PhonePe Pulse public data repository.**

🌐 **Live Demo:** [https://phonepe-web-dashboard.streamlit.app/](https://phonepe-web-dashboard.streamlit.app/)

📦 **Data Source:** [PhonePe Pulse — Official Public Data Repository](https://github.com/PhonePe/pulse)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Business Context](#business-context)
- [Data Pipeline](#data-pipeline)
- [Dashboard Features](#dashboard-features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started (Local)](#getting-started-local)
- [Deployment on Streamlit Cloud](#deployment-on-streamlit-cloud)
- [Data Coverage](#data-coverage)
- [License](#license)

---

## 🧭 Overview

This project is a **full end-to-end data analytics application** built around the official **PhonePe Pulse** public dataset — one of India's largest open fintech datasets, covering UPI transactions across all 28 states and 8 union territories from 2018 to 2023.

Unlike typical projects that just load a CSV file, this project implements a genuine **ETL (Extract, Transform, Load) pipeline**:

1. **Extract** — Clones and reads raw JSON data directly from the PhonePe Pulse GitHub repository using `GitPython`
2. **Transform** — Parses, flattens, and reshapes nested JSON structures into structured DataFrames
3. **Load** — Cleans and prepares the data for interactive visual analysis
4. **Visualise** — Serves insights through an interactive Streamlit dashboard with geographic maps and time-series charts

---

## 💼 Business Context

PhonePe is one of India's largest UPI payment platforms, processing hundreds of millions of transactions monthly. Understanding its growth across states, districts, and time periods helps:

- **Policymakers** track digital payment adoption across India
- **Business analysts** identify high-growth regions for expansion
- **Product teams** understand user engagement and insurance adoption patterns
- **Investors** gauge UPI market penetration and growth trajectories

This dashboard makes that analysis accessible and interactive for any stakeholder.

---

## 🔄 Data Pipeline

```
PhonePe Pulse GitHub Repository
(Public JSON data — transactions, users, insurance)
              │
              ▼
┌─────────────────────────────┐
│  Data Extraction            │
│  GitPython clones the repo  │
│  JSON files parsed per      │
│  state / district / quarter │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Data Transformation        │
│  Nested JSON → flat DataFrames│
│  State/District/Quarter     │
│  aggregations               │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Data Cleaning              │
│  Type casting, null handling│
│  Renaming, formatting       │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Streamlit Dashboard        │
│  Interactive filters,       │
│  Plotly charts, Folium maps │
└─────────────────────────────┘
```

---

## ✨ Dashboard Features

### 🗺️ Geographic Visualisation
- **India Choropleth Map** — State-level transaction volumes and user counts rendered on an interactive Folium map
- **District-level drilldown** — Zoom into specific states to explore district-level UPI adoption

### 📊 Transaction Analysis
- **Transaction Volume Trends** — Total UPI transaction count and value over time (2018–2023)
- **State-wise Comparison** — Bar and choropleth charts comparing transaction volumes across all Indian states
- **Quarterly Breakdown** — Transaction trends by quarter to identify seasonality and growth patterns
- **Transaction Type Split** — Peer-to-peer vs merchant payments vs others

### 👤 User Behaviour Analysis
- **Registered Users Growth** — State-wise and national growth in registered PhonePe users
- **App Opens Trends** — User engagement measured by app opens over time
- **User Segmentation** — Breakdown by device type, region, and engagement level

### 🛡️ Insurance Analysis
- **Insurance Policy Trends** — PhonePe insurance product adoption by state and quarter
- **Premium Value Analysis** — Total premium value trends over time
- **State Coverage Map** — Geographic spread of insurance products across India

### 🎛️ Interactive Controls
- **Year & Quarter filters** — Slice data by any year (2018–2023) and quarter
- **State selector** — Focus on any individual Indian state or view all-India data
- **Metric toggle** — Switch between transaction count, transaction value, and user metrics
- **Dynamic charts** — All visualisations update in real-time based on filter selections

---

## 📁 Project Structure

```
Phonepe-Dashboard-App/
├── Data/                               # Processed/cleaned data files
├── Phonepe-pulse-master/               # Cloned PhonePe Pulse raw data (JSON)
│   ├── data/
│   │   ├── aggregated/
│   │   │   ├── transaction/            # State-level transaction JSON
│   │   │   ├── user/                   # State-level user JSON
│   │   │   └── insurance/              # State-level insurance JSON
│   │   └── map/
│   │       ├── transaction/            # District-level transaction JSON
│   │       └── user/                   # District-level user JSON
├── assets/                             # Static assets (images, icons)
├── Data Extraction & Transformation.ipynb  # ETL pipeline notebook
├── Data Cleaning.ipynb                 # Data cleaning & preprocessing notebook
├── Phonepe-Webapp.py                   # Main Streamlit application
├── requirements.txt                    # Python dependencies (pinned versions)
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Technology | Version |
|---|---|---|
| **Language** | Python | 3.x |
| **Web Framework** | Streamlit | 1.34.0 |
| **Data Manipulation** | Pandas | 2.2.2 |
| **Numerical Computing** | NumPy | 1.26.4 |
| **Interactive Charts** | Plotly | 5.22.0 |
| **Geographic Maps** | Folium | 0.16.0 |
| **Data Format** | PyArrow | 16.0.0 |
| **Git-based Data Extract** | GitPython | 3.1.43 |
| **Map Tiles** | xyzservices | 2024.4.0 |
| **Deployment** | Streamlit Cloud | — |

---

## ✅ Prerequisites

- Python 3.8 or higher
- `pip` package manager
- Git (required for PhonePe Pulse data extraction via GitPython)

---

## 🚀 Getting Started (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/Kishores2801/Phonepe-Dashboard-App.git
cd Phonepe-Dashboard-App
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the ETL Pipeline (First Time Setup)

Open and run the notebooks in order:

```bash
pip install jupyter
jupyter notebook
```

Run in order:
1. `Data Extraction & Transformation.ipynb` — extracts raw JSON from PhonePe Pulse
2. `Data Cleaning.ipynb` — cleans and prepares data for the dashboard

### 5. Launch the Dashboard

```bash
streamlit run Phonepe-Webapp.py
```

Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## ☁️ Deployment on Streamlit Cloud

This app is deployed on **Streamlit Community Cloud** for free, public access.

To deploy your own instance:

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Set the main file path to `Phonepe-Webapp.py`
5. Click **Deploy** — Streamlit handles the rest

> ✅ Streamlit Cloud automatically installs dependencies from `requirements.txt` on each deploy.

---

## 📊 Data Coverage

| Dimension | Coverage |
|---|---|
| **Time Period** | 2018 Q1 → 2023 Q4 (6 years) |
| **Geographic Coverage** | All 28 states + 8 union territories of India |
| **Data Categories** | Transactions, Users, Insurance |
| **Granularity** | State-level & District-level |
| **Transaction Types** | P2P, P2M, Recharge & Bill Payments, Financial Services, Others |
| **Data Source** | PhonePe Pulse (Official public GitHub repository) |

---

## 📄 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

Data is sourced from the [PhonePe Pulse](https://github.com/PhonePe/pulse) public repository, licensed under [CDLA-Permissive-2.0](https://cdla.dev/permissive-2-0/).

---

<div align="center">

Built with 🐍 Python · 📊 Plotly · 🗺️ Folium · ⚡ Streamlit

**[🌐 View Live Dashboard](https://phonepe-web-dashboard.streamlit.app/)**

</div>
