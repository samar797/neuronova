import streamlit as st
import os

st.set_page_config(
    page_title="AI Vocational Tutor",
    page_icon="🎓",
    layout="centered"
)

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if "users" not in st.session_state:
    st.session_state.users = []

if "user" not in st.session_state:
    st.session_state.user = None

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

# -------------------------------
# STREAM / PDF DATA
# -------------------------------
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

# -------------------------------
# SAFETY FUNCTION
# -------------------------------
def safe_get_stream_for_user(user_obj):
    if not user_obj:
        return None
    s = user_obj.get("stream")
    if s in stream_data:
        return s
    for key in stream_data.keys():
        if key.strip().lower() == str(s).strip().lower():
            return key
    return None


# -------------------------------
# PAGE UI
# -------------------------------
st.title("AI Vocational Tutor")
st.caption("Smart Learning for Vocational Students")

# ----------------------------------------------
# ACCOUNT CREATION SCREEN  (Before Quiz)
# ----------------------------------------------
if not st.session_state.login:

    st.subheader("Create Account")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    stream = st.selectbox("Vocational Stream", list(stream_data.keys()))

    if st.button("Register & Continue"):
        if new_user and new_pass:
            user_data = {
                "username": new_user,
                "password": new_pass,
                "stream": stream,
            }
            st.session_state.users.append(user_data)
            st.session_state.user = user_data
            st.session_state.login = True
            st.success("Account created successfully! Please complete the SDG Quiz.")
            st.rerun()
        else:
            st.warning("Please fill all fields.")


# ----------------------------------------------
# SDG QUIZ PAGE
# ----------------------------------------------
elif st.session_state.login and not st.session_state.quiz_done:

    st.subheader("🌍 SDG Awareness Quiz (Each question = 2 marks)")
    st.write("Please answer all questions.")

    q1 = st.radio("1. What does SDG stand for?",
                  ["Sustainable Development Goals", "Social Development Guide", "Science Development Group"], index=None)

    q2 = st.radio("2. How many SDGs are there?",
                  ["10", "15", "17"], index=None)

    q3 = st.radio("3. SDG 4 focuses on:",
                  ["Quality Education", "Clean Water", "Zero Hunger"], index=None)

    q4 = st.radio("4. SDG 12 promotes:",
                  ["Responsible Consumption & Production", "Gender Equality", "Life Below Water"], index=None)

    q5 = st.radio("5. SDG 3 is related to:",
                  ["Good Health and Well-being", "Affordable Energy", "Industry Innovation"], index=None)

    if st.button("Submit Quiz"):
        if None in [q1, q2, q3, q4, q5]:
            st.warning("⚠ Please answer all questions before submitting.")
        else:
            score = 0
            if q1 == "Sustainable Development Goals": score += 2
            if q2 == "17": score += 2
            if q3 == "Quality Education": score += 2
            if q4 == "Responsible Consumption & Production": score += 2
            if q5 == "Good Health and Well-being": score += 2

            st.session_state.quiz_score = score
            st.session_state.quiz_done = True
            st.success("Quiz Submitted Successfully!")
            st.rerun()


# ----------------------------------------------
# MAIN APP (Lessons + Score Display)
# ----------------------------------------------
else:
    user = st.session_state.user

    if not user:
        st.error("Session user missing — please register again.")
        if st.button("Restart"):
            st.session_state.login = False
            st.session_state.quiz_done = False
            st.session_state.quiz_score = None
            st.rerun()
    else:
        st.success(f"Welcome {user.get('username')}")
        st.info(f"Stream: {user.get('stream')}")

        if st.button("Logout"):
            st.session_state.login = False
            st.session_state.quiz_done = False
            st.session_state.quiz_score = None
            st.session_state.user = None
            st.rerun()

        st.divider()
        st.subheader("📘 Lessons")

        user_stream = safe_get_stream_for_user(user)

        if not user_stream:
            st.error("Invalid stream selected. Please re-register.")
            st.write("Available streams:", list(stream_data.keys()))
        else:
            lessons = stream_data.get(user_stream, [])
            stream_pdf_dict = pdf_map.get(user_stream, {})

            if not lessons:
                st.info("No lessons available for your stream yet.")
            else:
                for lesson in lessons:
                    if st.button(lesson):
                        pdf_path = stream_pdf_dict.get(lesson)

                        if not pdf_path:
                            st.error("PDF not mapped for this lesson yet.")
                            continue

                        if os.path.exists(pdf_path):
                            st.success(f"PDF Loaded: {lesson}")
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    label="Download Lesson PDF",
                                    data=f,
                                    file_name=os.path.basename(pdf_path),
