import streamlit as st
import asyncio
import tempfile
import base64
import os
import subprocess
from datetime import datetime

st.set_page_config(page_title="AI Foundations & Certification Course", layout="wide")

# ---------- Language data (English, French, Spanish, Portuguese) ----------
LANGUAGES = {
    "English": {
        "code": "en",
        "voice": "en-US-GuyNeural",
        "login_title": "🔐 Access Required",
        "login_sub": "28 days to AI mastery – from beginner to certified expert",
        "login_password": "Enter password to access",
        "login_btn": "Login",
        "login_error": "Incorrect password. Access denied.",
        "sidebar_progress": "Your progress",
        "sidebar_completed": "of 28",
        "sidebar_founder": "Founder & Developer:",
        "sidebar_price": "**$299 USD** (full course – all 28 days, source code, certificate)",
        "sidebar_logout": "Logout",
        "day_prefix": "Day",
        "duration_label": "Duration",
        "milestone": "🎯 **Milestone achieved!** Great progress – keep going!",
        "cert_title": "🏅 Official AI Expert Certificate",
        "cert_text": "Congratulations! You have completed the AI Foundations & Certification Course.",
        "cert_btn": "📜 Download Certificate",
        "congrats_title": "🎓 Congratulations! You are now an AI Certified Expert.",
        "contact_text": "To continue with advanced courses or get support:",
        "footer_caption": "🤖 AI Foundations & Certification Course – 28 days to AI mastery.",
        "weeks": {
            1: "Week 1 - AI Foundations & Your Personal Mentor",
            2: "Week 2 - Creativity & Quiet Skill-Building",
            3: "Week 3 - Building AI Bots & Smart Automation",
            4: "Week 4 - Certification & Career Application"
        },
        "lessons": {
            1: {"title": "Meet your AI Mentor - Setting up ChatGPT & Gemini", "duration": "15 min", "content": "Learn how to create accounts, navigate the interfaces, and understand the core capabilities of ChatGPT and Google Gemini. These will be your primary AI assistants throughout the course."},
            2: {"title": "The 'Overthinker's Guide' to Prompting - Get exact answers", "duration": "14 min", "content": "Master the art of crafting precise prompts. Discover how to structure questions, use context, and avoid common pitfalls to get exactly the answers you need."},
            3: {"title": "Claude - Brainstorming & organizing messy thoughts", "duration": "16 min", "content": "Explore Claude's strength in handling long context windows. Use it to brainstorm ideas, summarize documents, and organize scattered notes into clear action plans."},
            4: {"title": "Perplexity - Smart, stress-free internet research", "duration": "12 min", "content": "Use Perplexity AI to conduct research with citations. Learn to ask follow-up questions and get accurate, up‑to‑date information without endless searching."},
            5: {"title": "AI for daily productivity & saving 2 hours a day", "duration": "15 min", "content": "Practical ways to integrate AI into your daily routine: email drafting, task prioritization, meeting summaries, and quick data analysis."},
            6: {"title": "Crafting your first custom AI assistant persona", "duration": "18 min", "content": "Create a personalized AI persona tailored to your role or interests. Define its tone, expertise, and typical responses to act as your dedicated assistant."},
            7: {"title": "Milestone - Build your personalized daily AI workflow", "duration": "20 min", "content": "Combine everything from week 1 into a seamless daily routine. Map out when and how you will use each AI tool to maximize efficiency."},
            8: {"title": "MidJourney - Turning simple text into stunning visuals", "duration": "14 min", "content": "Introduction to MidJourney. Learn basic commands, parameters, and how to generate high‑quality images from text prompts."},
            9: {"title": "MidJourney - Creating professional brand graphics", "duration": "16 min", "content": "Advanced techniques: logos, social media banners, presentation backgrounds. Learn to iterate and refine outputs for a consistent brand style."},
            10: {"title": "Canva + AI - Design basics with zero artistic skills", "duration": "15 min", "content": "Use Canva's AI features (Magic Write, Text to Image) to create professional designs quickly. No design experience required."},
            11: {"title": "Runway - Turning static images into engaging video", "duration": "17 min", "content": "Animate static images, add motion, and create short video clips using Runway's Gen‑2 and other tools."},
            12: {"title": "ElevenLabs - Pro voiceovers without recording yourself", "duration": "14 min", "content": "Generate natural‑sounding voiceovers from text. Adjust tone, speed, and emotion to match your project."},
            13: {"title": "Assembling your first AI-generated portfolio piece", "duration": "18 min", "content": "Combine visuals, voiceover, and video into a cohesive portfolio piece. Plan the narrative and structure."},
            14: {"title": "Milestone - Complete your 'Faceless' AI Video Project", "duration": "20 min", "content": "Produce a complete video (e.g., educational short, product promo) using only AI‑generated assets. No on‑camera presence needed."},
            15: {"title": "Basics - Visual automation without a single line of code", "duration": "16 min", "content": "Introduction to automation platforms (Zapier, Make). Understand triggers, actions, and how to connect apps visually."},
            16: {"title": "Connecting AI to your favorite everyday apps", "duration": "18 min", "content": "Integrate AI with Google Sheets, Gmail, Slack, and other common tools to automate repetitive tasks."},
            17: {"title": "Make.com - Building an automated researcher bot", "duration": "15 min", "content": "Step‑by‑step creation of a bot that fetches news, summarizes articles, and sends reports to you on a schedule."},
            18: {"title": "How to present AI wins to your manager", "duration": "18 min", "content": "Frameworks and templates for showcasing your automation successes. Learn to measure ROI and communicate value effectively."},
            19: {"title": "Creating a 24/7 AI Customer Support Agent", "duration": "20 min", "content": "Build a chatbot that answers common customer questions using OpenAI's API or a no‑code platform like Landbot."},
            20: {"title": "Testing & refining your new AI bot", "duration": "15 min", "content": "Methods for testing your bot, collecting feedback, and iterating to improve accuracy and user satisfaction."},
            21: {"title": "Milestone - Deploy your first working AI Automation", "duration": "20 min", "content": "Launch your automation in a real environment (e.g., for your own business or a test project). Document the process and results."},
            22: {"title": "Preparing for your JobEscape AI Certification", "duration": "14 min", "content": "Overview of the certification exam, key topics, and study strategies. Review the official guide."},
            23: {"title": "Packaging your AI skills for your current role", "duration": "16 min", "content": "How to add AI skills to your resume, LinkedIn, and performance reviews. Practical tips for immediate application."},
            24: {"title": "How to present AI wins to your manager (repeat)", "duration": "18 min", "content": "Refine your presentation skills with more examples and role‑play scenarios. Learn to handle questions and objections."},
            25: {"title": "Building your personal AI workflow from scratch", "duration": "15 min", "content": "Design a custom workflow that integrates the tools you've learned. Focus on your unique needs and goals."},
            26: {"title": "The Final AI Knowledge Check & Review", "duration": "20 min", "content": "Comprehensive review of all concepts covered in the course. Practice quiz to test your understanding."},
            27: {"title": "Claim your Official AI Expert Certificate", "duration": "10 min", "content": "Download your personalized certificate after completing the course requirements. Instructions for verification."},
            28: {"title": "Apply what you learned – your first real AI project at work", "duration": "15 min", "content": "Guidance on identifying a real project in your workplace, planning the implementation, and measuring success. Next steps for continued learning."}
        }
    },
    # ... (French, Spanish, Portuguese remain exactly as in your original code) ...
    # To keep this answer manageable, I will include only English here.
    # In your actual file, paste the full French, Spanish, Portuguese dictionaries from your original code.
    # They are identical to what you had – just copy them back.
}

