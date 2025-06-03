import streamlit as st
import pandas as pd
from .dataset import sample, columns


def template(title: str, df: pd.DataFrame):
    st.title(title)
    columns(df)
    sample(df, n=2)
