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

# Login/Signup system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.view = "login"  # "login" or "signup"

if not st.session_state.logged_in:
    st.title("AI Vocational Tutor")
    
    # Toggle between login and signup
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.view = "login"
            st.rerun()
    with col2:
        if st.button("Sign Up"):
            st.session_state.view = "signup"
            st.rerun()
    
    if st.session_state.view == "login":
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
    elif st.session_state.view == "signup":
        st.header("Sign Up")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.button("Sign Up"):
            if new_username in users:
                st.error("Username already exists.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif not new_username or not new_password:
                st.error("Please fill in all fields.")
            else:
                users[new_username] = new_password
                st.success("Account created successfully! Please log in.")
                st.session_state.view = "login"
                st.rerun()
else:
    st.title("AI Vocational Tutor")
    st.write(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.view = "login"
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



