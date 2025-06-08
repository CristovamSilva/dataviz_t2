import streamlit as st
import pandas as pd


def shape(df: pd.DataFrame):
    st.markdown(f"**Dataset Shape:** `{df.shape[0]}` rows x `{df.shape[1]}` columns")


def sample(df: pd.DataFrame, key: str):
    n = st.slider(
        "Select number of rows to sample",
        min_value=1,
        max_value=10,
        value=1,
        key=key,
    )
    st.dataframe(df.sample(n), use_container_width=True)


def columns(df: pd.DataFrame):
    with st.expander(f"🔍 Columns ({len(df.columns)})"):
        st.write(list(df.columns))


def show(df: pd.DataFrame):
    # st.title("📂 Dataset Overview")
    st.markdown("""
        ### 📌 About the Dataset
        This dataset originally contained **approximately 9,000 anonymous responses** of 70 questions that after processing generated **approximately 250 variables**, 
        collected through self-reported questionnaires. Each row represents an individual participant. After processing:
    """)

    shape(df)

    # columns(df)

    sample(df, key="overview")

    st.markdown("---")
