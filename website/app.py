"""
DeepSync - Enterprise AI Solutions Website
A professional Streamlit website showcasing AI services and the DeepSync Desktop App.
"""

import streamlit as st
import zipfile
import io
import os
from pathlib import Path

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="BATCH SEVEN AI & DATA SCIENCE | Enterprise AI Solutions",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional, company-style design
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --accent: #22d3ee;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --text: #f8fafc;
        --text-muted: #94a3b8;
    }
    
    /* Main container */
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(34, 211, 238, 0.08) 100%);
        border-radius: 24px;
        padding: 4rem 3rem;
        margin: 2rem 0;
        border: 1px solid rgba(99, 102, 241, 0.2);
        text-align: center;
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #fff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .hero p {
        font-size: 1.25rem;
        color: #94a3b8;
        max-width: 600px;
        margin: 0 auto 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
    }
    
    .feature-card h3 {
        color: #f8fafc;
        font-size: 1.25rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: #94a3b8;
        font-size: 0.95rem;
    }
    
    /* Product showcase */
    .product-showcase {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(34, 211, 238, 0.1) 100%);
        border-radius: 20px;
        padding: 3rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
        margin: 2rem 0;
    }
    
    /* Stats */
    .stat-box {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #6366f1;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    /* CTA button */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.5rem;
    }
    
    .section-subheader {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def create_app_zip():
    """Create a zip file of the Local Agent app for download."""
    base_path = Path(__file__).parent.parent
    files_to_include = [
        "agent.py", "gui_app.py", "voice_module.py",
        "requirements.txt", "run.bat", "run_gui.bat",
        "README.md", "SETUP.md"
    ]
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_name in files_to_include:
            file_path = base_path / file_name
            if file_path.exists():
                zf.write(file_path, f"deepsync/{file_name}")
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## BATCH SEVEN AI & DATA SCIENCE")
        st.markdown("---")
        page = st.radio(
            "Navigate",
            ["Home", "Local Agent", "Products", "Contact", "FAQ"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.markdown("""
        <div style="color: #64748b; font-size: 0.85rem;">
        © 2025 BATCH SEVEN AI & DATA SCIENCE<br>
        Enterprise AI Solutions
        </div>
        """, unsafe_allow_html=True)

    # Home page
    if page == "Home":
        # Hero section
        st.markdown('<div class="hero"><h1>BATCH SEVEN AI & DATA SCIENCE</h1><p>Enterprise-grade AI solutions that empower businesses. From cloud APIs to fully local agents—deploy intelligence where you need it.</p></div>', unsafe_allow_html=True)
        
        # Stats row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="stat-box"><div class="stat-number">100%</div><div class="stat-label">Local & Private</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="stat-box"><div class="stat-number">0</div><div class="stat-label">API Keys Needed</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="stat-box"><div class="stat-number">24/7</div><div class="stat-label">Offline Ready</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="stat-box"><div class="stat-number">∞</div><div class="stat-label">No Usage Limits</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Featured product - DeepSync
        st.markdown('<p class="section-header">Featured: DeepSync Desktop App</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subheader">Your personal AI assistant that runs entirely on your machine. No cloud. No subscriptions. No limits.</p>', unsafe_allow_html=True)
        
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown("""
            <div class="product-showcase">
                <h3 style="color: #22d3ee; font-size: 1.5rem;">DeepSync</h3>
                <p style="color: #94a3b8; margin: 1rem 0;">
                A lightweight desktop application that brings AI capabilities to your computer—completely offline. 
                Run commands, manage notes, search files, and control your system with natural language and voice.
                </p>
                <ul style="color: #cbd5e1; margin: 1rem 0;">
                    <li>Voice Recognition & Text-to-Speech</li>
                    <li>Modern Dark-Themed GUI</li>
                    <li>100% Private - No Data Leaves Your Machine</li>
                    <li>Low Resource Usage - No GPU Required</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col_right:
            st.markdown("### Download")
            zip_data = create_app_zip()
            st.download_button(
                label="Download Desktop App",
                data=zip_data,
                file_name="deepsync.zip",
                mime="application/zip",
                use_container_width=True
            )
            st.caption("Includes: agent, GUI, voice module, setup guide")
        
        # Services grid
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<p class="section-header">Our AI Services</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subheader">Comprehensive AI solutions for every business need</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>Local & Private AI</h3>
                <p>Deploy AI that runs entirely on your infrastructure. Zero data leakage, full compliance.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>Cloud AI APIs</h3>
                <p>Scalable, managed AI endpoints for high-throughput applications and integrations.</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>Custom Solutions</h3>
                <p>Tailored AI systems built for your workflows, from automation to intelligent assistants.</p>
            </div>
            """, unsafe_allow_html=True)

    # DeepSync dedicated page
    elif page == "Local Agent":
        st.markdown("# DeepSync Desktop App")
        st.markdown("Your personal AI assistant—runs entirely on your machine. No cloud. No API keys. No limits.")
        st.markdown("---")
        
        col_info, col_download = st.columns([2, 1])
        with col_info:
            st.markdown("### Features")
            st.markdown("""
            | Feature | Description |
            |---------|-------------|
            | **100% Local** | No internet or external APIs required |
            | **Voice Recognition** | Speak your commands (optional) |
            | **Text-to-Speech** | Hear responses aloud |
            | **Modern GUI** | Beautiful dark-themed interface |
            | **Low Resource** | No GPU, works on low-spec machines |
            | **Notes & Commands** | Run commands, manage notes, search files |
            """)
            
            st.markdown("### Quick Start")
            st.code("""
# 1. Extract the downloaded zip
# 2. Install dependencies (optional, for voice)
pip install -r requirements.txt

# 3. Run the app
python gui_app.py

# Or double-click run_gui.bat on Windows
            """, language="bash")
            
            st.markdown("### What You Can Do")
            st.markdown("""
            - **Time/Date** — "What time is it?" / "What's the date?"
            - **Run commands** — "Run notepad" / "Execute dir"
            - **List files** — "List files" / "Ls C:\\Users"
            - **Search files** — "Search hello in readme.txt"
            - **Read files** — "Read readme.txt"
            - **Notes** — "Remember buy milk" / "Show my notes"
            - **Help** — "Help" / "Exit"
            """)
        
        with col_download:
            st.markdown("### Download")
            zip_data = create_app_zip()
            st.download_button(
                label="Download Now",
                data=zip_data,
                file_name="deepsync.zip",
                mime="application/zip",
                use_container_width=True
            )
            st.markdown("**Requirements:** Python 3.7+")
            st.markdown("**Platform:** Windows, macOS, Linux")
            st.markdown("**Size:** ~50 KB (source)")

    # Products page
    elif page == "Products":
        st.markdown("# Our Products")
        st.markdown("AI solutions for every scale and use case")
        st.markdown("---")
        
        st.markdown("### DeepSync (Desktop)")
        st.markdown("""
        A lightweight desktop application for personal productivity. Run commands, manage notes, 
        search files, and control your system with natural language—all offline.
        """)
        zip_data = create_app_zip()
        st.download_button("Download DeepSync", data=zip_data, file_name="deepsync.zip", mime="application/zip")
        
        st.markdown("---")
        st.markdown("### Enterprise AI Platform (Coming Soon)")
        st.markdown("""
        Deploy custom AI models on your infrastructure. Full control, enterprise support, 
        and compliance-ready architecture.
        """)
        st.button("Notify Me", disabled=True)
        
        st.markdown("---")
        st.markdown("### AI API Gateway (Coming Soon)")
        st.markdown("""
        Unified API for multiple AI providers. Rate limiting, caching, and seamless 
        fallback across models.
        """)
        st.button("Notify Me", disabled=True, key="notify2")

    # Contact page
    elif page == "Contact":
        st.markdown("# Contact Us")
        st.markdown("Get in touch with our team")
        st.markdown("---")
        
        with st.form("contact_form"):
            name = st.text_input("Name *")
            email = st.text_input("Email *")
            company = st.text_input("Company")
            subject = st.selectbox("Subject", ["General Inquiry", "Sales", "Support", "Partnership"])
            message = st.text_area("Message *")
            submitted = st.form_submit_button("Send Message")
            if submitted:
                if name and email and message:
                    st.success("Thank you! Your message has been submitted. We'll get back to you soon.")
                else:
                    st.error("Please fill in all required fields (Name, Email, Message).")
        
        st.markdown("---")
        st.markdown("**Email:** aaabhishek841424@gmail.com")
        st.markdown("**Support:** https://infoofabhi.netlify.app/contact")

    # FAQ page
    elif page == "FAQ":
        st.markdown("# Frequently Asked Questions")
        st.markdown("---")
        
        with st.expander("What is DeepSync?"):
            st.markdown("""
            DeepSync is a lightweight desktop application that runs entirely on your computer. 
            It uses intent-based matching (no heavy ML models) to understand commands like "run notepad", 
            "what time is it", or "remember buy milk". It works offline and requires no API keys.
            """)
        
        with st.expander("Do I need an internet connection?"):
            st.markdown("No. DeepSync runs 100% offline. For voice recognition, you can use Pocketsphinx for fully offline speech-to-text.")
        
        with st.expander("What are the system requirements?"):
            st.markdown("""
            - **Python 3.7+** (Tkinter is built-in)
            - **Optional:** Microphone for voice, speakers for TTS
            - **Optional:** `pip install -r requirements.txt` for voice features
            - Works on Windows, macOS, and Linux
            """)
        
        with st.expander("Is my data private?"):
            st.markdown("Yes. All processing happens locally. Notes are stored in `data/notes.json` on your machine. No data is sent anywhere.")
        
        with st.expander("How do I install the desktop app?"):
            st.markdown("""
            1. Download the zip from this website
            2. Extract to a folder
            3. Open terminal in that folder
            4. Run `pip install -r requirements.txt` (optional, for voice)
            5. Run `python gui_app.py` or double-click `run_gui.bat` on Windows
            """)


if __name__ == "__main__":
    main()
