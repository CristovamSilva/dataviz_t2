import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px


def financial_impact(df: pd.DataFrame):
    st.subheader("🧠 Perceived Financial Impact on Well-Being")

    fig = px.histogram(
        df,
        x="self_eval_finance_well_being",
        nbins=11,
        title="Impact of Financial Situation on Life Quality",
        labels={"self_eval_finance_well_being": "Impact Score (-5 to 5)"},
        color_discrete_sequence=["#f28e2b"],
    )
    fig.update_layout(xaxis=dict(dtick=1), yaxis_title="Number of People")
    st.plotly_chart(fig, use_container_width=True)


def reserve_duration(df: pd.DataFrame):
    st.subheader("🕒 Emergency Reserve Coverage")

    label_map = {
        "none": "No Reserve",
        "lt_3_w": "<3 weeks",
        "lt_8_w": "<8 weeks",
        "lt_20_w": "<20 weeks",
        "gt_24_w": "24+ weeks",
    }

    order = ["none", "lt_3_w", "lt_8_w", "lt_20_w", "gt_24_w"]

    counts = (
        df["emergency_reserve_savings_period"]
        .map(label_map)
        .value_counts(normalize=True)
        .reindex([label_map[k] for k in order])
        .fillna(0)
        .reset_index()
    )

    counts.columns = ["Coverage", "Proportion"]
    counts["Percentage"] = (counts["Proportion"] * 100).round(1)

    fig = px.bar(
        counts,
        x="Coverage",
        y="Percentage",
        text="Percentage",
        color="Coverage",
        title="Emergency Reserve Duration",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    fig.update_layout(
        showlegend=False, yaxis_title="Percentage of People", xaxis_title=None
    )

    st.plotly_chart(fig, use_container_width=True)


def financial_flags(df: pd.DataFrame):
    st.subheader("🔐 Financial Security Indicators")

    bool_cols = [
        "debt",
        "emergency_reserve",
        "investments",
        "savings_money",
        "unexpected_expenses",
    ]

    labels = {
        "debt": "Has Debt",
        "emergency_reserve": "Emergency Reserve",
        "investments": "Has Investments",
        "savings_money": "Has Savings",
        "unexpected_expenses": "Can Cover Unexpected Expenses",
    }

    data = []
    for col in bool_cols:
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        data.extend(
            [
                {
                    "Label": labels[col],
                    "Response": "Yes",
                    "Percent": round(counts[True] * 100, 1),
                },
                {
                    "Label": labels[col],
                    "Response": "No",
                    "Percent": round(counts[False] * 100, 1),
                },
            ]
        )

    bool_df = pd.DataFrame(data)

    fig = px.bar(
        bool_df,
        x="Label",
        y="Percent",
        color="Response",
        barmode="stack",
        text="Percent",
        color_discrete_map={"Yes": "#59a14f", "No": "#e15759"},
        title="Financial Indicators (Yes/No)",
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Percentage",
        xaxis_tickangle=30,
        uniformtext_minsize=8,
        uniformtext_mode="hide",
    )

    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("💰 Financial Health", df)

    financial_impact(df)
    financial_flags(df)
    reserve_duration(df)
