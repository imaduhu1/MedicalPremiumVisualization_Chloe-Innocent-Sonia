# streamlitvisual_app.py

import streamlit as st
import pandas as pd
import altair as alt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Page configuration
st.set_page_config(page_title="Medical Premium Explorer", layout="wide")
st.title("Medical Premium Explorer Dashboard")

# 1. Load & preprocess data
df = pd.read_csv("Medicalpremium.csv")
df["HasMajorSurgery"] = (df["NumberOfMajorSurgeries"].fillna(0).apply(lambda x: 1 if x >= 1 else 0))


# 1a. Create AgeGroup bins
age_bins = [17, 29, 39, 49, 59, 69]
age_labels = ["18–29", "30–39", "40–49", "50–59", "60–69"]
df["AgeGroup"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels)

# 1b. K-means clustering on PremiumPrice to define RiskLevel
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[["PremiumPrice"]])
kmeans = KMeans(n_clusters=4, random_state=42)
df["Cluster"] = kmeans.fit_predict(X_scaled)

# Map clusters to risk categories exactly as in your notebook
cluster_map = {
    0: "High",
    1: "Low",
    2: "Moderate",
    3: "Moderate"
}
df["RiskLevel"] = df["Cluster"].map(cluster_map)

# 2. Sidebar controls
st.sidebar.header("Filters & Options")

# Highlight a single age group
age_highlight = st.sidebar.selectbox("Highlight Age-Group", ["None"] + age_labels)

# Conditions for comparison
conditions = [
    "Diabetes",
    "BloodPressureProblems",
    "HistoryOfCancerInFamily",
    "HasMajorSurgery",
    "AnyChronicDiseases"
]
sel_conditions = st.sidebar.multiselect("Compare Conditions", conditions)

# Heatmap axes
cond_x = st.sidebar.selectbox("Heatmap Condition X", conditions)
cond_y = st.sidebar.selectbox("Heatmap Condition Y", conditions, index=1)

# Box-plot condition
box_cond = st.sidebar.selectbox("Box-Plot Condition", ["None"] + conditions)

# Risk-level filter
risk_levels = ["Low", "Moderate", "High"]
sel_risks = st.sidebar.multiselect("Select Risk Levels", risk_levels, default=risk_levels)

# Filter dataframe by selected risk levels
df_filtered = df[df["RiskLevel"].isin(sel_risks)]

# 3. KPI cards
avg_prem = df_filtered["PremiumPrice"].mean()
min_prem = df_filtered["PremiumPrice"].min()
max_prem = df_filtered["PremiumPrice"].max()
count_records = len(df_filtered)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Avg Premium", f"${avg_prem:,.0f}")
c2.metric("Min Premium", f"${min_prem:,.0f}")
c3.metric("Max Premium", f"${max_prem:,.0f}")
c4.metric("Records", f"{count_records:,}")

# 4. Compound chart: Avg Premium & Record Count by Risk Level
st.subheader("Avg Premium & Record Count by Risk Level")

# build a summary with both metrics
risk_summary2 = (
    df_filtered
      .groupby("RiskLevel")
      .agg(
          AvgPremium=("PremiumPrice","mean"),
          RecordCount=("PremiumPrice","count")
      )
      .reindex(risk_levels)
      .reset_index()
)

base = alt.Chart(risk_summary2).encode(
    x=alt.X("RiskLevel:N", title="Risk Level")
)

# bar for average premium
bar_prem = base.mark_bar(size=20).encode(
    y=alt.Y("AvgPremium:Q", axis=alt.Axis(title="Avg Premium ($)"))
)

# bar for record count (semi‐transparent gray)
bar_count = base.mark_bar(size=20, opacity=0.5, color="lightgray").encode(
    y=alt.Y("RecordCount:Q", axis=alt.Axis(title="Record Count"))
)

# layer them and tell Altair to use independent scales
compound_chart = alt.layer(bar_prem, bar_count).resolve_scale(y="independent")

st.altair_chart(compound_chart, use_container_width=True)


# 5. Avg Premium by Age Group (with optional highlight)
st.subheader("Avg Premium by Age Group")
age_summary = df_filtered.groupby("AgeGroup")["PremiumPrice"].mean().reset_index()
bar = alt.Chart(age_summary).mark_bar().encode(
    x="AgeGroup:N",
    y="PremiumPrice:Q"
)
if age_highlight != "None":
    bar = bar.encode(
        color=alt.condition(
            alt.datum.AgeGroup == age_highlight,
            alt.value("steelblue"),
            alt.value("lightgray")
        )
    ) + alt.Chart(pd.DataFrame({"y": [avg_prem]})).mark_rule(strokeDash=[5,5]).encode(y="y:Q")
st.altair_chart(bar, use_container_width=True)

# 6. Multi-line chart for selected conditions
if sel_conditions:
    st.subheader("Avg Premium by Age Group for Selected Conditions")
    lines = []
    for cond in sel_conditions:
        tmp = (
            df_filtered[df_filtered[cond] == 1]
            .groupby("AgeGroup")["PremiumPrice"]
            .mean()
            .reset_index()
            .assign(Condition=cond)
        )
        lines.append(tmp)
    df_lines = pd.concat(lines, ignore_index=True)
    line_chart = alt.Chart(df_lines).mark_line(point=True).encode(
        x="AgeGroup:N",
        y="PremiumPrice:Q",
        color="Condition:N"
    ).properties(width=600, height=300)
    st.altair_chart(line_chart, use_container_width=True)

# 7. Heatmap of any two-condition combination
if cond_x != cond_y:
    st.subheader(f"Heatmap: {cond_x} vs {cond_y}")
    heat_data = (
        df_filtered.groupby([cond_x, cond_y])["PremiumPrice"]
        .mean()
        .reset_index()
        .rename(columns={cond_x: "X", cond_y: "Y", "PremiumPrice": "AvgPremium"})
    )
    heatmap = alt.Chart(heat_data).mark_rect().encode(
        x="X:N",
        y="Y:N",
        color=alt.Color("AvgPremium:Q", title="Avg Premium")
    ).properties(width=400, height=300)
    st.altair_chart(heatmap, use_container_width=True)

# 8. Box-plot for a single condition
if box_cond != "None":
    st.subheader(f"Premium Distribution by Age Group for {box_cond}")
    box = alt.Chart(df_filtered).mark_boxplot().encode(
        x="AgeGroup:N",
        y="PremiumPrice:Q",
        color=alt.Color(f"{box_cond}:N", legend=None, scale=None)
    ).properties(width=600, height=300)
    st.altair_chart(box, use_container_width=True)

# 9. Stacked bar: Risk Profile by Age Group
st.subheader("Risk Profile by Age Group")
stacked = (
    df_filtered.groupby(["AgeGroup", "RiskLevel"])
    .size()
    .reset_index(name="count")
)
stack_chart = alt.Chart(stacked).mark_bar().encode(
    x="AgeGroup:N",
    y=alt.Y("count:Q", stack="normalize", title="Proportion"),
    color=alt.Color(
        "RiskLevel:N",
        scale=alt.Scale(domain=risk_levels, range=["#2ca02c", "#ff7f0e", "#d62728"])
    )
).properties(width=600, height=300)
st.altair_chart(stack_chart, use_container_width=True)
