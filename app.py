import streamlit as st
from dotenv import load_dotenv
import os
import time
from google import genai


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

# Try Streamlit Secrets first
api_key = st.secrets.get("GEMINI_API_KEY", None)

# If not found, try local .env
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "❌ GEMINI_API_KEY not found. "
        "Please add it to Streamlit Secrets or your .env file."
    )
    st.stop()


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Gemini AI Chatbox",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN APP
       ================================ */

    .stApp {
        background: linear-gradient(
            135deg,
            #eef2ff,
            #f8f9ff
        );
        color: #111827 !important;
    }

    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }


    /* ================================
       TITLE
       ================================ */

    h1 {
        text-align: center !important;
        color: #4f46e5 !important;
        font-size: 42px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
    }


    /* ================================
       NORMAL TEXT
       ================================ */

    .stApp p {
        color: #374151 !important;
        font-size: 17px;
    }


    /* ================================
       TEXT AREA LABEL
       ================================ */

    [data-testid="stTextArea"] label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }


    /* ================================
       TEXT AREA
       ================================ */

    textarea {
        background-color: #ffffff !important;
        color: #111827 !important;
        border-radius: 15px !important;
        border: 2px solid #c7d2fe !important;
        padding: 15px !important;
        font-size: 16px !important;
    }

    textarea::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }

    textarea:focus {
        border: 2px solid #6366f1 !important;
        box-shadow:
            0 0 10px rgba(99, 102, 241, 0.25) !important;
    }


    /* ================================
       BUTTON
       ================================ */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none !important;

        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #7c3aed
            ) !important;

        color: white !important;
        font-size: 17px !important;
        font-weight: 600 !important;

        padding: 12px !important;

        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 6px 18px
            rgba(79, 70, 229, 0.35);
    }


    /* ================================
       ALERTS
       ================================ */

    .stAlert {
        border-radius: 12px;
    }


    /* ================================
       RESPONSE CONTAINER
       ================================ */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 15px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# HEADER
# ==========================================

st.title("🤖 Gemini AI Chatbox")

st.write(
    "<p style='text-align:center;'>Ask Gemini anything!</p>",
    unsafe_allow_html=True
)


# ==========================================
# PROMPT INPUT
# ==========================================

prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Explain Artificial Intelligence in simple words...",
    height=120
)


# ==========================================
# GENERATE RESPONSE
# ==========================================

if st.button("✨ Generate Response"):

    if not prompt.strip():

        st.warning("⚠️ Please enter a prompt.")

    else:

        try:

            # ==================================
            # GEMINI REQUEST
            # ==================================

            with st.spinner("🤖 Gemini is thinking..."):

                response = None

                for attempt in range(3):

                    try:

                        response = client.models.generate_content(
                            model=MODEL_NAME,
                            contents=prompt
                        )

                        break

                    except Exception as api_error:

                        error_message = str(api_error)

                        # Temporary Gemini server/rate-limit errors
                        if (
                            "503" in error_message
                            or "UNAVAILABLE" in error_message
                            or "429" in error_message
                        ):

                            if attempt < 2:

                                wait_time = 2 ** attempt
                                time.sleep(wait_time)

                            else:

                                raise api_error

                        else:

                            raise api_error


            # ==================================
            # DISPLAY RESPONSE
            # ==================================

            if response and response.text:

                st.success("✅ Response generated!")

                # Proper Streamlit container
                with st.container(border=True):

                    st.markdown(
                        "### 🤖 Gemini Response"
                    )

                    # IMPORTANT:
                    # Display Gemini's response directly
                    # instead of putting it inside HTML.
                    st.markdown(response.text)


            else:

                st.warning(
                    "⚠️ Gemini returned an empty response."
                )


        # ======================================
        # ERROR HANDLING
        # ======================================

        except Exception as e:

            error_message = str(e)

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            ):

                st.error(
                    "❌ Gemini is temporarily experiencing "
                    "high demand. Please try again in a few seconds."
                )

            elif "429" in error_message:

                st.error(
                    "❌ Gemini rate limit reached. "
                    "Please wait a moment and try again."
                )

            elif "401" in error_message or "403" in error_message:

                st.error(
                    "❌ Gemini API authentication failed. "
                    "Please check your API key."
                )

            else:

                st.error(
                    f"❌ Something went wrong while contacting Gemini:\n\n"
                    f"{e}"
                )