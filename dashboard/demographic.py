import streamlit as st
import plotly.express as px
import pandas as pd


def biological_sex(df):
    counts = df["biological_sex"].value_counts(normalize=True).reset_index()
    counts.columns = ["label", "value"]
    fig = px.pie(
        counts, names="label", values="value", title="Biological Sex", hole=0.3
    )
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)


def health_insurance(df):
    counts = df["health_insurance"].value_counts(normalize=True).reset_index()
    counts.columns = ["label", "value"]
    fig = px.pie(
        counts, names="label", values="value", title="Health Insurance", hole=0.3
    )
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)


def age_distribution(df):
    counts = df["age_binned"].value_counts(normalize=True).sort_index().reset_index()
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)
    fig = px.bar(
        counts, x="label", y="percent", title="Age Distribution", text="percent"
    )
    fig.update_layout(yaxis_title="%", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def education_level(df):
    counts = (
        df["education_level"].value_counts(normalize=True).sort_index().reset_index()
    )
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)
    fig = px.bar(
        counts, x="label", y="percent", title="Education Level", text="percent"
    )
    fig.update_layout(yaxis_title="%", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def marital_status(df):
    counts = (
        df["marital_status"].value_counts(normalize=True).sort_index().reset_index()
    )
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)
    fig = px.bar(counts, x="label", y="percent", title="Marital Status", text="percent")
    fig.update_layout(yaxis_title="%", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def work_model(df):
    counts = df["work_model"].value_counts(normalize=True).sort_index().reset_index()
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)
    fig = px.bar(counts, x="label", y="percent", title="Work Model", text="percent")
    fig.update_layout(yaxis_title="%", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def general_health_eval(df):
    fig = px.histogram(
        df["self_eval_health_general"].dropna(),
        nbins=11,
        title="Self-Eval: General Health",
        labels={"self_eval_health_general": "Rating"},
    )
    fig.update_layout(xaxis=dict(dtick=1), yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)


def quality_of_life_eval(df):
    fig = px.histogram(
        df["self_eval_health_quality"].dropna(),
        nbins=11,
        title="Self-Eval: Quality of Life",
        labels={"self_eval_health_quality": "Rating"},
    )
    fig.update_layout(xaxis=dict(dtick=1), yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    st.title("📊 Demographic Distributions")

    # Bin ages
    age_bins = [18, 25, 35, 45, 55, 65, 100]
    age_labels = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
    df["age_binned"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)

    # Render in 2x4 grid
    charts = [
        biological_sex,
        health_insurance,
        age_distribution,
        education_level,
        marital_status,
        work_model,
        general_health_eval,
        quality_of_life_eval,
    ]

    for i in range(0, 8, 4):
        cols = st.columns(4)
        for col, chart in zip(cols, charts[i : i + 4]):
            with col:
                chart(df)
