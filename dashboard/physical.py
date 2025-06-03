import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px
import plotly.graph_objects as go


def bmi(df: pd.DataFrame):
    st.subheader("⚖️ Weight vs. Height Colored by BMI Category")

    fig = px.scatter(
        df,
        x="height",
        y="weight",
        color="bmi_category",
        size="bmi",  # optional: size by BMI
        hover_data=["bmi", "bmi_category"],
        labels={
            "height": "Height (cm)",
            "weight": "Weight (kg)",
            "bmi_category": "BMI Category",
            "bmi": "BMI",
        },
        title="Physical Health: Weight vs Height by BMI Category",
        opacity=0.7,
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

    # Define category order (if needed)
    cat_order = ["lt_2h", "lt_4h", "lt_6h", "gt_6h"]
    df["sit_down_time_daily"] = pd.Categorical(
        df["sit_down_time_daily"], categories=cat_order, ordered=True
    )

    # Count combinations
    counts = (
        df.groupby(["sit_down_time_daily", "excessive_sit_down_time"])
        .size()
        .reset_index(name="count")
    )

    # Plot grouped bar
    fig = px.bar(
        counts,
        x="sit_down_time_daily",
        y="count",
        color="excessive_sit_down_time",
        barmode="group",
        title="Sitting Time Categories vs Excessive Sitting Classification",
        labels={
            "sit_down_time_daily": "Sitting Time Category",
            "excessive_sit_down_time": "Excessive Sitting",
            "count": "Number of People",
        },
        color_discrete_map={True: "#e15759", False: "#59a14f"},
    )

    st.plotly_chart(fig, use_container_width=True)


def pain(df: pd.DataFrame):
    st.subheader("🩻 Weekly Pain Frequency")

    # Count values per pain level
    back_counts = df["back_pain_weekly"].value_counts().sort_index()
    body_counts = df["body_pain_weekly"].value_counts().sort_index()

    # Ensure full index range (0–7)
    index = pd.Index(range(8), name="Days")
    back_counts = back_counts.reindex(index, fill_value=0)
    body_counts = body_counts.reindex(index, fill_value=0)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=back_counts.index,
            y=back_counts.values,
            mode="lines+markers",
            name="Back Pain",
            line=dict(color="#4e79a7"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=body_counts.index,
            y=body_counts.values,
            mode="lines+markers",
            name="Body Pain",
            line=dict(color="#f28e2b"),
        )
    )

    fig.update_layout(
        title="Pain Frequency by Number of Days per Week",
        xaxis_title="Days per Week with Pain",
        yaxis_title="Number of People",
        xaxis=dict(dtick=1),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("🏃 Physical Health", df)

    bmi(df)
    activities(df)
    sitting_time(df)
    pain(df)
