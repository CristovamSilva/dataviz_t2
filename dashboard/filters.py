import streamlit as st
import pandas as pd


def show(df: pd.DataFrame):
    st.sidebar.header("🔍 Filter Participants")

    # --- Set Default Filter Values ---
    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    sexes = df["biological_sex"].dropna().unique().tolist()

    selected_sexes = st.sidebar.multiselect(
        "Biological Sex",
        options=sexes,
        default=st.session_state.get("selected_sexes", sexes),
        key="selected_sexes",
    )

    # --- Filters Stored in Session ---
    age_range = st.sidebar.slider(
        "Age Range",
        min_value=age_min,
        max_value=age_max,
        value=st.session_state.get("age_range", (age_min, age_max)),
        key="age_range",
    )

    # --- Reset Button ---
    if st.sidebar.button("🔄 Reset Filters"):
        for key in ["age_range", "selected_sexes", "selected_edu"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # --- Apply Filters ---
    filtered_df = df[
        (df["age"] >= age_range[0])
        & (df["age"] <= age_range[1])
        & (df["biological_sex"].isin(selected_sexes))
    ]

    st.sidebar.markdown(f"**Participants: {len(filtered_df)} shown**")

    return filtered_df
