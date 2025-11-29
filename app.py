import streamlit as st
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Vocational Tutor", layout="centered")

# ---------------- SESSION STATES ----------------
if "login" not in st.session_state: st.session_state.login = False
if "user" not in st.session_state: st.session_state.user = None
if "quiz_done" not in st.session_state: st.session_state.quiz_done = False
if "quiz_score" not in st.session_state: st.session_state.quiz_score = None
if "lesson_quiz_scores" not in st.session_state: st.session_state.lesson_quiz_scores = {}

# ---------------- STREAM DATA ----------------
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

# ---------------- SDG ENTRY QUIZ ----------------
sdg_questions = [
    ("Which skill promotes traditional learning?", ["Jewellery making","Computer skills","English","Maths"], "Jewellery making"),
    ("Which skill leads to self-employment?", ["Candle making","Physics","Biology","English"], "Candle making"),
    ("Which skill teaches chemistry also?", ["Soap making","Dance","Music","Sports"], "Soap making"),
    ("Which activity supports SDG 4?", ["Jewellery making","Gaming","TV","Reels"], "Jewellery making"),
    ("Lifelong learning means:", ["Learning for life","One day study","Forced study","No study"], "Learning for life"),
]

# ---------------- 50 LESSON QUESTIONS (10 PER LESSON) ----------------
lesson_question_bank = {

"Terracotta Jewellery": [
("Terracotta jewellery is made from:", ["Clay", "Plastic", "Glass", "Wood"], "Clay"),
("Which SDG supports skill education?", ["SDG 4", "SDG 1", "SDG 13", "SDG 16"], "SDG 4"),
("Terracotta jewellery is:", ["Eco-friendly", "Harmful", "Chemical based", "Plastic based"], "Eco-friendly"),
("This skill helps in:", ["Self-employment", "Gambling", "Gaming", "Watching TV"], "Self-employment"),
("Clay must be:", ["Baked", "Frozen", "Washed", "Painted"], "Baked"),
("Terracotta supports:", ["Sustainable living", "Pollution", "Wastage", "None"], "Sustainable living"),
("Terracotta jewellery is mostly:", ["Handmade", "Machine only", "Imported", "Illegal"], "Handmade"),
("Terracotta art comes from:", ["Traditional crafts", "Modern physics", "Coding", "Banking"], "Traditional crafts"),
("This skill improves:", ["Creativity", "Laziness", "Fear", "Anger"], "Creativity"),
("This skill can earn:", ["Income", "Punishment", "Loss", "Trouble"], "Income"),
],

"Beaded Jewellery": [
("Beaded jewellery is made using:", ["Beads", "Clay", "Soap", "Wax"], "Beads"),
("Beads can be made of:", ["Glass", "Plastic", "Wood", "All of these"], "All of these"),
("Beaded jewellery is used for:", ["Decoration", "Cooking", "Driving", "Farming"], "Decoration"),
("This skill supports:", ["Entrepreneurship", "Unemployment", "Crime", "Waste"], "Entrepreneurship"),
("Beaded jewellery improves:", ["Fine motor skills", "Weakness", "Stress", "Fear"], "Fine motor skills"),
("Making beads requires:", ["Patience", "Anger", "Speed", "Fear"], "Patience"),
("Beaded jewellery is:", ["Lightweight", "Extremely heavy", "Liquid", "Edible"], "Lightweight"),
("This is a type of:", ["Handicraft", "Software", "Medicine", "Tool"], "Handicraft"),
("Beaded jewellery can be sold:", ["Online & offline", "Only offline", "Only online", "Cannot be sold"], "Online & offline"),
("This skill is useful for:", ["Self business", "Time waste", "Games only", "TV only"], "Self business"),
],

"Thread Jewellery": [
("Thread jewellery uses:", ["Threads", "Clay", "Wax", "Soap"], "Threads"),
("Thread jewellery is:", ["Lightweight", "Very heavy", "Liquid", "Metal"], "Lightweight"),
("Thread jewellery supports:", ["Home business", "Crime", "Waste", "Pollution"], "Home business"),
("Thread art requires:", ["Creativity", "Fighting", "Running", "Shouting"], "Creativity"),
("Thread jewellery is mostly:", ["Handmade", "Factory only", "Imported only", "Illegal"], "Handmade"),
("Thread jewellery is suitable for:", ["Low investment business", "High risk gambling", "Crime", "Loss"], "Low investment business"),
("Thread jewellery supports:", ["Skill development", "No learning", "Failure", "Fear"], "Skill development"),
("Thread jewellery is:", ["Eco-friendly", "Dangerous", "Toxic", "Waste"], "Eco-friendly"),
("Thread jewellery can be:", ["Customized", "Fixed only", "Broken", "Destroyed"], "Customized"),
("This skill gives:", ["Income opportunity", "Loss only", "Punishment", "Risk only"], "Income opportunity"),
],

"Scented Candle": [
("Scented candles are made from:", ["Wax", "Clay", "Thread", "Soap"], "Wax"),
("Scented candles are used for:", ["Aroma therapy", "Eating", "Farming", "Driving"], "Aroma therapy"),
("Candle making supports:", ["Small business", "Crime", "Waste", "Fear"], "Small business"),
("Wax is melted using:", ["Heat", "Cold", "Water only", "Air"], "Heat"),
("Fragrance is added to:", ["Wax", "Thread", "Plastic", "Clay"], "Wax"),
("Candle making requires:", ["Safety", "Risk", "Carelessness", "Fear"], "Safety"),
("Candle making is a:", ["Vocational skill", "Sport", "Game", "Dance"], "Vocational skill"),
("Scented candles are sold in:", ["Shops", "Hospitals only", "Schools only", "Banks only"], "Shops"),
("Candle business requires:", ["Low investment", "Huge land", "No work", "No skill"], "Low investment"),
("Candle making supports:", ["Entrepreneurship", "Unemployment", "Loss", "Waste"], "Entrepreneurship"),
],

"Organic Soap": [
("Organic soap is made from:", ["Natural ingredients", "Plastic", "Metal", "Paint"], "Natural ingredients"),
("Organic soap is good for:", ["Skin", "Iron", "Wood", "Plastic"], "Skin"),
("Soap making teaches:", ["Chemistry & business", "Only gaming", "Dance", "Sports"], "Chemistry & business"),
("Soap making supports:", ["Home industry", "Crime", "Waste", "Pollution"], "Home industry"),
("Soap is made using:", ["Oils & lye", "Only water", "Only sugar", "Only wax"], "Oils & lye"),
("Organic soap is:", ["Chemical free", "Highly toxic", "Plastic", "Metal"], "Chemical free"),
("Soap making requires:", ["Safety measures", "Blind work", "Carelessness", "Fear"], "Safety measures"),
("Soap making can be:", ["Business", "Time waste", "Game", "Punishment"], "Business"),
("Soap is used for:", ["Hygiene", "Eating", "Painting", "Driving"], "Hygiene"),
("Soap making supports:", ["Self-employment", "Unemployment", "Loss", "Waste"], "Self-employment"),
],
}