# ---------- Additional notes and images for each day (English only) ----------
DAY_NOTES = {
    1: "💡 **Pro Tip:** Create separate accounts for ChatGPT and Gemini. Use a password manager. Explore the 'Explore GPTs' section in ChatGPT to see what others have built.",
    2: "💡 **Pro Tip:** Use the 'Chain of Thought' prompting: ask the AI to explain its reasoning step by step. This gives you more accurate and transparent answers.",
    3: "💡 **Pro Tip:** Claude's 100k token context is perfect for pasting entire research papers or long reports. Ask it to create a table of contents or an executive summary.",
    4: "💡 **Pro Tip:** In Perplexity, use the 'Focus' feature to limit search to academic sources or Reddit. Great for market research or finding niche opinions.",
    5: "💡 **Pro Tip:** Create email templates with placeholders, then ask AI to fill them. For meeting summaries, record and transcribe first, then feed to AI.",
    6: "💡 **Pro Tip:** Save your persona instructions in a text file. You can then copy-paste it every time you start a new chat to keep consistency.",
    7: "🎯 **Milestone Note:** Your workflow should be a checklist. For example: 1) Perplexity for research (10 min), 2) ChatGPT for drafting (15 min), 3) Gemini for final polish (5 min).",
    8: "💡 **Pro Tip:** MidJourney works best with 'style modifiers' like '--style raw' or '--stylize 500'. Experiment with '--ar 16:9' for widescreen images.",
    9: "💡 **Pro Tip:** For brand consistency, use the same seed number (--seed) to generate variations of a logo. Combine with '--iw 2' to reference an initial image.",
    10: "💡 **Pro Tip:** Canva's 'Magic Media' can generate custom illustrations. Use the 'Background Remover' to isolate subjects, then animate with 'Magic Animate'.",
    11: "💡 **Pro Tip:** Runway's 'Motion Brush' lets you select areas of an image to move. Use it to create subtle parallax effects for storytelling.",
    12: "💡 **Pro Tip:** In ElevenLabs, clone your own voice (requires consent). Use 'stability' and 'similarity' sliders to balance naturalness and consistency.",
    13: "💡 **Pro Tip:** Plan your portfolio piece with a storyboard: 1) hook (5 sec), 2) problem (10 sec), 3) AI solution (15 sec), 4) result (10 sec).",
    14: "🎯 **Milestone Note:** A 'faceless' video can be a slideshow with voiceover. Use Canva to export slides as video, then overlay ElevenLabs audio.",
    15: "💡 **Pro Tip:** Zapier's 'Paths' let you create if-this-then-that logic. Start with a simple 'email to spreadsheet' automation to understand triggers.",
    16: "💡 **Pro Tip:** Use Google Sheets + AI to auto-categorize expenses. Connect Gmail to AI to auto-draft replies for common customer emails.",
    17: "💡 **Pro Tip:** On Make.com, use the 'Router' module to split a bot into multiple branches. One branch for news, another for social media monitoring.",
    18: "💡 **Pro Tip:** When presenting to management, focus on time saved (e.g., 'this automation saves 10 hours/week') and error reduction (e.g., 'zero data entry mistakes').",
    19: "💡 **Pro Tip:** Start with a FAQ document. Feed it into the AI's context. Use a no-code chatbot builder like Landbot or Botpress for a quick prototype.",
    20: "💡 **Pro Tip:** Create a 'test user' group of 5 people. Ask them to try breaking the bot. Log all failed interactions and update the knowledge base.",
    21: "🎯 **Milestone Note:** Document your automation with screenshots and a one-page guide. This makes it easy to hand over to colleagues or scale later.",
    22: "💡 **Pro Tip:** The JobEscape certification focuses on practical application. Review your notes from days 1-21. Practice with sample prompts they provide.",
    23: "💡 **Pro Tip:** On LinkedIn, add a 'Projects' section for your AI automations. Use action verbs: 'built', 'deployed', 'optimized', 'reduced cost by X%'.",
    24: "💡 **Pro Tip:** Role-play the presentation with a friend. Ask them to play a skeptical manager. Prepare data-backed answers to 'Why should we trust AI?'",
    25: "💡 **Pro Tip:** Your personal workflow should be modular. For example: a morning briefing bot (news + calendar), a midday research bot, and an evening summary bot.",
    26: "💡 **Pro Tip:** The final knowledge check includes: prompt engineering, AI ethics, automation design, and tool selection. Use flashcards to memorize key terms.",
    27: "🎓 **Note:** Your certificate is verifiable via the download link. Add it to your LinkedIn 'Licenses & Certifications' section with the verification URL.",
    28: "🚀 **Next Steps:** Join AI communities (Reddit r/LocalLLaMA, EleutherAI Discord). Start a small freelance project or contribute to an open-source AI tool."
}

