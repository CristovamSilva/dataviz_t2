import streamlit as st
import pandas as pd
from .dataset import sample, columns


def template(title: str, df: pd.DataFrame):
    st.title(title)
    st.markdown("---")
    st.markdown("#### **Data Preview**")
    sample(df, key=title)
    columns(df)
