import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px
import plotly.graph_objects as go


def bmi(df: pd.DataFrame):
    st.subheader("⚖️ Weight vs. Height Colored by BMI Category")

    # Rename category for consistency
    df["bmi_category"] = df["bmi_category"].replace(
        {"Peso Elevado": "Obesidade grau 1"}
    )

    # Define desired order and color for categories
    bmi_order = [
        "Abaixo do peso.",
        "Peso normal",
        "Obesidade grau 1",
        "Obesidade grau 2",
        "Obesidade grau 3",
    ]

    bmi_colors = {
        "Abaixo do peso.": "#1f77b4",  # blue
        "Peso normal": "#59a14f",  # green
        "Obesidade grau 1": "#e15759",  # red
        "Obesidade grau 2": "#f28e2b",  # orange
        "Obesidade grau 3": "#d62728",  # dark red
    }

    # Enforce order in the data
    df["bmi_category"] = pd.Categorical(
        df["bmi_category"], categories=bmi_order, ordered=True
    )

    fig = px.scatter(
        df,
        x="height",
        y="weight",
        color="bmi_category",
        category_orders={"bmi_category": bmi_order},
        size="bmi",
        hover_data=["bmi", "bmi_category"],
        labels={
            "height": "Height (cm)",
            "weight": "Weight (kg)",
            "bmi_category": "BMI Category",
            "bmi": "BMI",
        },
        title="Physical Health: Weight vs Height by BMI Category",
        opacity=0.7,
        color_discrete_map=bmi_colors,
    )

    fig.update_layout(legend_title_text="BMI Category")
    st.plotly_chart(fig, use_container_width=True)


def activities(df: pd.DataFrame):
    st.subheader("🏃 Active and Sedentary Classification Across Activity Levels")

    # Make sure 'physical_activities' has correct order
    activity_order = ["none", "low", "moderate", "high"]
    df["physical_activities"] = pd.Categorical(
        df["physical_activities"], categories=activity_order, ordered=True
    )

    # Melt active/sedentary into long format for grouped plotting
    melted = df.melt(
        id_vars="physical_activities",
        value_vars=["active", "sedentary"],
        var_name="Classification",
        value_name="Value",
    )

    # Filter to only True values
    melted = melted[melted["Value"] == True]

    # Count combinations
    counts = (
        melted.groupby(["physical_activities", "Classification"])
        .size()
        .reset_index(name="count")
    )

    # Plot
    fig = px.bar(
        counts,
        x="physical_activities",
        y="count",
        color="Classification",
        barmode="group",
        title="Active and Sedentary Counts by Physical Activity Level",
        labels={
            "physical_activities": "Physical Activity Level",
            "count": "Number of Individuals",
            "Classification": "",
        },
        color_discrete_map={"active": "#59a14f", "sedentary": "#e15759"},
    )

    st.plotly_chart(fig, use_container_width=True)


def sitting_time(df: pd.DataFrame):
    st.subheader("🪑 Sitting Time Category vs Excessiveness")

    # Define label map and order
    freq_label_map = {
        "lt_2h": "Less than 2 hours",
        "lt_4h": "Less than 4 hours",
        "lt_6h": "Less than 6 hours",
        "gt_6h": "More than 6 hours",
    }
    label_order = list(freq_label_map.values())

    # Replace labels
    df["sit_down_time_daily"] = df["sit_down_time_daily"].replace(freq_label_map)
    df["sit_down_time_daily"] = pd.Categorical(
        df["sit_down_time_daily"], categories=label_order, ordered=True
    )

    # Group and count
    counts = (
        df.groupby(["sit_down_time_daily", "excessive_sit_down_time"])
        .size()
        .reset_index(name="count")
    )

    # Compute % of total population
    total = counts["count"].sum()
    counts["percent"] = (counts["count"] / total * 100).round(1)

    # Plot
    fig = px.bar(
        counts,
        x="sit_down_time_daily",
        y="percent",
        color="excessive_sit_down_time",
        barmode="group",
        title="Sitting Time vs Excessive Sitting Classification",
        color_discrete_map={True: "#e15759", False: "#59a14f"},
        labels={
            "sit_down_time_daily": "Sitting Time Category",
            "excessive_sit_down_time": "Excessive Sitting",
            "percent": "Percentage of People",
        },
    )

    fig.update_layout(
        yaxis=dict(range=[0, 100]),
    )

    st.plotly_chart(fig, use_container_width=True)


def pain(df: pd.DataFrame):
    st.subheader("🩻 Weekly Pain Frequency")

    # Define the pain columns to process
    pain_columns = {
        "back_pain_weekly": ("Back Pain", "#4e79a7"),
        "body_pain_weekly": ("Body Pain", "#f28e2b"),
        "headache_weekly": ("Headache", "#e15759"),
    }

    # Ensure x-axis includes all days 0–7
    index = pd.Index(range(8), name="Days")

    fig = go.Figure()

    for col, (label, color) in pain_columns.items():
        if col in df.columns:
            counts = df[col].value_counts(normalize=True).sort_index() * 100
            counts = counts.reindex(index, fill_value=0)
            fig.add_trace(
                go.Scatter(
                    x=counts.index,
                    y=counts.values,
                    mode="lines+markers",
                    name=label,
                    line=dict(color=color),
                )
            )

    fig.update_layout(
        title="Weekly Pain: Percentage of People by Days per Week",
        xaxis_title="Days per Week with Pain",
        yaxis_title="Percentage of People",
        xaxis=dict(dtick=1),
        yaxis=dict(range=[0, 100]),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("🏃 Physical Health", df)

    st.markdown("---")
    bmi(df)
    st.markdown("---")
    activities(df)
    st.markdown("---")
    sitting_time(df)
    st.markdown("---")
    pain(df)
    st.markdown("---")
