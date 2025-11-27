import streamlit as st
import random

# Mock AI responses for tutoring (expand as needed)
responses = {
    "IT": {
        "en": [
            "In IT, programming languages like Python are essential. What specific topic would you like to learn?",
            "Networking involves protocols like TCP/IP. Can you tell me more about your question?",
            "Cybersecurity focuses on protecting systems. How can I assist you today?"
        ],
        "es": [
            "En TI, lenguajes de programación como Python son esenciales. ¿Qué tema específico te gustaría aprender?",
            "Las redes involucran protocolos como TCP/IP. ¿Puedes decirme más sobre tu pregunta?",
            "La ciberseguridad se centra en proteger sistemas. ¿Cómo puedo ayudarte hoy?"
        ]
    },
    "Mechanical Engineering": {
        "en": [
            "Thermodynamics is key in mechanical engineering. What aspect interests you?",
            "Fluid mechanics deals with liquids and gases. Ask me anything!",
            "Materials science helps in designing durable parts. How can I help?"
        ],
        "es": [
            "La termodinámica es clave en ingeniería mecánica. ¿Qué aspecto te interesa?",
            "La mecánica de fluidos trata de líquidos y gases. ¡Pregúntame cualquier cosa!",
            "La ciencia de materiales ayuda en el diseño de piezas duraderas. ¿Cómo puedo ayudar?"
        ]
    },
    "Nursing": {
        "en": [
            "Patient care involves empathy and skills. What do you want to know?",
            "Anatomy and physiology are foundational. Let's discuss!",
            "Ethics in nursing is crucial. How can I guide you?"
        ],
        "es": [
            "El cuidado del paciente implica empatía y habilidades. ¿Qué quieres saber?",
            "La anatomía y fisiología son fundamentales. ¡Hablemos!",
            "La ética en enfermería es crucial. ¿Cómo puedo guiarte?"
        ]
    }
}

# Simple user database (in a real app, use a secure database)
users = {
    "student1": "pass1",
    "student2": "pass2"
}

# Streamlit app
st.set_page_config(page_title="AI Vocational Tutor", page_icon="🎓")

# Language selection (persistent across sessions)
if "language" not in st.session_state:
    st.session_state.language = "en"

# Language toggle
col1, col2 = st.columns(2)
with col1:
    if st.button("English"):
        st.session_state.language = "en"
        st.rerun()
with col2:
    if st.button("Español"):
        st.session_state.language = "es"
        st.rerun()

lang = st.session_state.language

# Translations
texts = {
    "en": {
        "title": "AI Vocational Tutor",
        "login": "Login",
        "signup": "Sign Up",
        "username": "Username",
        "password": "Password",
        "new_username": "New Username",
        "new_password": "New Password",
        "confirm_password": "Confirm Password",
        "login_button": "Login",
        "signup_button": "Sign Up",
        "logout": "Logout",
        "select_stream": "Select Vocational Stream",
        "it": "Information Technology",
        "mech": "Mechanical Engineering",
        "nursing": "Nursing",
        "ask_question": "Ask a question:",
        "submit": "Submit",
        "response": "AI Response:",
        "invalid": "Invalid username or password.",
        "username_exists": "Username already exists.",
        "password_mismatch": "Passwords do not match.",
        "fill_fields": "Please fill in all fields.",
        "account_created": "Account created successfully! Please log in.",
        "welcome": "Welcome! Select a stream to start tutoring.",
        "enter_question": "Please enter a question."
    },
    "es": {
        "title": "Tutor Vocacional de IA",
        "login": "Iniciar Sesión",
        "signup": "Registrarse",
        "username": "Nombre de Usuario",
        "password": "Contraseña",
        "new_username": "Nuevo Nombre de Usuario",
        "new_password": "Nueva Contraseña",
        "confirm_password": "Confirmar Contraseña",
        "login_button": "Iniciar Sesión",
        "signup_button": "Registrarse",
        "logout": "Cerrar Sesión",
        "select_stream": "Seleccionar Flujo Vocacional",
        "it": "Tecnología de la Información",
        "mech": "Ingeniería Mecánica",
        "nursing": "Enfermería",
        "ask_question": "Haz una pregunta:",
        "submit": "Enviar",
        "response": "Respuesta de IA:",
        "invalid": "Nombre de usuario o contraseña inválidos.",
        "username_exists": "El nombre de usuario ya existe.",
        "password_mismatch": "Las contraseñas no coinciden.",
        "fill_fields": "Por favor, completa todos los campos.",
        "account_created": "¡Cuenta creada exitosamente! Por favor, inicia sesión.",
        "welcome": "¡Bienvenido! Selecciona un flujo para comenzar la tutoría.",
        "enter_question": "Por favor, ingresa una pregunta."
    }
}

