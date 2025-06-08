import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px
import plotly.graph_objects as go


def nutrition_impact(df: pd.DataFrame):
    st.subheader("🍽️ Nutritional Health Impact on Well-Being")
    st.markdown(
        "This shows how people rated the impact of their nutritional health on their well-being, "
        "from very negative (-5) to very positive (+5)."
    )

    # Prepare data
    counts = (
        df["self_eval_nutrition_well_being"]
        .value_counts(normalize=True)
        .reindex(range(-5, 6), fill_value=0)
        .mul(100)
        .round(1)
        .reset_index()
    )
    counts.columns = ["Score", "Percentage"]

    # Define color per sentiment
    counts["Color"] = counts["Score"].apply(
        lambda x: "#e15759" if x < 0 else "#59a14f" if x > 0 else "#bab0ac"
    )

    # Create lollipop chart (vertical stems + dots)
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=counts["Score"],
            y=counts["Percentage"],
            mode="lines+markers",
            line=dict(color="rgba(0,0,0,0)"),  # invisible line for stems
            marker=dict(
                size=12, color=counts["Color"], line=dict(width=1, color="black")
            ),
            hovertemplate="Score: %{x}<br>%{y:.1f}%",
            showlegend=False,
        )
    )

    # Add stems as individual vertical lines
    for _, row in counts.iterrows():
        fig.add_shape(
            type="line",
            x0=row["Score"],
            y0=0,
            x1=row["Score"],
            y1=row["Percentage"],
            line=dict(color=row["Color"], width=2),
        )

    fig.update_layout(
        title="Self-Evaluated Mental Well-Being (Scale: -5 to 5)",
        xaxis=dict(dtick=1, title="Score", tickmode="linear"),
        yaxis=dict(
            title="Percentage of People", range=[0, counts["Percentage"].max() + 5]
        ),
        template="plotly_white",
        height=400,
        margin=dict(t=50, b=40, l=30, r=30),
    )

    st.plotly_chart(fig, use_container_width=True)


def self_eval_nutrition(df: pd.DataFrame):
    st.subheader("🍽️ Perceived Nutritional Health")

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

    fig1 = px.bar(
        counts,
        x="Response",
        y="Percentage",
        text="Percentage",
        color="Response",
        color_discrete_map={"Yes": "#59a14f", "No": "#e15759"},
    )

    fig1.update_traces(texttemplate="%{text:.1f}%", textposition="outside")

    fig1.update_layout(
        title="Answer to the question: 'Do You Believe You Eat Well?'",
        showlegend=False,
        xaxis_title=None,
        yaxis=dict(visible=False),
        margin=dict(t=40, b=20),
    )

    st.plotly_chart(fig1, use_container_width=True)


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

    color_map = {
        "None": "#d9f0d3",
        "1-2x/week": "#a6dba0",
        "3-5x/week": "#5aae61",
        "6-7x/week": "#1b7837",
    }

    def prep_data(columns):
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

    unhealthy_df = prep_data(unhealthy)
    healthy_df = prep_data(healthy)

    col1, col2 = st.columns(2)

    with col1:
        fig2 = px.bar(
            healthy_df,
            x="Food",
            y="Percent",
            color="Frequency",
            text="Percent",
            title="Healthy Foods",
            color_discrete_map=color_map,
        )
        fig2.update_layout(
            barmode="stack",
            yaxis_title="Percentage",
            xaxis_title=None,
            legend_title_text="Frequency",
        )
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        fig1 = px.bar(
            unhealthy_df,
            x="Food",
            y="Percent",
            color="Frequency",
            text="Percent",
            title="Unhealthy Foods",
            color_discrete_map=color_map,
        )
        fig1.update_layout(
            barmode="stack",
            yaxis_title="Percentage",
            xaxis_title=None,
            legend_title_text="Frequency",
        )
        fig1.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
        st.plotly_chart(fig1, use_container_width=True)


def show(df: pd.DataFrame):
    template("🥦 Nutritional Health", df)
    st.markdown("---")
    nutrition_impact(df)
    st.markdown("---")
    self_eval_nutrition(df)
    st.markdown("---")
    food_frequency_distribution(df)
    st.markdown("---")
    water_intake_bar_grouped(df)
    st.markdown("---")
