import streamlit as st
import pandas as pd


def shape(df: pd.DataFrame):
    st.markdown(f"**Dataset Shape:** `{df.shape[0]}` rows x `{df.shape[1]}` columns")


def sample(df: pd.DataFrame, n: int = 5):
    st.markdown("**Sample Rows:**")
    st.dataframe(df.sample(n), use_container_width=True)


def columns(df: pd.DataFrame):
    with st.expander(f"🔍 View All Column Names ({len(df.columns)})"):
        st.write(list(df.columns))


def show(df: pd.DataFrame):
    # st.title("📂 Dataset Overview")
    st.markdown("""
        ### 📌 About the Dataset
        This dataset originally contained **approximately 8,000 anonymous responses** of 70 questions that after processing generated **approximately 200 variables**, 
        collected through self-reported questionnaires. Each row represents an individual participant.
    """)

    shape(df)

    # columns(df)

    sample(df, n=5)

    st.markdown("---")
