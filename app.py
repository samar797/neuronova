import streamlit as st
import os

st.set_page_config(page_title="AI Vocational Tutor", layout="centered")

if "login" not in st.session_state: st.session_state.login = False
if "user" not in st.session_state: st.session_state.user = None
if "quiz_done" not in st.session_state: st.session_state.quiz_done = False
if "quiz_score" not in st.session_state: st.session_state.quiz_score = None

stream_data = {
    "Jewellery Making": ["Terracotta Jewellery", "Beaded Jewellery", "Thread Jewellery"],
    "Candle And Soap Making": ["Scented Candle", "Organic Soap"],
}

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

shorts_map = {
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

sdg_questions = [
    ("Which skill promotes traditional learning that supports creativity and income generation?", ["Communicative English","Jewellery Making","Computer Skills","Soap Making"], "Jewellery Making"),
    ("Which learning teaches practical skills that can lead to self-employment?", ["Candle Making","Maths Learning","Spoken English","Scientific Learning"], "Candle Making"),
    ("Which skill helps students learn chemistry and entrepreneurship together?", ["Soap Making","Jewellery Making","Computer Skills","Baking"], "Soap Making"),
    ("SDG 4 promotes vocational and technical skills. Which activity is an example of this?", ["Jewellery Making","Watching TV","Playing Video Games","Listening To Music"], "Jewellery Making"),
    ("How can jewellery making help students achieve SDG 4’s aim of lifelong learning?", ["By teaching a skill they can continue improving and earning","By forcing them to memorize facts","By limiting creativity","By focusing only on theory"], "By teaching a skill they can continue improving and earning"),
]

def safe_stream(s):
    for k in stream_data:
        if k.lower() == s.lower():
            return k
    return None

st.title("AI Vocational Tutor")


if not st.session_state.login:
    u = st.text_input("Create Username")
    p = st.text_input("Create Password", type="password")
    s = st.selectbox("Select Stream", list(stream_data.keys()))

    if st.button("Register"):
        if u and p:
            st.session_state.user = {"username": u, "stream": s}
            st.session_state.login = True
            st.rerun()

elif not st.session_state.quiz_done:
    st.subheader("SDG Entry Quiz")

    answers = []
    for i,(q,opt,_) in enumerate(sdg_questions):
        a = st.radio(f"{i+1}. {q}", opt, key=f"sdg{i}", index=None)
        answers.append(a)

    if st.button("Submit Sdg Quiz"):
        if any(a is None for a in answers):
            st.warning("Answer all questions")
        else:
            score = 0
            for i,a in enumerate(answers):
                if a == sdg_questions[i][2]:
                    score += 2

            st.session_state.quiz_score = score
            st.session_state.quiz_done = True
            st.success(f"SDG Quiz Passed! Score: {score}/10")
            st.rerun()


else:
    user = st.session_state.user
    stream_name = safe_stream(user["stream"])
    st.success(f"Welcome {user['username']} | SDG Score: {st.session_state.quiz_score}/10")

    for lesson in stream_data[stream_name]:
        st.subheader(lesson)

        
        with open(pdf_map[stream_name][lesson], "rb") as f:
            st.download_button("Download PDF", f, file_name=os.path.basename(pdf_map[stream_name][lesson]))

      
        st.components.v1.iframe(shorts_map[stream_name][lesson], height=360)

        st.divider()
