import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.health_dash import template


def show(df: pd.DataFrame):
    template("🧠 Mental Health", df)

    mental_emotional(df)
    mental_social(df)
    mental_context(df)


def mental_emotional(df: pd.DataFrame):
    st.subheader("😔 Emotional and Cognitive Indicators")

    columns = {
        "anxiety": "Anxiety",
        "depression": "Depression",
        "burnout": "Burnout",
        "forgetfulness": "Forgetfulness",
        "low_quality_of_life": "Low Quality of Life",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes_pct = round(counts[True] * 100, 1)
        no_pct = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes_pct, "No": no_pct})

    plot_df = pd.DataFrame(data).melt(
        id_vars="Label", var_name="Evaluation", value_name="Percent"
    )

    fig = px.bar(
        plot_df,
        x="Label",
        y="Percent",
        color="Evaluation",
        barmode="stack",
        text="Percent",
        color_discrete_map={"Yes": "#e15759", "No": "#bab0ac"},
        title="Reported Mental Health Symptoms",
    )

    fig.update_layout(xaxis_tickangle=30, yaxis_title="Percentage")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


def mental_social(df: pd.DataFrame):
    st.subheader("🤝 Social & Well-Being Engagement")

    columns = {
        "is_socially_active": "Socially Active",
        "work_satisfaction": "Work Satisfaction",
        "spirituality": "Spirituality",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes_pct = round(counts[True] * 100, 1)
        no_pct = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes_pct, "No": no_pct})

    plot_df = pd.DataFrame(data).melt(
        id_vars="Label", var_name="Response", value_name="Percent"
    )

    fig = px.bar(
        plot_df,
        x="Label",
        y="Percent",
        color="Response",
        barmode="stack",
        text="Percent",
        color_discrete_map={"Yes": "#59a14f", "No": "#bab0ac"},
        title="Positive Social and Psychological Support Factors",
    )

    fig.update_layout(xaxis_tickangle=30, yaxis_title="Percentage")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


def mental_context(df: pd.DataFrame):
    st.subheader("🏠 Household Composition")

    columns = {
        "household_situation_alone": "Lives Alone",
        "household_situation_adults": "With Other Adults",
        "household_situation_parents": "With Parents",
        "household_situation_partner": "With Partner",
        "household_situation_pet": "Has Pets",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes_pct = round(counts[True] * 100, 1)
        no_pct = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes_pct, "No": no_pct})

    plot_df = pd.DataFrame(data).melt(
        id_vars="Label", var_name="Response", value_name="Percent"
    )

    fig = px.bar(
        plot_df,
        x="Label",
        y="Percent",
        color="Response",
        barmode="stack",
        text="Percent",
        color_discrete_map={"Yes": "#4e79a7", "No": "#bab0ac"},
        title="Household Living Arrangements",
    )

    fig.update_layout(xaxis_tickangle=30, yaxis_title="Percentage")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