def safe_stream(s):
    for key in stream_data:
        if key.lower() == s.lower():
            return key
    return None

# ---------------- UI ----------------
st.title("AI Vocational Tutor")

# ---------------- REGISTRATION ----------------
if not st.session_state.login:
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    stream = st.selectbox("Select Vocational Stream", list(stream_data.keys()))

    if st.button("Register"):
        if username and password:
            st.session_state.user = {"username": username, "stream": stream}
            st.session_state.login = True
            st.rerun()
        else:
            st.warning("Fill all fields")

# ---------------- SDG QUIZ GATE ----------------
elif not st.session_state.quiz_done:
    st.subheader("SDG Quiz (5 Questions)")

    user_answers = []
    for i, (q, opt, _) in enumerate(sdg_questions):
        ans = st.radio(f"{i+1}. {q}", opt, key=f"sdg_{i}", index=None)
        user_answers.append(ans)

    if st.button("Submit SDG Quiz"):
        if any(a is None for a in user_answers):
            st.warning("Answer all SDG questions.")
        else:
            score = 0
            for i, ans in enumerate(user_answers):
                if ans == sdg_questions[i][2]:
                    score += 2

            st.session_state.quiz_score = score
            st.session_state.quiz_done = True
            st.success(f"SDG Quiz Passed! Score: {score}/10")
            st.rerun()

# ---------------- DASHBOARD ----------------
else:
    user = st.session_state.user
    stream_name = safe_stream(user["stream"])

    st.success(f"Welcome {user['username']} | SDG Score: {st.session_state.quiz_score}/10")
    st.subheader("Lessons")

    lessons = stream_data[stream_name]

    for lesson in lessons:
        st.write(f"## {lesson}")

        pdf_path = pdf_map[stream_name][lesson]
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name=os.path.basename(pdf_path))

        st.components.v1.iframe(shorts_map[stream_name][lesson], height=360)

        st.write("### 📘 Lesson Quiz (10 Questions)")
        quiz_key = f"{lesson}_quiz"

        if quiz_key in st.session_state.lesson_quiz_scores:
            st.success(f"Already attempted. Score: {st.session_state.lesson_quiz_scores[quiz_key]} / 10")
        else:
            score = 0
            answers = []

            for i, (q, opts, correct) in enumerate(lesson_question_bank[lesson]):
                user_ans = st.radio(f"{i+1}. {q}", opts, key=f"{lesson}_{i}", index=None)
                answers.append((user_ans, correct))

            if st.button(f"Submit {lesson} Quiz", key=f"btn_{lesson}"):
                if any(a[0] is None for a in answers):
                    st.warning("Answer all questions")
                else:
                    for ua, ca in answers:
                        if ua == ca:
                            score += 1

                    st.session_state.lesson_quiz_scores[quiz_key] = score
                    st.success(f"You scored {score}/10")
                    st.rerun()

        st.divider()

    if st.session_state.lesson_quiz_scores:
        total = sum(st.session_state.lesson_quiz_scores.values())
        st.subheader("📊 Total Lesson Score")
        st.info(f"Total Score: {total} / 50")
