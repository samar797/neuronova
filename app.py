import streamlit as st
import os

st.set_page_config(
    page_title="AI Vocational Tutor",
    page_icon="🎓",
    layout="centered"
)

if "login" not in st.session_state:
    st.session_state.login = False

if "users" not in st.session_state:
    st.session_state.users = []

if "user" not in st.session_state:
    st.session_state.user = None

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

def safe_get_stream_for_user(user_obj):
    """Return stream name if present and valid, else None."""
    if not user_obj:
        return None
    s = user_obj.get("stream")
    if s in stream_data:
        return s
    for key in stream_data.keys():
        if key.strip().lower() == str(s).strip().lower():
            return key
    return None

st.title("AI Vocational Tutor")
st.caption("Smart Learning for Vocational Students")

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

else:
    user = st.session_state.user

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

        st.subheader("Lessons")

        user_stream = safe_get_stream_for_user(user)
        if not user_stream:
            st.error("Your selected stream is not recognised. Please re-register selecting a valid stream.")
            st.write("Available streams:", list(stream_data.keys()))
        else:
            stream_pdf_dict = pdf_map.get(user_stream, {})
            lessons = stream_data.get(user_stream, [])
            if not lessons:
                st.info("No lessons configured for your stream yet.")
            else:
                for lesson in lessons:
                    if st.button(lesson):
                        pdf_path = stream_pdf_dict.get(lesson)
                        if not pdf_path:
                            st.error("No PDF linked for this lesson yet. (Mapping missing)")
                            st.write("Mapped lessons for this stream:", list(stream_pdf_dict.keys()))
                            continue

                        st.write("Looking for PDF at:", pdf_path)
                        st.write("File exists?", os.path.exists(pdf_path))

                        if os.path.exists(pdf_path):
                            st.success(f"PDF Ready: {lesson}")
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    label=" Download Lesson PDF",
                                    data=f,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf"
                                )
                        else:
                            st.error("PDF file not found. Please upload it on GitHub to the correct path.")
                            st.write("Expected path:", pdf_path)

       
