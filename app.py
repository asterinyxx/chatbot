import streamlit as st
from dotenv import load_dotenv
import os
from google import genai


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


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

st.markdown("""
<style>

    /* =================================
       MAIN APP
    ================================= */

    .stApp {
        background: linear-gradient(135deg, #eef2ff, #f8f9ff);
        color: #111827 !important;
    }

    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }


    /* =================================
       TITLE
    ================================= */

    h1 {
        text-align: center !important;
        color: #4f46e5 !important;
        font-size: 42px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
    }


    /* =================================
       NORMAL TEXT
    ================================= */

    .stApp p {
        color: #374151 !important;
        font-size: 17px;
    }

    .stMarkdown {
        color: #374151 !important;
    }


    /* =================================
       TEXT AREA LABEL
    ================================= */

    [data-testid="stTextArea"] label {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }


    /* =================================
       TEXT AREA
    ================================= */

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
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.25) !important;
    }


    /* =================================
       BUTTON
    ================================= */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none !important;
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        font-size: 17px !important;
        font-weight: 600 !important;
        padding: 12px !important;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35);
    }


    /* =================================
       ALERTS
    ================================= */

    .stAlert {
        border-radius: 12px;
    }


    /* =================================
       RESPONSE TEXT
    ================================= */

    [data-testid="stMarkdownContainer"] {
        line-height: 1.7;
        color: #111827 !important;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# UI
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

    if prompt.strip():

        try:

            with st.spinner("Gemini is thinking..."):

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

            st.success("Response generated!")


            # ==================================
            # RESPONSE CARD
            # ==================================

            st.markdown(
                f"""
                <div style="
                    background: white;
                    padding: 25px;
                    border-radius: 15px;
                    margin-top: 15px;
                    border: 1px solid #e0e7ff;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                    color: #111827;
                ">

                    <h3 style="
                        color: #4f46e5;
                        margin-top: 0;
                        margin-bottom: 15px;
                    ">
                        🤖 Gemini Response
                    </h3>

                    <div style="
                        color: #374151;
                        font-size: 16px;
                        line-height: 1.7;
                    ">
                        {response.text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        except Exception as e:

            st.error(
                f"❌ Something went wrong while contacting Gemini:\n\n{e}"
            )


    else:

        st.warning("⚠️ Please enter a prompt.")