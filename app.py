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

# ---------------- SAMPLE CONTENT WITH SDG INTEGRATION ----------------
# Added SDG mappings: Each lesson now links to relevant SDGs (e.g., Goal 4 for education, Goal 8 for economic growth).
# SDGs are simplified as a list of goal numbers/descriptions for display.
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

# SDG mappings per lesson (expand as needed; based on UN SDGs)
lesson_sdgs = {
    "terracotta jewellery": ["Goal 4: Quality Education", "Goal 8: Decent Work and Economic Growth", "Goal 12: Responsible Consumption"],
    "beaded jewellery": ["Goal 4: Quality Education", "Goal 5: Gender Equality", "Goal 12: Responsible Consumption"],
    "thread jewellery": ["Goal 4: Quality Education", "Goal 8: Decent Work and Economic Growth"],
    "scented candle": ["Goal 4: Quality Education", "Goal 8: Decent Work and Economic Growth", "Goal 12: Responsible Consumption"],
    "organic soap": ["Goal 4: Quality Education", "Goal 3: Good Health and Well-being", "Goal 12: Responsible Consumption"],
}

# ---------------- PDF BACKEND MAPPING (UNCHANGED) ----------------
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

# ---------------- SDG PROGRESS TRACKER (NEW) ----------------
# Simple session-based tracker for SDG points (e.g., 1 point per lesson completed).
if "sdg_progress" not in st.session_state:
    st.session_state.sdg_progress = {}  # e.g., {"Goal 4": 2, "Goal 8": 1}

# ---------------- helper ----------------
def safe_get_stream_for_user(user_obj):
    """Return stream name if present and valid, else None."""
    if not user_obj:
        return None
    s = user_obj.get("stream")
    # direct check
    if s in stream_data:
        return s
    # try case-insensitive match
    for key in stream_data.keys():
        if key.strip().lower() == str(s).strip().lower():
            return key
    return None

# ---------------- UI ----------------
st.title("🎓 AI Vocational Tutor")
st.caption("Smart Learning for Vocational Students with SDG Focus")

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

    # Safety: if session user missing, reset login
    if not user:
        st.error("Session user missing — please register again.")
        if st.button("Restart"):
            st.session_state.login = False
            st.rerun()
    else:
        st.success(f"Welcome {user.get('username')}")
        st.info(f"Stream: {user.get('stream')}")

        if st.button("Logout"):
            st.session_state.login = False
            st.session_state.user = None
            st.rerun()

        st.divider()

        # ---------------- SDG PROGRESS DASHBOARD (NEW) ----------------
        st.subheader("🌍 SDG Progress Tracker")
        if st.session_state.sdg_progress:
            st.write("Your contributions to SDGs:")
            for sdg, points in st.session_state.sdg_progress.items():
                st.progress(min(points / 10, 1.0), text=f"{sdg}: {points} points")  # Cap at 10 for demo
        else:
            st.info("Complete lessons to earn SDG points and track your impact!")

        st.divider()

        # ---------------- LESSONS WITH PDF BACKEND AND SDG INTEGRATION ----------------
        st.subheader("📚 Lessons")

        # Determine user's stream name safely (handles minor case differences)
        user_stream = safe_get_stream_for_user(user)
        if not user_stream:
            st.error("Your selected stream is not recognised. Please re-register selecting a valid stream.")
            st.write("Available streams:", list(stream_data.keys()))
        else:
            # Try to get the pdf mapping for this stream safely
            stream_pdf_dict = pdf_map.get(user_stream, {})

            # Show lessons (if stream exists in stream_data)
            lessons = stream_data.get(user_stream, [])
            if not lessons:
                st.info("No lessons configured for your stream yet.")
            else:
                for lesson in lessons:
                    # NEW: Display SDG badges for each lesson
                    sdgs = lesson_sdgs.get(lesson, [])
                    sdg_text = " | ".join(sdgs) if sdgs else "No SDGs linked yet"
                    st.write(f"**{lesson}** - SDG Links: {sdg_text}")

                    if st.button(f"Start {lesson}"):
                        # safe check if pdf_map has this lesson
                        pdf_path = stream_pdf_dict.get(lesson)
                        if not pdf_path:
                            st.error("❌ No PDF linked for this lesson yet. (Mapping missing)")
                            st.write("Mapped lessons for this stream:", list(stream_pdf_dict.keys()))
                            continue

                        # debug lines (helpful if file missing) - you can remove later
                        st.write("Looking for PDF at:", pdf_path)
                        st.write("File exists?", os.path.exists(pdf_path))

                        if os.path.exists(pdf_path):
                            st.success(f"PDF Ready: {lesson}")
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    label="📥 Download Lesson PDF",
                                    data=f,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf"
                                )
                            # NEW: Award SDG points upon "starting" lesson (simulate completion)
                            for sdg in sdgs:
                                if sdg not in st.session_state.sdg_progress:
                                    st.session_state.sdg_progress[sdg] = 0
                                st.session_state.sdg_progress[sdg] += 1
                            st.info("SDG points awarded! Check your tracker above.")
                        else:
                            st.error("❌ PDF file not found. Please upload it on GitHub to the correct path.")
                            st.write("Expected path:", pdf_path)

        st.divider()

        # ---------------- AI TUTOR WITH SDG ENHANCEMENT ----------------
        st.subheader("🤖 Ask AI Tutor")
        question = st.text_area("Ask your question (include SDG-related queries for better insights)")

        if st.button("Get Answer"):
            if question:
                st.write("**AI Response (Demo):**")
                # NEW: Basic SDG integration in response (expand with real AI like GPT for production)
                response = f"This is a demo AI answer for {user.get('stream')} student."
                if "sdg" in question.lower() or "sustainable" in question.lower():
                    response += " Relating to SDGs: This topic supports Goal 4 (Quality Education) and Goal 8 (Decent Work). For more, explore our lessons!"
                st.info(response)
            else:
                st.warning("Please enter a question.")