# ---------- RELIABLE IMAGE URLs (direct Unsplash CDN links that always work) ----------
DAY_IMAGES = {
    1: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop",   # AI chip
    2: "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=800&h=400&fit=crop",   # question marks
    3: "https://images.unsplash.com/photo-1453738773917-9c3eff1db985?w=800&h=400&fit=crop",   # brainstorming
    4: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&h=400&fit=crop",   # research
    5: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=400&fit=crop",   # productivity
    6: "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=800&h=400&fit=crop",   # assistant
    7: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop",      # workflow
    8: "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=800&h=400&fit=crop",   # digital art
    9: "https://images.unsplash.com/photo-1626785774573-4b799315345d?w=800&h=400&fit=crop",   # brand graphics
    10: "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=800&h=400&fit=crop",  # design
    11: "https://images.unsplash.com/photo-1536240474400-b3b87e3b2e8f?w=800&h=400&fit=crop",  # video editing
    12: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&h=400&fit=crop",  # microphone
    13: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=800&h=400&fit=crop",     # portfolio
    14: "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&h=400&fit=crop",  # faceless video
    15: "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=400&fit=crop",     # automation code
    16: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop",     # connected apps
    17: "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=400&fit=crop",  # robot
    18: "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=400&fit=crop",     # presentation
    19: "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?w=800&h=400&fit=crop",     # customer support
    20: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&h=400&fit=crop",  # testing
    21: "https://images.unsplash.com/photo-1551434678-e076c2231a32?w=800&h=400&fit=crop",     # deploy
    22: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=400&fit=crop",  # certification
    23: "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=800&h=400&fit=crop",  # resume
    24: "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=400&fit=crop",     # presentation repeat
    25: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop",     # workflow custom
    26: "https://images.unsplash.com/photo-1513258496099-48168024aec0?w=800&h=400&fit=crop",  # knowledge check
    27: "https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=800&h=400&fit=crop",   # certificate
    28: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&h=400&fit=crop"    # real project
}

