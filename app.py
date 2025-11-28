import streamlit as st
import os
import openai

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

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
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------------
# STREAMS + PDFs
# ------------------------
stream_data = {
    "Jewellery Making": ["terracotta jewellery", "beaded jewellery", "thread jewellery"],
    "Candle And Soap Making": ["scented candle", "organic soap"],
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

shorts_map = {
    "Jewellery Making": {
        "terracotta jewellery": "https://youtube.com/embed/xLnv2H6oIyE?si=gLYrTJJF4cfoS_QP",
        "beaded jewellery": "https://youtube.com/embed/cfzRxrWtOKY?si=gLZ3yPZpyFFzeBXK",
        "thread jewellery": "https://youtube.com/embed/ZI0i_b8fhu4?si=NQIjN6dB00R3vlbX",
    },
    "Candle And Soap Making": {
        "scented candle": "https://youtube.com/embed/0KIQrn-NuL0?si=jN7KeAQD1s7Np7tJ",
        "organic soap": "https://youtube.com/embed/MxXXWymDpuc?si=KibxUlnF6gIzMlMU",
    }
}

# ------------------------
# Helper Functions
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
            st.session_state.user = {"username": username, "password": password, "stream": stream}
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

    q1 = st.radio(
        "1. Which skill promotes traditional learning that supports creativity and income generation:",
        ["Communicative english","Jewellery making","Computer skills","Soap making"], index=None
    )
    q2 = st.radio(
        "2. Which learning teaches practical skills that can lead to self-employment?:",
        ["Candle making","Maths learning", "Spoken english", "Scientific learning"], index=None
    )
    q3 = st.radio(
        "3. Which skill helps students learn chemistry and entrepreneurship together?:",
        ["Jewellery making","Computer skills","Soap making","Baking"], index=None
    )
    q4 = st.radio(
        "4. SDG 4 promotes vocational and technical skills. Which activity is an example of this?:",
        ["Jewellery making", "Watching TV", "Playing video games", "Listening to music"], index=None
    )
    q5 = st.radio(
        "5. How can jewellery making help students achieve SDG 4’s aim of “lifelong learning?",
        ["By teaching a skill they can continue improving and earning from",
         "By forcing them to memorize facts",
         "By limiting creativity",
         "Only sports facilities"], index=None
    )

    if st.button("Submit Quiz"):
        if None in [q1, q2, q3, q4, q5]:
            st.warning("Please answer all questions.")
        else:
            score = 0
            if q1 == "Jewellery making": score += 2
            if q2 == "Candle making": score += 2
            if q3 == "Soap making": score += 2
            if q4 == "Jewellery making": score += 2
            if q5 == "By teaching a skill they can continue improving and earning from": score += 2

            st.session_state.quiz_score = score
            st.session_state.quiz_done = True
            st.success("Quiz Submitted!")
            st.rerun()

# ----------------------------------
# LESSONS & AI TUTOR PAGE
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
        st.session_state.chat_history = []
        st.rerun()

    st.subheader("📘 Lessons")
    lessons = stream_data.get(stream_name, [])

    if not lessons:
        st.error("⚠ No lessons found for your stream (Check spelling).")

    # Show lessons with PDF and YouTube Shorts
    for lesson in lessons:
        st.write(f"### 📗 {lesson}")

        # PDF DOWNLOAD
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

        # YOUTUBE SHORT EMBED
        video_url = shorts_map[stream_name].get(lesson)
        if video_url:
            st.write("🎬 **Watch Tutorial Video:**")
            st.components.v1.iframe(video_url, height=380)
        else:
            st.warning("No video available for this lesson.")

        st.divider()

    # ----------------------------------
    # AI VOCATIONAL TUTOR
    # ----------------------------------
    st.subheader("🤖 AI Vocational Tutor")
    st.write("Ask any question about your vocational lesson.")

    user_question = st.text_input("Ask your question here", key="user_question_input")

    if st.button("Ask AI"):
        if user_question:
            st.session_state.chat_history.append({"role": "user", "content": user_question})

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.chat_history
                )
                ai_answer = response["choices"][0]["message"]["content"]
                st.session_state.chat_history.append({"role": "assistant", "content": ai_answer})
            except Exception as e:
                st.error(f"Error: {e}")

    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**🧑‍🎓 You:** {chat['content']}")
        else:
            st.markdown(f"**🤖 AI Tutor:** {chat['content']}")

    # SHOW SCORE BELOW LESSONS
    if st.session_state.quiz_score is not None:
        st.subheader("📝 Your SDG Quiz Score")
        st.success(f"Score: **{st.session_state.quiz_score}/10**")
