import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.health_dash import template
import plotly.graph_objects as go


def mental_well_being(df: pd.DataFrame):
    st.subheader("🧠 Mental Health Impact on Well-Being")
    st.markdown(
        "This shows how people rated the impact of their mental health on their well-being, "
        "from very negative (-5) to very positive (+5)."
    )

    # Prepare data
    counts = (
        df["self_eval_mental_well_being"]
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
    plot_df["Label"] = pd.Categorical(
        plot_df["Label"], categories=columns.values(), ordered=True
    )

    fig = px.bar(
        plot_df,
        y="Label",
        x="Percent",
        color="Evaluation",
        barmode="stack",
        orientation="h",
        text="Percent",
        color_discrete_map={"Yes": "#e15759", "No": "#bab0ac"},
        title="Reported Mental Health Symptoms",
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
    )

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
    plot_df["Label"] = pd.Categorical(
        plot_df["Label"], categories=columns.values(), ordered=True
    )

    fig = px.bar(
        plot_df,
        y="Label",
        x="Percent",
        color="Response",
        barmode="stack",
        orientation="h",
        text="Percent",
        color_discrete_map={"Yes": "#59a14f", "No": "#bab0ac"},
        title="Positive Social and Psychological Support Factors",
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
    )

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
    plot_df["Label"] = pd.Categorical(
        plot_df["Label"], categories=columns.values(), ordered=True
    )

    fig = px.bar(
        plot_df,
        y="Label",
        x="Percent",
        color="Response",
        barmode="stack",
        orientation="h",
        text="Percent",
        color_discrete_map={"Yes": "#4e79a7", "No": "#bab0ac"},
        title="Household Living Arrangements",
    )

    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("🧠 Mental Health", df)

    st.markdown("---")
    mental_well_being(df)
    st.markdown("---")
    mental_emotional(df)
    st.markdown("---")
    mental_social(df)
    st.markdown("---")
    mental_context(df)
    st.markdown("---")
