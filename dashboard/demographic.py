import streamlit as st
import plotly.express as px
import pandas as pd


def biological_sex(df):
    counts = df["biological_sex"].value_counts(normalize=True).reset_index()
    counts.columns = ["label", "value"]
    fig = px.pie(counts, names="label", values="value", hole=0.3)
    fig.update_traces(textinfo="percent+label", showlegend=False)
    fig.update_layout(
        title_text="Biological Sex",
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        margin=dict(t=40, b=10, l=10, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def health_insurance(df):
    counts = df["health_insurance"].value_counts(normalize=True).reset_index()
    counts.columns = ["label", "value"]
    fig = px.pie(counts, names="label", values="value", hole=0.3)
    fig.update_traces(textinfo="percent+label", showlegend=False)
    fig.update_layout(
        title_text="Health Insurance",
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        margin=dict(t=40, b=10, l=10, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def age_distribution(df):
    # Bin ages
    age_bins = [18, 25, 35, 45, 55, 65, 100]
    age_labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    df["age_binned"] = pd.cut(df["age"], bins=age_bins, labels=age_labels, right=False)

    counts = df["age_binned"].value_counts(normalize=True).sort_index().reset_index()
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)
    fig = px.bar(
        counts, x="label", y="percent", title="Age Distribution", text="percent"
    )
    fig.update_layout(yaxis_title="Percentage", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def education_level(df):
    label_map = {
        "incomplete_elementary": "Elem. Incomplete",
        "complete_elementary": "Elem. Completed",
        "incomplete_high_school": "HS Incomplete",
        "complete_high_school": "HS Completed",
        "incomplete_higher_education": "Univ. Incomplete",
        "complete_higher_education": "Univ. Completed",
        "post_graduation": "Postgrad",
        "masters": "Masters",
        "ph_d": "PhD",
    }
    ordered_labels = [
        "Elem. Incomplete",
        "Elem. Completed",
        "HS Incomplete",
        "HS Completed",
        "Univ. Incomplete",
        "Univ. Completed",
        "Masters",
        "Postgrad",
        "PhD",
    ]

    df["education_level"] = df["education_level"].apply(lambda x: label_map.get(x, x))

    counts = df["education_level"].value_counts(normalize=True).reset_index()
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)

    # Enforce correct order
    counts["label"] = pd.Categorical(
        counts["label"], categories=ordered_labels, ordered=True
    )
    counts = counts.sort_values("label")

    fig = px.bar(
        counts, x="label", y="percent", title="Education Level", text="percent"
    )
    fig.update_layout(yaxis_title="Percentage", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def marital_status(df):
    counts = (
        df["marital_status"].value_counts(normalize=True).sort_index().reset_index()
    )
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)
    fig = px.bar(counts, x="label", y="percent", title="Marital Status", text="percent")
    fig.update_layout(yaxis_title="Percentage", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def work_model(df):
    counts = df["work_model"].value_counts(normalize=True).sort_index().reset_index()
    counts.columns = ["label", "percent"]
    counts["percent"] = (counts["percent"] * 100).round(1)
    fig = px.bar(counts, x="label", y="percent", title="Work Model", text="percent")
    fig.update_layout(yaxis_title="Percentage", xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)


def general_health_eval(df):
    data = df["self_eval_health_general"].dropna()

    counts = data.value_counts(normalize=True).sort_index()
    percent_df = counts.mul(100).round(1).reset_index()
    percent_df.columns = ["Rating", "Percent"]

    fig = px.bar(
        percent_df,
        x="Rating",
        y="Percent",
        text="Percent",
        title="General Health Assessment",
    )
    fig.update_layout(yaxis_title="Percentage", xaxis_title="Rating")
    st.plotly_chart(fig, use_container_width=True)


def quality_of_life_eval(df):
    data = df["self_eval_health_quality"].dropna()

    counts = data.value_counts(normalize=True).sort_index()
    percent_df = counts.mul(100).round(1).reset_index()
    percent_df.columns = ["Rating", "Percent"]

    fig = px.bar(
        percent_df,
        x="Rating",
        y="Percent",
        text="Percent",
        title="Quality of Life Assessment",
    )
    fig.update_layout(yaxis_title="Percentage", xaxis_title="Rating")
    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    st.title("📊 Demography")
    st.markdown("---")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            biological_sex(df)
        with col2:
            health_insurance(df)

        st.markdown("---")

        row2 = st.columns(3)
        for col, chart in zip(
            row2, [age_distribution, education_level, marital_status]
        ):
            with col:
                chart(df)

        st.markdown("---")

        row3 = st.columns(3)
        for col, chart in zip(
            row3, [work_model, general_health_eval, quality_of_life_eval]
        ):
            with col:
                chart(df)
