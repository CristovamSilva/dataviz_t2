import streamlit as st
import pandas as pd
import plotly.express as px
from .health_dash import template


def show(df: pd.DataFrame):
    df["age"] = df["heart_age"] - df["years_lost"]
    template("🩺 Clinical Health", df)
    heart_age(df)
    smoking(df)
    bowel_health(df)
    medication_usage(df)
    medical_followup(df)
    health_history(df)
    exam_gaps(df)


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

    # Add flat line at 0 for reference
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="green",
        annotation_text="Ideal: No Years Lost",
        annotation_position="bottom right",
    )

    # Force visible baseline and allow negative range
    fig.update_layout(
        yaxis=dict(title="Years Lost", range=[-5, 15]),  # adjust as needed
        xaxis_title="Actual Age",
        hovermode="x unified",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)


def smoking(df):
    st.subheader("🚬 Smoking Behavior: Status vs Quit Intention")

    # Derive smoking status
    df["smoking_status"] = df.apply(
        lambda row: "Non-smoker"
        if not row["smoker"]
        else "Smoker: Wants to Quit"
        if row["quit_smoking"]
        else "Smoker: Doesn't Want to Quit",
        axis=1,
    )

    # Count and calculate percentages
    counts = df["smoking_status"].value_counts(normalize=True).reset_index()
    counts.columns = ["Smoking Status", "Proportion"]
    counts["Percentage"] = (counts["Proportion"] * 100).round(1)

    # Plot as percent
    fig = px.bar(
        counts,
        x="Smoking Status",
        y="Percentage",
        color="Smoking Status",
        text="Percentage",
        title="Smoking Status (as Percentage of Population)",
        color_discrete_sequence=["#59a14f", "#edc949", "#e15759"],
    )

    fig.update_layout(
        showlegend=False,
        yaxis_title="Percentage of People",
        xaxis_title=None,
        yaxis=dict(range=[0, 100]),
    )
    st.plotly_chart(fig, use_container_width=True)


# --- Bowel Health ---
def bowel_health(df: pd.DataFrame):
    st.subheader("🧻 Bowel Health")

    # 1. Bowel movements per week
    fig1 = px.histogram(
        df,
        x="bowel_movements",
        nbins=8,
        title="Bowel Movements per Week",
        labels={"bowel_movements": "Days per Week"},
        color_discrete_sequence=["#4e79a7"],
    )
    fig1.update_layout(xaxis=dict(dtick=1), yaxis_title="Number of People")
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Constipation prevalence
    counts = (
        df["constipation"].value_counts(normalize=True).reindex([True, False]).fillna(0)
    )
    data = pd.DataFrame(
        {
            "Response": ["Yes", "No"],
            "Percent": [round(counts[True] * 100, 1), round(counts[False] * 100, 1)],
        }
    )

    fig2 = px.pie(
        data,
        names="Response",
        values="Percent",
        title="Constipation (Self-Reported)",
        color_discrete_sequence=["#e15759", "#bab0ac"],
    )
    fig2.update_traces(textinfo="label+percent")
    st.plotly_chart(fig2, use_container_width=True)


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
        color_discrete_map={"Yes": "#e15759", "No": "#bab0ac"},
        title="Medication and Drug Use",
    )
    fig.update_layout(xaxis_tickangle=30, yaxis_title="Percentage")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


# --- Medical Follow-up ---
def medical_followup(df: pd.DataFrame):
    st.subheader("🩺 Health Professional Appointments")

    columns = {
        "appointments_dentist": "Dentist",
        "appointments_generalist": "General Practitioner",
        "appointments_nutritionist": "Nutritionist",
        "appointments_psychologist": "Psychologist",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes = round(counts[True] * 100, 1)
        no = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes, "No": no})

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
        title="Appointments with Health Professionals",
    )
    fig.update_layout(xaxis_tickangle=30, yaxis_title="Percentage")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


# --- Health History ---
def health_history(df: pd.DataFrame):
    st.subheader("📋 Personal and Family Medical History")

    columns = {
        "clean_family_history": "No Family Medical History",
        "clean_medical_history": "No Personal Medical History",
    }

    data = []
    for col, label in columns.items():
        counts = df[col].value_counts(normalize=True).reindex([True, False]).fillna(0)
        yes = round(counts[True] * 100, 1)
        no = round(counts[False] * 100, 1)
        data.append({"Label": label, "Yes": yes, "No": no})

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
        title="Clean Medical Background",
    )
    fig.update_layout(xaxis_tickangle=30, yaxis_title="Percentage")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
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
        color_discrete_map={"Yes": "#f28e2b", "No": "#bab0ac"},
        title="Lack of Preventive Exams",
    )
    fig.update_layout(xaxis_tickangle=30, yaxis_title="Percentage")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