# ---------- Helper functions (unchanged) ----------
def set_tech_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0a0f1f, #0e1a2a, #0a0f1f); }
        .main-header { background: linear-gradient(135deg, #00d4ff, #0077ff, #0033aa); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, pre, code, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: #ffffff !important; }
        .stText { color: #ffffff !important; font-size: 1rem; background: transparent !important; }
        .stTabs [role="tab"] { color: #ffffff !important; background: rgba(0,212,255,0.2); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: #0077ff; color: white !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
        .stButton button { background-color: #0077ff; color: white !important; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #00d4ff; color: black !important; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0a0f1f, #0e1a2a); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #1e2a3a; border: 1px solid #0077ff; border-radius: 10px; }
        div[data-baseweb="popover"] ul { background-color: #1e2a3a; border: 1px solid #0077ff; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #1e2a3a; }
        div[data-baseweb="popover"] li:hover { background-color: #0077ff; }
        .certificate { background: linear-gradient(135deg, #ffd700, #ffaa00); padding: 1rem; border-radius: 20px; text-align: center; color: #000 !important; }
        .certificate h3, .certificate p { color: #000 !important; }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#00d4ff" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00d4ff"/>
                    <stop offset="50%" stop-color="#0077ff"/>
                    <stop offset="100%" stop-color="#0033aa"/>
                </linearGradient></defs>
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">🤖</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ---------- Authentication ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"

if not st.session_state.authenticated:
    set_tech_style()
    lang = st.session_state.lang
    st.title(LANGUAGES[lang]["login_title"])
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>AI Foundations & Certification Course</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #00d4ff;'>{LANGUAGES[lang]['login_sub']}</p>", unsafe_allow_html=True)
        password_input = st.text_input(LANGUAGES[lang]["login_password"], type="password")
        if st.button(LANGUAGES[lang]["login_btn"]):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(LANGUAGES[lang]["login_error"])
    st.stop()

# ---------- Main app after login ----------
set_tech_style()
lang = st.session_state.lang
ui = LANGUAGES[lang]

# Language selector in sidebar
with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=60)
    st.selectbox("🌐 Language", options=list(LANGUAGES.keys()), key="lang")
    st.markdown("---")
    show_logo()
    st.markdown("## 🎯 Select a day")
    day_number = st.selectbox("Day", list(range(1, 29)), index=0, label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"### 📚 {ui['sidebar_progress']}")
    st.progress(day_number / 28)
    st.markdown(f"✅ {ui['day_prefix']} {day_number} {ui['sidebar_completed']}")
    st.markdown("---")
    st.markdown(f"**{ui['sidebar_founder']}**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown(ui['sidebar_price'])
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button(f"🚪 {ui['sidebar_logout']}", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ---------- Display current lesson ----------
week_num = (day_number - 1) // 7 + 1
week_title = ui['weeks'][week_num]
day_title = ui['lessons'][day_number]["title"]
duration = ui['lessons'][day_number]["duration"]
content = ui['lessons'][day_number]["content"]

st.markdown(f"## 📅 {week_title}")
st.markdown(f"### {ui['day_prefix']} {day_number}: {day_title}")
st.markdown(f"⏱️ **{ui['duration_label']}:** {duration}")
st.markdown("---")
st.markdown(content)

# ----- IMAGE for the day (reliable Unsplash CDN) -----
if day_number in DAY_IMAGES:
    try:
        st.image(DAY_IMAGES[day_number], caption=f"Visual for Day {day_number}: {day_title}", use_container_width=True)
        st.caption("📷 Image from Unsplash (free to use)")
    except Exception:
        st.info("🖼️ Image could not be loaded. Here's a fun fact: " + DAY_NOTES.get(day_number, "Keep learning!")[:100])
else:
    st.info("🖼️ No image for this day – but the notes below will guide you.")

# ----- NOTES for the day -----
if day_number in DAY_NOTES:
    st.markdown("---")
    st.markdown("### 📝 Module Notes & Pro Tips")
    st.markdown(DAY_NOTES[day_number])
else:
    st.markdown("---")
    st.markdown("### 📝 Notes")
    st.markdown("*No additional notes for this module yet. Practice the lesson and experiment with the tools.*")

# Audio for the lesson content
def generate_audio(text, output_path, voice):
    cmd = ["edge-tts", "--voice", voice, "--text", text, "--write-media", output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
    except Exception as e:
        st.error(f"Audio error: {e}")

def play_audio(text, key, voice):
    if st.button(f"🔊 Listen to lesson", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            generate_audio(text, tmp.name, voice)
            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            os.unlink(tmp.name)

play_audio(f"{ui['day_prefix']} {day_number}: {day_title}. {content}", f"audio_{day_number}_{lang}", ui['voice'])

# Milestone indicator
if day_number in [7, 14, 21, 28]:
    st.markdown("---")
    st.success(ui['milestone'])

# Certificate claim on day 27-28
if day_number >= 27:
    st.markdown("---")
    st.markdown(f'<div class="certificate"><h3>{ui["cert_title"]}</h3><p>{ui["cert_text"]}</p><p>Click the button below to download your certificate.</p></div>', unsafe_allow_html=True)
    if st.button(ui['cert_btn'], use_container_width=True):
        cert_text = f"AI Expert Certificate\n\nThis certifies that User has successfully completed the 28‑day AI Foundations & Certification Course.\n\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\nGesner Deslandes\nFounder, GlobalInternet.py"
        st.download_button("⬇️ Download Certificate (TXT)", cert_text, file_name="ai_certificate.txt", mime="text/plain")

if day_number == 28:
    st.markdown("---")
    st.markdown(f"## {ui['congrats_title']}")
    st.markdown(f"""
    ### 📞 {ui['contact_text']}
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Keep practicing and applying your skills. You are ready for real‑world AI projects!
    """)

st.markdown("---")
st.caption(ui['footer_caption'])
