import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px


def self_eval_nutrition(df: pd.DataFrame):
    st.subheader("🍽️ Perceived Nutritional Quality")

    # --- Perceived Diet Quality (Yes/No) ---
    counts = (
        df["self_eval_nutrition"]
        .map({True: "Yes", False: "No"})
        .value_counts(normalize=True)
        .reindex(["Yes", "No"])
        .fillna(0)
        .reset_index()
    )
    counts.columns = ["Response", "Proportion"]
    counts["Percentage"] = (counts["Proportion"] * 100).round(1)

    fig = px.pie(
        counts,
        names="Response",
        values="Proportion",
        hole=0.4,
        title="Do You Believe You Eat Well?",
        color="Response",
        color_discrete_map={"Yes": "#59a14f", "No": "#e15759"},
    )
    fig.update_traces(textinfo="label+percent")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🧠 Perceived Impact of Nutrition on Overall Well-Being")

    fig2 = px.histogram(
        df,
        x="self_eval_nutrition_well_being",
        nbins=11,
        title="Impact Scale (-5 = Very Negative, +5 = Very Positive)",
        labels={"self_eval_nutrition_well_being": "Impact Score"},
        color_discrete_sequence=["#4e79a7"],
    )

    fig2.update_layout(xaxis=dict(dtick=1), yaxis_title="Number of People")

    st.plotly_chart(fig2, use_container_width=True)


def water_intake_bar_grouped(df):
    st.subheader("💧 Water Intake Groups")

    levels = {
        "lt_500": "Very Low",
        "lt_1000": "Low",
        "lt_1500": "Medium",
        "gt_1500": "Adequate",
        "gt_2000": "Optimal",
    }

    counts = (
        df["water_intake"]
        .map(levels)
        .value_counts(normalize=True)
        .reindex(["Very Low", "Low", "Medium", "Adequate", "Optimal"])
        .fillna(0)
        .reset_index()
    )
    counts.columns = ["Hydration Level", "Proportion"]
    counts["Percentage"] = (counts["Proportion"] * 100).round(1)

    fig = px.bar(
        counts,
        x="Percentage",
        y="Hydration Level",
        orientation="h",
        text="Percentage",
        color="Hydration Level",
        title="Hydration Levels by Intake Group",
        color_discrete_sequence=px.colors.sequential.Blues,
    )
    fig.update_layout(showlegend=False, xaxis_title="%", yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def food_frequency_distribution(df: pd.DataFrame):
    st.subheader("🥗 Food Consumption Frequency by Health Category")

    unhealthy = ["fast_food", "processed", "soft_drink"]
    healthy = ["vegetables", "fruits", "fibers"]
    order = ["none", "lt_2", "gt_3", "gt_5"]
    labels = {
        "none": "None",
        "lt_2": "1-2x/week",
        "gt_3": "3-5x/week",
        "gt_5": "6-7x/week",
    }

    def prep_data(columns, group_label):
        data = []
        for col in columns:
            dist = df[col].value_counts(normalize=True).reindex(order).fillna(0)
            for freq in order:
                data.append(
                    {
                        "Food": col.replace("_", " ").title(),
                        "Frequency": labels[freq],
                        "Percent": round(dist[freq] * 100, 1),
                    }
                )
        return pd.DataFrame(data)

    unhealthy_df = prep_data(unhealthy, "Unhealthy")
    healthy_df = prep_data(healthy, "Healthy")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            unhealthy_df,
            x="Food",
            y="Percent",
            color="Frequency",
            text="Percent",
            title="Unhealthy Foods",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig1.update_layout(barmode="stack", yaxis_title="%", xaxis_title=None)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            healthy_df,
            x="Food",
            y="Percent",
            color="Frequency",
            text="Percent",
            title="Healthy Foods",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig2.update_layout(barmode="stack", yaxis_title="%", xaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)


def show(df: pd.DataFrame):
    template("🥦 Nutritional Health", df)
    self_eval_nutrition(df)
    water_intake_bar_grouped(df)
    food_frequency_distribution(df)
