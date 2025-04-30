#  Medical Premium Visualization Dashboard

This interactive dashboard allows users to explore health insurance premium patterns based on individual health characteristics and risk indicators. Built using **Streamlit**, the app uses clustering and visual analytics to offer insights into medical premium factors and segmentation.

## 🚀 Launch the App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medicalpremiumvisualizationchloe-innocent-sonia-bmhodbm3cfnpso.streamlit.app/)

---

## 🧾 Project Description

This project visualizes a medical premium dataset across various individual health factors. It highlights how premiums vary across **low, moderate, and high-risk clusters**, using **KMeans Clustering** for segmentation.

Key features include:
- **Cluster-based analysis** of premiums using KMeans.
- Visualization of **premium distributions** across **age groups** and **health conditions** (e.g., diabetes, chronic illnesses, cancer history).
- Interactive **boxplots and heatmaps** comparing how the presence (1) or absence (0) of any two selected conditions affects premium variation.

The core logic is contained in `streamlitvisual_app.py`, which loads and processes the dataset (`Medicalpremium.csv`) and generates visuals using **Pandas**, **Altair**, and **Scikit-learn**.

---

## 📊 Features

- Dynamic visualizations of health premium trends
- Clustering analysis for segmenting clients by risk level
- Real-time filtering by age group, health conditions, and more
- Intuitive visuals: heatmaps, boxplots, scatter plots

---

## 🧠 Technologies Used

- **Streamlit** – Web app framework
- **Pandas** – Data manipulation
- **Altair** – Visualizations
- **Scikit-learn** – KMeans clustering
- **Python** – Core programming

---

## 🗂️ File Structure

```bash
├── streamlitvisual_app.py       # Main Streamlit app script
├── Medicalpremium.csv           # Dataset used for visualization
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation



