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
    layout="wide"
)

# Custom CSS for professional, company-style design
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #8b5cf6;
        --accent: #06b6d4;
        --accent-light: #22d3ee;
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        --bg-card: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border: rgba(148, 163, 184, 0.1);
        --border-hover: rgba(99, 102, 241, 0.3);
        --shadow: rgba(0, 0, 0, 0.1);
        --shadow-hover: rgba(99, 102, 241, 0.15);
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        --gradient-accent: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
        --gradient-bg: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    }
    
    /* Main container */
    .stApp {
        background: var(--gradient-bg);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navigation styling */
    .stSelectbox > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--border-hover) !important;
        box-shadow: 0 0 0 3px var(--shadow-hover) !important;
    }
    
    .stSelectbox > div > div > div {
        color: var(--text-primary) !important;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
        border-radius: 24px;
        padding: 4rem 3rem;
        margin: 2rem 0;
        border: 1px solid var(--border);
        text-align: center;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(99, 102, 241, 0.03) 50%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    .hero h1 {
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .hero p {
        font-size: 1.25rem;
        color: var(--text-secondary);
        max-width: 700px;
        margin: 0 auto 2rem;
        position: relative;
        z-index: 1;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid var(--border);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, transparent 0%, rgba(99, 102, 241, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: var(--border-hover);
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px var(--shadow-hover);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-card h3 {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .feature-card p {
        color: var(--text-muted);
        font-size: 1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Product showcase */
    .product-showcase {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(6, 182, 212, 0.08) 100%);
        border-radius: 24px;
        padding: 3rem;
        border: 1px solid var(--border-hover);
        margin: 2rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Stats */
    .stat-box {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        border-color: var(--border-hover);
        transform: translateY(-4px);
        box-shadow: 0 10px 30px var(--shadow);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: var(--text-muted);
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px var(--shadow-hover) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Section headers */
    .section-header {
        font-size: clamp(2rem, 4vw, 2.5rem);
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-subheader {
        color: var(--text-secondary);
        font-size: 1.2rem;
        margin-bottom: 3rem;
        max-width: 600px;
    }
    
    /* Download button specific styling */
    .stDownloadButton > button {
        background: var(--gradient-accent) !important;
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 15px 35px rgba(6, 182, 212, 0.3) !important;
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--border-hover) !important;
    }
    
    /* Table styling */
    .stMarkdown table {
        background: var(--bg-secondary);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border);
    }
    
    .stMarkdown th {
        background: var(--bg-tertiary);
        color: var(--text-primary);
        font-weight: 600;
        padding: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .stMarkdown td {
        color: var(--text-secondary);
        padding: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    /* Code styling */
    .stCodeBlock {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid var(--border);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero {
            padding: 2rem 1.5rem;
        }
        
        .hero h1 {
            font-size: 2.5rem;
        }
        
        .feature-card {
            padding: 1.5rem;
        }
        
        .stat-box {
            padding: 1.5rem;
        }
        
        .stat-number {
            font-size: 2.5rem;
        }
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
    # Professional header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            BATCH SEVEN AI & DATA SCIENCE
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem; margin: 0.5rem 0 0 0; font-weight: 400;">
            Enterprise AI Solutions
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Local Agent", "Products", "Contact", "FAQ"])
    
    with tab1:
        # Hero section
        st.markdown("""
        <div class="hero">
            <h1>Transforming Business with AI</h1>
            <p>Enterprise-grade AI solutions that empower businesses. From cloud APIs to fully local agents—deploy intelligence where you need it most.</p>
            <div style="margin-top: 2rem;">
                <button style="background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%); color: white; border: none; padding: 1rem 2rem; border-radius: 12px; font-weight: 600; font-size: 1rem; cursor: pointer; margin: 0 1rem; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 10px 25px rgba(6, 182, 212, 0.3)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                    Explore Solutions
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">100%</div>
                <div class="stat-label">Local & Private</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">0</div>
                <div class="stat-label">API Keys Needed</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Offline Ready</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">∞</div>
                <div class="stat-label">No Usage Limits</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Featured product - DeepSync
        st.markdown('<p class="section-header">Featured: DeepSync Desktop App</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-subheader">Your personal AI assistant that runs entirely on your machine. No cloud. No subscriptions. No limits.</p>', unsafe_allow_html=True)
        
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown("""
            <div class="product-showcase">
                <h3 style="color: #22d3ee; font-size: 1.8rem; font-weight: 700; margin-bottom: 1rem;">DeepSync Desktop App</h3>
                <p style="color: #cbd5e1; font-size: 1.1rem; margin: 1.5rem 0; line-height: 1.7;">
                A lightweight desktop application that brings AI capabilities to your computer—completely offline. 
                Run commands, manage notes, search files, and control your system with natural language and voice.
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin: 1.5rem 0;">
                    <span style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">Voice Recognition</span>
                    <span style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">Text-to-Speech</span>
                    <span style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">Modern GUI</span>
                    <span style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">100% Private</span>
                </div>
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
                <p>Deploy AI that runs entirely on your infrastructure. Zero data leakage, full compliance, and complete control over your data.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>Cloud AI APIs</h3>
                <p>Scalable, managed AI endpoints for high-throughput applications. Enterprise-grade reliability with flexible deployment options.</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>Custom Solutions</h3>
                <p>Tailored AI systems built for your unique workflows. From automation to intelligent assistants, designed specifically for your needs.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
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
    
    with tab3:
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
    
    with tab4:
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
        st.markdown("**Support:** https://infoofabhi.netlify.app")
    
    with tab5:
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

    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
    © 2026 BATCH SEVEN AI & DATA SCIENCE<br>
    Enterprise AI Solutions
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
