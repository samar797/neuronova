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

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

# ------------------------
# STREAMS + PDFs
# ------------------------
stream_data = {
    "Jewellery Making": [
        "terracotta jewellery",
        "beaded jewellery",
        "thread jewellery"
    ],
    "Candle And Soap Making": [
        "scented candle",
        "organic soap"
    ],
}

pdf_map = {
    "Jewellery Making": {
        "terracotta jewellery": "lesson_pdfs/Jewellery_Making/terracotta.pdf",
        "beaded jewellery": "lesson_pdfs/Jewellery_Making/beaded.pdf",
        "thread jewellery": "lesson_pdfs/Jewellery_Making/threaded.pdf",
    },
    "Candle And Soap Making": {
        "scented candle": "lesson_pdfs/Candle_And_Soap_Making/scented candle.pdf",
        "organic soap": "lesson_pdfs/Candle_And_Soap_Making/organic soap.pdf",
    }
}

# ------------------------
# Helper
# ------------------------
def safe_stream(s):
    if not s:
        return None
    for key in stream_data:
        if key.lower() == s.lower():
            return key
    return None


# ------------------------
# UI
# ------------------------
st.title("AI Vocational Tutor")
st.caption("Smart Learning for Vocational Students")

# ----------------------------------
# REGISTER PAGE
# ----------------------------------
if not st.session_state.login:

    st.subheader("Create Account")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    stream = st.selectbox("Select Vocational Stream", list(stream_data.keys()))

    if st.button("Register & Continue"):
        if username and password:
            st.session_state.user = {
                "username": username,
                "password": password,
                "stream": stream
            }
            st.session_state.login = True
            st.rerun()
        else:
            st.warning("Please fill all fields.")


# ----------------------------------
# SDG QUIZ PAGE
# ----------------------------------
elif st.session_state.login and not st.session_state.quiz_done:

    st.subheader("🌍 SDG Quiz (Each question = 2 marks)")
    st.write("Answer all questions to continue.")

    q1 = st.radio("1. What is the main goal of SDG 4:", 
                   ["Ensure healthy lives", "Promote lifelong learning and quality education", "Achieve Gender Equality","End hunger"], index=None)
    q2 = st.radio("2. By which year does SDG 4 aim to achieve universal primary and secondary education?:", ["2025", "2030", "2050", "2040"], index=None)
    q3 = st.radio("3. Which group does SDG 4 emphasize for equal access to education?:", ["Only adults","Only people in cities","Girls, children with disabilities, and vulnerable groups","Only university students"], index=None)
    q4 = st.radio("4. Which skill is highlighted by SDG 4 as important for employment?:", ["Basic reading", "Technical and vocational skills", "Public speaking", "Sports skills"], index=None)
    q5 = st.radio("5. SDG 4 supports the building of safe and inclusive school environments. What does this include?", "options": ["Free uniforms","Access to internet and electricity","More school holidays","Only sports facilities"],index=None)

    if st.button("Submit Quiz"):
        if None in [q1, q2, q3, q4, q5]:
            st.warning("Please answer all questions.")
        else:
            score = 0
            if q1 == "Promote lifelong learning and quality education for all": score += 2
            if q2 == "2030": score += 2
            if q3 == "Girls, children with disabilities, and vulnerable groups": score += 2
            if q4 == "Technical and vocational skills": score += 2
            if q5 == "Access to internet and electricity": score += 2

            st.session_state.quiz_score = score
            st.session_state.quiz_done = True
            st.success("Quiz Submitted!")
            st.rerun()


# ----------------------------------
# LESSONS PAGE (AFTER QUIZ)
# ----------------------------------
else:

    user = st.session_state.user
    stream_name = safe_stream(user["stream"])

    st.success(f"Welcome {user['username']}")
    st.info(f"Stream: {stream_name}")

    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.quiz_done = False
        st.session_state.quiz_score = None
        st.session_state.user = None
        st.rerun()

    st.subheader("📘 Lessons")

    # FIX: ENSURE LESSONS ALWAYS SHOW
    lessons = stream_data.get(stream_name, [])

    if not lessons:
        st.error("⚠ No lessons found for your stream (Check spelling).")

    # Show ALL lesson buttons (not depending on clicking)
    for lesson in lessons:
        st.write(f"### 📗 {lesson}")
        pdf_path = pdf_map[stream_name].get(lesson)

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF",
                    data=f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    key=lesson
                )
        else:
            st.error(f"PDF NOT FOUND: {pdf_path}")

    st.divider()

    # SHOW SCORE BELOW LESSONS
    if st.session_state.quiz_score is not None:
        st.subheader("📝 Your SDG Quiz Score")
        st.success(f"Score: **{st.session_state.quiz_score}/10**")