# Login/Signup system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.view = "login"  # "login" or "signup"

if not st.session_state.logged_in:
    st.title(texts[lang]["title"])
    
    # Toggle between login and signup
    col1, col2 = st.columns(2)
    with col1:
        if st.button(texts[lang]["login"]):
            st.session_state.view = "login"
            st.rerun()
    with col2:
        if st.button(texts[lang]["signup"]):
            st.session_state.view = "signup"
            st.rerun()
    
    if st.session_state.view == "login":
        st.header(texts[lang]["login"])
        username = st.text_input(texts[lang]["username"])
        password = st.text_input(texts[lang]["password"], type="password")
        if st.button(texts[lang]["login_button"]):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(texts[lang]["welcome"])
                st.rerun()
            else:
                st.error(texts[lang]["invalid"])
    elif st.session_state.view == "signup":
        st.header(texts[lang]["signup"])
        new_username = st.text_input(texts[lang]["new_username"])
        new_password = st.text_input(texts[lang]["new_password"], type="password")
        confirm_password = st.text_input(texts[lang]["confirm_password"], type="password")
        if st.button(texts[lang]["signup_button"]):
            if new_username in users:
                st.error(texts[lang]["username_exists"])
            elif new_password != confirm_password:
                st.error(texts[lang]["password_mismatch"])
            elif not new_username or not new_password:
                st.error(texts[lang]["fill_fields"])
            else:
                users[new_username] = new_password
                st.success(texts[lang]["account_created"])
                st.session_state.view = "login"
                st.rerun()
else:
    st.title(texts[lang]["title"])
    st.write(f"{texts[lang]['welcome']} {st.session_state.username}")
    if st.button(texts[lang]["logout"]):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.view = "login"
        st.rerun()

    # Stream selection
    if "stream" not in st.session_state:
        st.session_state.stream = None

    stream_options = {
        "en": [texts["en"]["it"], texts["en"]["mech"], texts["en"]["nursing"]],
        "es": [texts["es"]["it"], texts["es"]["mech"], texts["es"]["nursing"]]
    }
    stream_map = {
        texts["en"]["it"]: "IT",
        texts["es"]["it"]: "IT",
        texts["en"]["mech"]: "Mechanical Engineering",
        texts["es"]["mech"]: "Mechanical Engineering",
        texts["en"]["nursing"]: "Nursing",
        texts["es"]["nursing"]: "Nursing"
    }

    selected_stream_display = st.selectbox(texts[lang]["select_stream"], stream_options[lang])
    st.session_state.stream = stream_map[selected_stream_display]

    # Tutoring interface
    if st.session_state.stream:
        st.subheader(f"{texts[lang]['response']} ({st.session_state.stream})")
        question = st.text_input(texts[lang]["ask_question"])
        if st.button(texts[lang]["submit"]):
            if question:
                # Mock AI response (random from list)
                ai_response = random.choice(responses[st.session_state.stream][lang])
                st.write(ai_response)
            else:
                st.write(texts[lang]["enter_question"])



