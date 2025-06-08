import streamlit as st
import pandas as pd
from dashboard import (
    dataset,
    demographic,
    financial,
    mental,
    nutritional,
    physical,
    sleep,
    clinical,
    filters,
)


##  Data Preparation
@st.cache_data
def load_data():
    return pd.read_csv("processed.csv")


df = load_data()
filtered_df = filters.show(df)

# Demographic DataFrame
demo_columns = [
    "age",
    "education_level",
    "work_model",
    "marital_status",
    "biological_sex",
    "health_insurance",
    "self_eval_health_quality",
    "self_eval_health_general",
]
demographic_df = filtered_df[demo_columns]

# Physical Health DataFrame
physical_columns = [
    "height",
    "weight",
    "bmi",
    "bmi_category",
    "healthy_weight",
    "obesity",
    "physical_activities",
    "active",
    "sedentary",
    "headache",
    "headache_weekly",
    "migraine",
    "back_pain_weekly",
    "body_pain_weekly",
    "sit_down_time_daily",
    "excessive_sit_down_time",
]
physical_df = filtered_df[physical_columns]

# Sleep Health DataFrame
sleep_columns = [
    "self_eval_sleep_quality",
    "sleep_hours",
    "apnea",
    "sleepness_day_time",
    "wake_up_tired",
    "sleep_break",
    "snore",
    "insomnia",
]
sleep_df = filtered_df[sleep_columns]

# Mental Health DataFrame
mental_columns = [
    "self_eval_mental_well_being",
    "burnout",
    "forgetfulness",
    "work_satisfaction",
    "suicide_risk",
    "anxiety",
    "depression",
    "is_isolated",
    "is_socially_active",
    "isolation",
    "low_quality_of_life",
    "meaningful_life",
    "meaningless_life",
    "socialization",
    "spirituality",
    "household_situation_alone",
    "household_situation_adults",
    "household_situation_parents",
    "household_situation_partner",
    "household_situation_pet",
]
mental_df = filtered_df[mental_columns]

# Nutritional Health Dataframe
nutritional_columns = [
    "self_eval_nutrition",
    "self_eval_nutrition_well_being",
    "fast_food",
    "fibers",
    "fruits",
    "processed",
    "soft_drink",
    "vegetables",
    "water_intake",
    "eat_fibers",
    "eat_fruits",
    "eat_vegetables",
    "good_water_intake",
    "high_fast_food_intake",
    "high_processed_intake",
    "high_sodium_intake",
    "high_soft_drink_intake",
    "high_cholesterol",
]
nutritional_df = filtered_df[nutritional_columns]

# Financial Health DataFrame
financial_columns = [
    "self_eval_finance_well_being",
    "debt",
    "emergency_reserve",
    "emergency_reserve_savings_period",
    "investments",
    "savings_money",
    "unexpected_expenses",
]
financial_df = filtered_df[financial_columns]

# Clinical DataFrame
clinical_columns = [
    "age",
    "years_lost",
    "heart_age",
    "bowel_movements",
    "constipation",
    "smoker",
    "quit_smoking",
    "use_medication",
    "polypharmacy",
    "medication_antidepressants",
    "medication_antipsychotics",
    "medication_anxiolytic",
    "medication_for_sleep",
    "medication_for_weight_loss",
    "appointments_dentist",
    "appointments_generalist",
    "appointments_nutritionist",
    "appointments_psychologist",
    "clean_family_history",
    "clean_medical_history",
    "high_cvd_risk",
    "high_cholesterol",
    "diabetes",
    "diabetes_lack_exams",
    "lack_exams_general",
    "cancer_lack_exams",
    "cardio_lack_exams",
]
clinical_df = filtered_df[clinical_columns]

## Configure Categories
categories = [
    {"name": "Demographic", "fn": demographic.show, "df": demographic_df},
    {"name": "Clinical Health", "fn": clinical.show, "df": clinical_df},
    {"name": "Physical Health", "fn": physical.show, "df": physical_df},
    {"name": "Sleep Health", "fn": sleep.show, "df": sleep_df},
    {"name": "Mental Health", "fn": mental.show, "df": mental_df},
    {"name": "Nutritional Health", "fn": nutritional.show, "df": nutritional_df},
    {"name": "Financial Health", "fn": financial.show, "df": financial_df},
    {"name": "Dataset", "fn": dataset.show, "df": df},
]

## Display the dashboard
st.markdown("""
# Health Survey Dashboard

Welcome to this interactive dashboard designed to explore responses from a large-scale health and lifestyle survey.

---
### 🔍 Dashboard Structure
Use the tabs below to explore different dimensions of the data:

- **Demographics**: Understand the respondents: age, sex, education, marital status, work model, insurance, and their self-assessed quality of life and well-being.
- **Health Blocks**: Analyze participants' perceptions of their health and their self-reported responses across multiple health domains.
- **Dataset**: Review the raw input data, including its column structure and representative sample entries.
---

""")

tabs = st.tabs([cat["name"] for cat in categories])

for tab, cat in zip(tabs, categories):
    with tab:
        cat["fn"](cat["df"])
