import streamlit as st
import pandas as pd
from .health_dash import template
import plotly.express as px
import plotly.graph_objects as go


def financial_impact(df: pd.DataFrame):
    st.subheader("📉 Financial Health Impact on Well-Being")
    st.markdown(
        "This shows how people rated the impact of their financial health on their well-being, "
        "from very negative (-5) to very positive (+5)."
    )

    # Prepare data
    counts = (
        df["self_eval_finance_well_being"]
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
        y="Coverage",
        x="Percentage",
        orientation="h",
        text="Percentage",
        title="Emergency Reserve Duration",
        color_discrete_sequence=["#4e79a7"],
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")

    fig.update_layout(
        showlegend=False,
        yaxis_title=None,
        xaxis_title=None,
        margin=dict(t=40, l=10, r=10, b=30),
    )

    st.plotly_chart(fig, use_container_width=True)


def financial_flags(df: pd.DataFrame):
    st.subheader("🔐 Financial Security Indicators")

    bool_cols = [
        "debt",
        "investments",
        "savings_money",
        "unexpected_expenses",
    ]

    labels = {
        "debt": "Has Debt",
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
    bool_df["Label"] = pd.Categorical(
        bool_df["Label"], categories=list(labels.values()), ordered=True
    )

    fig = px.bar(
        bool_df,
        y="Label",
        x="Percent",
        color="Response",
        barmode="stack",
        orientation="h",
        text="Percent",
        color_discrete_map={"Yes": "#59a14f", "No": "#e15759"},
        title="Financial Indicators (Yes/No)",
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(t=40, l=10, r=10, b=30),
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("💰 Financial Health", df)

    st.markdown("---")
    financial_impact(df)
    st.markdown("---")
    financial_flags(df)
    st.markdown("---")
    reserve_duration(df)
    st.markdown("---")
