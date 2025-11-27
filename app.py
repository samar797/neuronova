import streamlit as st
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Vocational Tutor",
    page_icon="🎓",
    layout="centered"
)

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False

if "users" not in st.session_state:
    st.session_state.users = []

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SAMPLE CONTENT ----------------
stream_data = {
    "jewellery making": ["terracotta jewellery", "beaded jewellery", "threaded jewellery"],
    "Candle And Soap Making": ["scented candle", "organic soap"],
}

# ---------------- PDF BACKEND MAPPING ----------------
pdf_map = {
    "jewellery making": {
        "terracotta jewellery": "lesson_pdfs/jewellery_making/terracotta.pdf",
        "beaded jewellery": "lesson_pdfs/jewellery_making/beaded.pdf",
        "thread jewellery": "lesson_pdfs/jewellery_making/threaded.pdf",
    },
    "Candle And Soap Making": {
        "scented candles": "lesson_pdfs/candle_and_soap_making/scented_candles.pdf",
        "organic soaps": "lesson_pdfs/candle_and_soap_making/organic_soaps.pdf",
    }
}

# ---------------- UI ----------------
st.title("🎓 AI Vocational Tutor")
st.caption("Smart Learning for Vocational Students")

# ---------------- ONLY SIGN UP (NO LOGIN) ----------------
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

            st.success("Account created successfully!")
            st.rerun()
        else:
            st.warning("Please fill all fields.")

# ---------------- MAIN DASHBOARD ----------------
else:
    user = st.session_state.user

    st.success(f"Welcome {user['username']}")
    st.info(f"Stream: {user['stream']}")

    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.user = None
        st.rerun()

    st.divider()

    # ---------------- LESSONS WITH PDF BACKEND ----------------
    st.subheader("📚 Lessons")

    for lesson in stream_data[user["stream"]]:
        if st.button(lesson):
            pdf_path = pdf_map[user["stream"]][lesson]

            if os.path.exists(pdf_path):
                st.success(f"PDF Ready: {lesson}")

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Lesson PDF",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.error("❌ PDF not found. Please upload it on GitHub.")

    st.divider()

    # ---------------- AI TUTOR ----------------
    st.subheader("🤖 Ask AI Tutor")
    question = st.text_area("Ask your question")

    if st.button("Get Answer"):
        if question:
            st.write("**AI Response (Demo):**")
            st.info(
                f"This is a demo AI answer for {user['stream']} student."
            )
        else:
            st.warning("Please enter a question.")
