import streamlit as st
from pathlib import Path
BASE_PATH = Path(__file__).resolve().parents[0]
INFO_PATH = BASE_PATH / "info.md"
with open(INFO_PATH, 'r',encoding="utf-8") as file:
    st.markdown(file.read())