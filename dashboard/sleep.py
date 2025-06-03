import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px


def sleep_eval(df: pd.DataFrame):
    st.subheader("😴 Self-Evaluated Sleep Quality")

    quality_counts = (
        df["self_eval_sleep_quality"].value_counts().sort_index().reset_index()
    )
    quality_counts.columns = ["Rating", "Count"]

    fig = px.line(
        quality_counts,
        x="Rating",
        y="Count",
        markers=True,
        title="Sleep Quality Trend (0–10)",
        labels={"Rating": "Quality Rating", "Count": "Number of People"},
    )

    fig.update_traces(line=dict(color="#4e79a7"))
    st.plotly_chart(fig, use_container_width=True)


def sleep_duration(df: pd.DataFrame):
    st.subheader("⏱️ Sleep Duration")

    fig = px.violin(
        df,
        y="sleep_hours",
        box=True,
        points="all",
        title="Distribution of Sleep Duration (Hours per Night)",
        labels={"sleep_hours": "Hours of Sleep"},
        color_discrete_sequence=["#59a14f"],
    )
    fig.update_layout(yaxis=dict(dtick=1))
    st.plotly_chart(fig, use_container_width=True)


def sleep_disturbances(df: pd.DataFrame):
    st.subheader("🌙 Sleep-Related Symptoms")

    bool_columns = [
        "apnea",
        "sleepness_day_time",
        "wake_up_tired",
        "sleep_break",
        "snore",
        "insomnia",
    ]

    # Melt into long format
    melted = df[bool_columns].melt(var_name="Symptom", value_name="Present")
    counts = melted[melted["Present"] == True]["Symptom"].value_counts().reset_index()
    counts.columns = ["Symptom", "Count"]
    counts["Symptom"] = counts["Symptom"].str.replace("_", " ").str.title()

    fig = px.bar(
        counts,
        x="Symptom",
        y="Count",
        title="Frequency of Sleep-Related Symptoms",
        color="Symptom",
        text="Count",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=30)
    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("🛌 Sleep Health", df)

    sleep_eval(df)
    sleep_duration(df)
    sleep_disturbances(df)
