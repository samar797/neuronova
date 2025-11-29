import streamlit as st
import os

# ----------------- Page Configuration -----------------
st.set_page_config(page_title="AI Vocational Tutor", layout="centered")

# ----------------- Session State Initialization -----------------
if "login" not in st.session_state: 
    st.session_state.login = False
if "user" not in st.session_state: 
    st.session_state.user = None
if "quiz_done" not in st.session_state: 
    st.session_state.quiz_done = False
if "quiz_score" not in st.session_state: 
    st.session_state.quiz_score = None

# ----------------- Streams and Lessons -----------------
stream_data = {
    "Jewellery Making": ["Terracotta Jewellery", "Beaded Jewellery", "Thread Jewellery"],
    "Candle And Soap Making": ["Scented Candle", "Organic Soap"],
}

# PDF paths for each lesson
pdf_map = {
    "Jewellery Making": {
        "Terracotta Jewellery": "lesson_pdfs/Jewellery_Making/terracotta.pdf",
        "Beaded Jewellery": "lesson_pdfs/Jewellery_Making/beaded.pdf",
        "Thread Jewellery": "lesson_pdfs/Jewellery_Making/threaded.pdf",
    },
    "Candle And Soap Making": {
        "Scented Candle": "lesson_pdfs/Candle_And_Soap_Making/scented candle.pdf",
        "Organic Soap": "lesson_pdfs/Candle_And_Soap_Making/organic soap.pdf",
    }
}

# Short video links for each lesson
video_map = {
    "Jewellery Making": {
        "Terracotta Jewellery": "https://youtube.com/embed/xLnv2H6oIyE",
        "Beaded Jewellery": "https://youtube.com/embed/cfzRxrWtOKY",
        "Thread Jewellery": "https://youtube.com/embed/ZI0i_b8fhu4",
    },
    "Candle And Soap Making": {
        "Scented Candle": "https://youtube.com/embed/0KIQrn-NuL0",
        "Organic Soap": "https://youtube.com/embed/MxXXWymDpuc",
    }
}

# ----------------- SDG Quiz -----------------
sdg_questions = [
    ("Which skill promotes traditional learning that supports creativity and income generation?", 
     ["Communicative English","Jewellery Making","Computer Skills","Soap Making"], "Jewellery Making"),
    ("Which learning teaches practical skills that can lead to self-employment?", 
     ["Candle Making","Maths Learning","Spoken English","Scientific Learning"], "Candle Making"),
    ("Which skill helps students learn chemistry and entrepreneurship together?", 
     ["Soap Making","Jewellery Making","Computer Skills","Baking"], "Soap Making"),
    ("SDG 4 promotes vocational and technical skills. Which activity is an example of this?", 
     ["Jewellery Making","Watching TV","Playing Video Games","Listening To Music"], "Jewellery Making"),
    ("How can jewellery making help students achieve SDG 4’s aim of lifelong learning?", 
     ["By teaching a skill they can continue improving and earning",
      "By forcing them to memorize facts",
      "By limiting creativity",
      "By focusing only on theory"], 
     "By teaching a skill they can continue improving and earning"),
]

# Helper function to safely match stream names
def safe_stream(stream_name):
    for key in stream_data:
        if key.lower() == stream_name.lower():
            return key
    return None

# ----------------- App Title -----------------
st.title("🎓 AI Vocational Tutor")
st.write("Welcome to the AI-powered vocational learning platform! Learn, watch, and practice skills from your selected stream.")

# ----------------- Registration Flow -----------------
if not st.session_state.login:
    st.subheader("Create Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    selected_stream = st.selectbox("Select Your Stream", list(stream_data.keys()))

    if st.button("Register"):
        if username and password:
            st.session_state.user = {"username": username, "stream": selected_stream}
            st.session_state.login = True
            st.success(f"Welcome {username}! You have registered successfully.")
            st.experimental_rerun()
        else:
            st.warning("Please enter both username and password.")

# ----------------- SDG Entry Quiz -----------------
elif not st.session_state.quiz_done:
    st.subheader("📝 SDG Entry Quiz")
    st.write("Answer the following questions to begin your learning journey:")

    answers = []
    for i, (question, options, _) in enumerate(sdg_questions):
        answer = st.radio(f"{i+1}. {question}", options, key=f"sdg{i}")
        answers.append(answer)

    if st.button("Submit Quiz"):
        if any(a is None for a in answers):
            st.warning("Please answer all questions before submitting.")
        else:
            score = sum(2 for i, a in enumerate(answers) if a == sdg_questions[i][2])
            st.session_state.quiz_score = score
            st.session_state.quiz_done = True
            st.success(f"Quiz completed! Your score: {score}/10")
            st.experimental_rerun()

# ----------------- Dashboard -----------------
else:
    user = st.session_state.user
    stream_name = safe_stream(user["stream"])
    st.success(f"Welcome back, {user['username']}! | SDG Quiz Score: {st.session_state.quiz_score}/10")

    st.write("Here are your lessons for the selected stream:")

    for lesson in stream_data[stream_name]:
        st.subheader(f"📘 {lesson}")

        # PDF Download
        pdf_path = pdf_map[stream_name][lesson]
        with open(pdf_path, "rb") as f:
            st.download_button("Download Lesson PDF", f, file_name=os.path.basename(pdf_path))

        # Lesson Video
        st.components.v1.iframe(video_map[stream_name][lesson], height=360)

        st.divider()
