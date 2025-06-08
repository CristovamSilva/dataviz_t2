import streamlit as st
import pandas as pd
import plotly.express as px
from .health_dash import template


def heart_age(df: pd.DataFrame):
    st.markdown("### Heart Age")
    st.markdown(
        "Heart age is a measure of your cardiovascular health, indicating how your heart's age compares to your actual age. A lower heart age suggests better heart health."
    )

    # Group by actual age
    avg_lost = df.groupby("age")["years_lost"].mean().reset_index()

    # Plot
    fig = px.line(
        avg_lost,
        x="age",
        y="years_lost",
        title="🩺 Average Cardiovascular Years Lost by Age",
        labels={"age": "Actual Age", "years_lost": "Years Lost (Heart Age - Age)"},
    )

    # Make the line red and thicker
    fig.update_traces(line=dict(color="#e15759", width=3))

    # Add flat line at 0 for reference
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="green",
        annotation_text="Ideal: No Years Lost",
        annotation_position="bottom right",
    )

    # Adjust layout
    fig.update_layout(
        yaxis=dict(title="Years Lost", range=[-5, 15]),
        xaxis_title="Actual Age",
        hovermode="x unified",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def smoking(df):
    st.subheader("🚬 Smoking Behavior")

    df["smoking_status"] = df["smoker"].map({True: "Smoker", False: "Non-smoker"})

    col1, col2 = st.columns(2)

    # --- Chart 1: Smokers vs Non-smokers in population ---
    status_counts = df["smoking_status"].value_counts(normalize=True).reset_index()
    status_counts.columns = ["Smoking Status", "Proportion"]
    status_counts["Percentage"] = (status_counts["Proportion"] * 100).round(1)

    with col1:
        fig1 = px.bar(
            status_counts,
            x="Smoking Status",
            y="Percentage",
            color="Smoking Status",
            text="Percentage",
            title="Population: Smokers vs Non-smokers",
            color_discrete_sequence=["#59a14f", "#e15759"],
        )
        fig1.update_layout(
            showlegend=False,
            yaxis_title="Percentage",
            xaxis_title=None,
            yaxis=dict(range=[0, 100]),
        )
        st.plotly_chart(fig1, use_container_width=True)

    # --- Chart 2: Among smokers, quit intention ---
    smoker_df = df[df["smoker"] == True]
    if not smoker_df.empty:
        smoker_df["quit_status"] = smoker_df["quit_smoking"].map(
            {True: "Wants to Quit", False: "Doesn't Want to Quit"}
        )
        smoker_counts = (
            smoker_df["quit_status"].value_counts(normalize=True).reset_index()
        )
        smoker_counts.columns = ["Quit Intention", "Proportion"]
        smoker_counts["Percentage"] = (smoker_counts["Proportion"] * 100).round(1)

        with col2:
            fig2 = px.bar(
                smoker_counts,
                x="Quit Intention",
                y="Percentage",
                color="Quit Intention",
                text="Percentage",
                title="Among Smokers: Quit Intention",
                color_discrete_sequence=["#59a14f", "#e15759"],
            )
            fig2.update_layout(
                showlegend=False,
                yaxis_title="Percentage",
                xaxis_title=None,
                yaxis=dict(range=[0, 100]),
            )
            st.plotly_chart(fig2, use_container_width=True)


# --- Bowel Health ---
def bowel_health(df: pd.DataFrame):
    st.subheader("🧻 Bowel Health")

    counts = (
        df["constipation"]
        .value_counts(normalize=True)
        .reset_index()
        .replace({True: "Constipated", False: "Not Constipated"})
    )
    counts.columns = ["label", "value"]

    fig = px.pie(
        counts,
        names="label",
        values="value",
        hole=0.3,
        color="label",
        color_discrete_map={
            "Constipated": "#e15759",  # red
            "Not Constipated": "#59a14f",  # green
        },
    )

    fig.update_traces(textinfo="percent+label", showlegend=False)
    fig.update_layout(
        title_text="Constipation (Self-Reported)",
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        margin=dict(t=40, b=10, l=10, r=10),
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Medication Use ---
def medication_usage(df: pd.DataFrame):
    st.subheader("💊 Medication Use")

    columns = {
        "use_medication": "Uses Medication",
        "polypharmacy": "Takes 5+ Medications",
        "medication_antidepressants": "Antidepressants",
        "medication_antipsychotics": "Antipsychotics",
        "medication_anxiolytic": "Anxiolytics",
        "medication_for_sleep": "Sleep Medication",
        "medication_for_weight_loss": "Weight Loss Medication",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes = round(counts[True] * 100, 1)
        no = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes, "No": no})

    # Maintain defined order top-to-bottom
    ordered_labels = list(columns.values())
    plot_df = pd.DataFrame(data).melt(
        id_vars="Label", var_name="Response", value_name="Percent"
    )
    plot_df["Label"] = pd.Categorical(
        plot_df["Label"], categories=ordered_labels, ordered=True
    )

    fig = px.bar(
        plot_df,
        y="Label",
        x="Percent",
        color="Response",
        barmode="stack",
        orientation="h",
        text="Percent",
        color_discrete_map={"Yes": "#e15759", "No": "#bab0ac"},
        title="Medication and Drug Use",
        category_orders={"Label": ordered_labels},
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis_title=None,
        xaxis_title=None,
        showlegend=True,
        bargap=0.2,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%", textposition="inside", insidetextanchor="middle"
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Medical Follow-up ---
def medical_followup(df: pd.DataFrame):
    st.subheader("🩺 Health Professional Appointments")

    columns = {
        "appointments_generalist": "General Practitioner",
        "appointments_dentist": "Dentist",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes = round(counts[True] * 100, 1)
        no = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes, "No": no})

    ordered_labels = list(columns.values())
    plot_df = pd.DataFrame(data).melt(
        id_vars="Label", var_name="Response", value_name="Percent"
    )
    plot_df["Label"] = pd.Categorical(
        plot_df["Label"], categories=ordered_labels, ordered=True
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
        title="Health Appointments",
        category_orders={"Label": ordered_labels},
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis_title=None,
        xaxis_title=None,
        showlegend=True,
        bargap=0.2,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%", textposition="inside", insidetextanchor="middle"
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Health History ---
def health_history(df: pd.DataFrame):
    st.subheader("📋 Personal and Family Medical History")

    columns = {
        "clean_medical_history": "No Personal Medical History",
        "clean_family_history": "No Family Medical History",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes = round(counts[True] * 100, 1)
        no = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes, "No": no})

    ordered_labels = list(columns.values())
    plot_df = pd.DataFrame(data).melt(
        id_vars="Label", var_name="Response", value_name="Percent"
    )
    plot_df["Label"] = pd.Categorical(
        plot_df["Label"], categories=ordered_labels, ordered=True
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
        title="Clean Medical Background",
        category_orders={"Label": ordered_labels},
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis_title=None,
        xaxis_title=None,
        showlegend=True,
        bargap=0.2,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%", textposition="inside", insidetextanchor="middle"
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Preventive Exams ---
def exam_gaps(df: pd.DataFrame):
    st.subheader("🧪 Preventive Screening Gaps")

    columns = {
        "lack_exams_general": "General Check-ups Missing",
        "diabetes_lack_exams": "Diabetes Exams Missing",
        "cancer_lack_exams": "Cancer Screening Missing",
        "cardio_lack_exams": "Cardiovascular Exams Missing",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes = round(counts[True] * 100, 1)
        no = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes, "No": no})

    ordered_labels = list(columns.values())
    plot_df = pd.DataFrame(data).melt(
        id_vars="Label", var_name="Response", value_name="Percent"
    )
    plot_df["Label"] = pd.Categorical(
        plot_df["Label"], categories=ordered_labels, ordered=True
    )

    fig = px.bar(
        plot_df,
        y="Label",
        x="Percent",
        color="Response",
        barmode="stack",
        orientation="h",
        text="Percent",
        color_discrete_map={"Yes": "#e15759", "No": "#bab0ac"},
        title="Preventive Exams Missing",
        category_orders={"Label": ordered_labels},
    )

    fig.update_layout(
        xaxis=dict(showgrid=False, visible=False),
        yaxis_title=None,
        xaxis_title=None,
        showlegend=True,
        bargap=0.2,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%", textposition="inside", insidetextanchor="middle"
    )

    st.plotly_chart(fig, use_container_width=True)


def show(df: pd.DataFrame):
    template("🩺 Clinical Health", df)

    st.markdown("---")
    heart_age(df)
    st.markdown("---")
    bowel_health(df)
    st.markdown("---")
    smoking(df)
    st.markdown("---")
    medication_usage(df)
    st.markdown("---")
    health_history(df)
    st.markdown("---")
    medical_followup(df)
    st.markdown("---")
    exam_gaps(df)
    st.markdown("---")
