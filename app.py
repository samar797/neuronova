import streamlit as st

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
    "IT": ["Python Basics", "Web Development", "Databases", "Cyber Security"],
    "Healthcare": ["First Aid", "Anatomy", "Patient Care"],
    "Automotive": ["Engine Basics", "Vehicle Repair"],
    "Culinary": ["Food Safety", "Cooking Skills"],
}

# ---------------- UI ----------------
st.title("🎓 AI Vocational Tutor")
st.caption("Smart Learning for Vocational Students")

if not st.session_state.login:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            for u in st.session_state.users:
                if u["username"] == username and u["password"] == password:
                    st.session_state.login = True
                    st.session_state.user = u
                    st.rerun()
            st.error("Invalid Login")

    with tab2:
        st.subheader("Create Account")

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")
        language = st.selectbox("Preferred Language", ["English"])
        stream = st.selectbox("Vocational Stream", list(stream_data.keys()))

        if st.button("Register"):
            st.session_state.users.append({
                "username": new_user,
                "password": new_pass,
                "language": language,
                "stream": stream,
            })
            st.success("Account created successfully!")

else:
    user = st.session_state.user

    st.success(f"Welcome {user['username']}")
    st.info(f"Stream: {user['stream']} | Level: {user['level']} | Language: {user['language']}")

    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

    st.divider()

    st.subheader("📚 Lessons")
    for lesson in stream_data[user["stream"]]:
        st.button(lesson)

    st.divider()

    st.subheader("🤖 Ask AI Tutor")
    question = st.text_area("Ask your question")

    if st.button("Get Answer"):
        if question:
            st.write("**AI Response (Demo):**")
            st.info(
                f"This is a demo AI answer for {user['stream']} student at {user['level']} level."
            )
        else:
            st.warning("Please enter a question.")
