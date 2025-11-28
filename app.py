import streamlit as st
import os

st.set_page_config(
    page_title="AI Vocational Tutor",
    page_icon="🎓",
    layout="centered"
)

# ------------------------
# SESSION SETUP
# ------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if "user" not in st.session_state:
    st.session_state.user = None

if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

if "quiz_score" not in st._
