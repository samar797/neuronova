import streamlit as st
import random

# Mock AI responses for tutoring (expand as needed)
responses = {
    "IT": [
        "In IT, programming languages like Python are essential. What specific topic would you like to learn?",
        "Networking involves protocols like TCP/IP. Can you tell me more about your question?",
        "Cybersecurity focuses on protecting systems. How can I assist you today?"
    ],
    "Mechanical Engineering": [
        "Thermodynamics is key in mechanical engineering. What aspect interests you?",
        "Fluid mechanics deals with liquids and gases. Ask me anything!",
        "Materials science helps in designing durable parts. How can I help?"
    ],
    "Nursing": [
        "Patient care involves empathy and skills. What do you want to know?",
        "Anatomy and physiology are foundational. Let's discuss!",
        "Ethics in nursing is crucial. How can I guide you?"
    ],
    "General": [
        "General knowledge covers a wide range of topics. What subject are you interested in?",
        "Study skills like time management are important. How can I help?",
        "Career advice can guide your vocational path. Ask away!"
    ]
}

# Simple user database (in a real app, use a secure database)
users = {
    "student1": "pass1",
    "student2": "pass2"
}

# Streamlit app
st.set_page_config(page_title="AI Vocational Tutor", page_icon="🎓")

# Login system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("AI Vocational Tutor")
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Welcome! Select a stream to start tutoring.")
            st.rerun()
        else:
            st.error("Invalid username or password.")
else:
    st.title("AI Vocational Tutor")
    st.write(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Stream selection (including General)
    if "stream" not in st.session_state:
        st.session_state.stream = None

    stream_options = ["Information Technology", "Mechanical Engineering", "Nursing", "General"]
    stream_map = {
        "Information Technology": "IT",
        "Mechanical Engineering": "Mechanical Engineering",
        "Nursing": "Nursing",
        "General": "General"
    }

    selected_stream_display = st.selectbox("Select Vocational Stream", stream_options)
    st.session_state.stream = stream_map[selected_stream_display]

    # Tutoring interface
    if st.session_state.stream:
        st.subheader(f"AI Response ({st.session_state.stream})")
        question = st.text_input("Ask a question:")
        if st.button("Submit"):
            if question:
                # Mock AI response (random from list)
                ai_response = random.choice(responses[st.session_state.stream])
                st.write(ai_response)
            else:
                st.write("Please enter a question.")
