"""
Main application entry point for the AI Chat Assistant.

This module handles the Streamlit user interface, session state,
chat history, sidebar controls, conversation export, and
interaction with the Groq service.
"""

import json

import streamlit as st

from config import (
    AI_PERSONALITIES,
    AVAILABLE_MODELS,
    TEMPERATURE
)

from services.groq_service import GroqService
from utils.logger import logger
from utils.pdf_generator import PDFGenerator


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# INITIALIZE SERVICES
# =====================================================

groq_service = GroqService()
pdf_generator = PDFGenerator()


# =====================================================
# LOAD CSS
# =====================================================

def load_css():
    """Load the application's custom CSS file."""

    with open(
        "styles/style.css",
        "r",
        encoding="utf-8"
    ) as css_file:

        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )


# =====================================================
# SESSION STATE
# =====================================================

def initialize_session_state():
    """Initialize application session state."""

    if "messages" not in st.session_state:
        st.session_state.messages = []


# =====================================================
# TEXT EXPORT
# =====================================================

def create_text_export():
    """Create a readable text representation of the conversation."""

    lines = []

    for message in st.session_state.messages:

        role = message["role"].upper()
        content = message["content"]

        lines.append(
            f"{role}:\n{content}\n"
        )

    return "\n".join(lines)


# =====================================================
# JSON EXPORT
# =====================================================

def create_json_export():
    """Create a JSON representation of the conversation."""

    return json.dumps(
        st.session_state.messages,
        indent=4,
        ensure_ascii=False
    )


# =====================================================
# PDF EXPORT
# =====================================================

def create_pdf_export():
    """Generate a PDF from the current conversation."""

    return pdf_generator.generate_conversation_pdf(
        st.session_state.messages
    )


# =====================================================
# SIDEBAR CONTROLS
# =====================================================

def render_sidebar_controls():
    """
    Render sidebar settings and return selected values.

    Returns:
        tuple: Personality, model, and temperature.
    """

    with st.sidebar:

        st.title("🤖 AI Chat Assistant")

        st.caption("Powered by Groq")

        st.divider()

        # -------------------------------------------------
        # AI PERSONALITY
        # -------------------------------------------------

        selected_personality = st.selectbox(
            "🧠 AI Personality",
            options=list(AI_PERSONALITIES.keys())
        )

        # -------------------------------------------------
        # MODEL
        # -------------------------------------------------

        selected_model = st.selectbox(
            "⚙️ Model",
            options=AVAILABLE_MODELS
        )

        # -------------------------------------------------
        # TEMPERATURE
        # -------------------------------------------------

        selected_temperature = st.slider(
            "🌡️ Temperature",
            min_value=0.0,
            max_value=1.0,
            value=TEMPERATURE,
            step=0.1
        )

        st.divider()

    return (
        selected_personality,
        selected_model,
        selected_temperature
    )


# =====================================================
# EXPORT SECTION
# =====================================================

def render_export_section():
    """Render conversation export controls."""

    with st.sidebar:

        st.subheader("💾 Export Conversation")

        st.download_button(
            label="📄 Download TXT",
            data=create_text_export(),
            file_name="chat_conversation.txt",
            mime="text/plain",
            use_container_width=True,
            on_click="ignore"
        )

        st.download_button(
            label="📦 Download JSON",
            data=create_json_export(),
            file_name="chat_conversation.json",
            mime="application/json",
            use_container_width=True
        )

        st.download_button(
            label="📑 Download PDF",
            data=create_pdf_export(),
            file_name="chat_conversation.pdf",
            mime="application/pdf",
            use_container_width=True,
            on_click="ignore"
        )

        st.divider()

        # -------------------------------------------------
        # CLEAR CHAT
        # -------------------------------------------------

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.messages = []

            logger.info(
                "Chat history cleared."
            )

            st.rerun()


# =====================================================
# HERO
# =====================================================

def render_hero():
    """Render the application's hero section."""

    st.markdown(
        """
<div class="hero">
<div class="hero-title">🤖 AI Chat Assistant</div>
<div class="hero-subtitle">
Your intelligent AI companion powered by Groq.
</div>
</div>
""",
        unsafe_allow_html=True
    )


# =====================================================
# CHAT HISTORY
# =====================================================

def render_chat_history():
    """Display previous messages from the conversation."""

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


# =====================================================
# HANDLE CHAT
# =====================================================

def handle_chat(
    system_prompt,
    model,
    temperature
):
    """
    Handle user input and generate a streaming AI response.

    Args:
        system_prompt (str): Instructions defining AI behavior.
        model (str): Selected Groq model.
        temperature (float): Response variability.
    """

    prompt = st.chat_input(
        "Message AI Chat Assistant..."
    )

    if not prompt:
        return

    # =================================================
    # SAVE USER MESSAGE
    # =================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # =================================================
    # DISPLAY USER MESSAGE
    # =================================================

    with st.chat_message("user"):

        st.markdown(prompt)

    logger.info(
        "User message received."
    )

    # =================================================
    # GENERATE AI RESPONSE
    # =================================================

    try:

        response_stream = (
            groq_service.stream_response(
                messages=st.session_state.messages,
                system_prompt=system_prompt,
                model=model,
                temperature=temperature
            )
        )

        # =================================================
        # DISPLAY STREAMING RESPONSE
        # =================================================

        with st.chat_message("assistant"):

            response = st.write_stream(
                response_stream
            )

        # =================================================
        # SAVE AI RESPONSE
        # =================================================

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        logger.info(
            "AI response generated successfully."
        )

    except Exception as e:

        logger.error(
            f"Groq API request failed: {e}"
        )

        st.error(
            "❌ Sorry, something went wrong while "
            "generating the response."
        )


# =====================================================
# MAIN
# =====================================================

def main():
    """Run the AI Chat Assistant application."""

    load_css()

    initialize_session_state()

    # -------------------------------------------------
    # SIDEBAR SETTINGS FIRST
    # -------------------------------------------------

    (
        selected_personality,
        selected_model,
        selected_temperature
    ) = render_sidebar_controls()

    # -------------------------------------------------
    # MAIN UI
    # -------------------------------------------------

    render_hero()

    render_chat_history()

    # -------------------------------------------------
    # SYSTEM PROMPT
    # -------------------------------------------------

    system_prompt = AI_PERSONALITIES[
        selected_personality
    ]

    # -------------------------------------------------
    # HANDLE CHAT
    # -------------------------------------------------

    handle_chat(
        system_prompt=system_prompt,
        model=selected_model,
        temperature=selected_temperature
    )

    # -------------------------------------------------
    # EXPORT SECTION LAST
    # -------------------------------------------------

    render_export_section()


# =====================================================
# APPLICATION ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()