import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px


def sleep_eval(df: pd.DataFrame):
    st.subheader("😴 Self-Evaluated Sleep Quality")

    # Compute percentage per rating
    quality_counts = (
        df["self_eval_sleep_quality"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .reset_index()
    )
    quality_counts.columns = ["Rating", "Percentage"]

    fig = px.bar(
        quality_counts,
        x="Rating",
        y="Percentage",
        text="Percentage",
        title="Sleep Quality Distribution (0–10)",
        labels={"Rating": "Quality Rating", "Percentage": "Percentage of People"},
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")

    fig.update_layout(
        yaxis=dict(visible=False),
        xaxis_title="Quality Rating",
        margin=dict(t=40, b=30),
    )

    st.plotly_chart(fig, use_container_width=True)


def sleep_duration(df: pd.DataFrame):
    st.subheader("⏱️ Sleep Duration")
    st.markdown(
        "Each point is a person — the wider the shape, the more people sleep that number of hours."
    )

    fig = px.violin(
        df,
        y="sleep_hours",
        box=False,  # remove the box
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
    symptom_counts = (
        melted[melted["Present"] == True]["Symptom"]
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
        .reset_index()
    )

    symptom_counts.columns = ["Symptom", "Percentage"]
    symptom_counts["Symptom"] = (
        symptom_counts["Symptom"].str.replace("_", " ").str.title()
    )

    fig = px.bar(
        symptom_counts,
        x="Symptom",
        y="Percentage",
        text="Percentage",
        title="Prevalence of Sleep-Related Symptoms",
    )

    fig.update_traces(
        marker_color="#4e79a7", texttemplate="%{text:.1f}%", textposition="outside"
    )
    fig.update_layout(
        showlegend=False,
        xaxis_tickangle=30,
        yaxis_title=None,
        yaxis=dict(visible=False),
    )

    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("🛌 Sleep Health", df)

    st.markdown("---")
    sleep_eval(df)
    st.markdown("---")
    sleep_duration(df)
    st.markdown("---")
    sleep_disturbances(df)
    st.markdown("---")
