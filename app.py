import streamlit as st
import asyncio
import tempfile
import base64
import os
import subprocess
from datetime import datetime

st.set_page_config(page_title="AI & Robotics Insights", layout="wide")

# ---------- Language data ----------
LANGUAGES = {
    "English": {
        "code": "en",
        "voice": "en-US-GuyNeural",
        "login_title": "🔐 Access Required",
        "login_sub": "2 essential insights – LLMs & dexterous robotics",
        "login_password": "Enter password to access",
        "login_btn": "Login",
        "login_error": "Incorrect password. Access denied.",
        "sidebar_progress": "Your progress",
        "sidebar_completed": "of 2",
        "sidebar_founder": "Founder & Developer:",
        "sidebar_price": "**$49 USD** (complete insights, source code included)",
        "sidebar_logout": "Logout",
        "module_prefix": "Module",
        "duration_label": "Reading time",
        "next_module": "Next Module",
        "prev_module": "Previous Module",
        "footer_caption": "🤖 AI & Robotics Insights – stay ahead of the curve.",
        "modules": {
            1: {
                "title": "Introduction to LLMs (Stanford Lecture)",
                "duration": "2 hours (self‑paced)",
                "content": """
                **What you'll learn:**  
                This 2‑hour Stanford lecture breaks down how models like GPT, Gemini, and Claude are actually built – clearer than what many people in top AI roles ever get exposed to.  
                
                **Key takeaways:**  
                - How large language models are trained (pre‑training, fine‑tuning, RLHF).  
                - The architecture behind transformers and attention mechanisms.  
                - Why scale and data quality matter more than raw parameter count.  
                - Practical limitations: hallucinations, context windows, and inference costs.  
                
                **Why this matters:**  
                Understanding the fundamentals of LLMs gives you a massive advantage in leveraging AI for your work, regardless of your technical background.  
                
                **Action step:**  
                Set aside two hours this weekend to watch the full lecture. It might be the most valuable thing you learn all week.  
                
                🔗 Link to the video in the comments (or contact us for the direct URL).
                """,
                "audio_text": "Introduction to Large Language Models. This Stanford lecture explains how GPT, Gemini and Claude are built. Key topics: training, transformers, attention, and practical limitations. Save two hours this weekend to watch it."
            },
            2: {
                "title": "Dexterous Robotics – BrainCo's Breakthrough",
                "duration": "15 min read",
                "content": """
                **What happened:**  
                China's BrainCo unveiled a next‑generation dexterous robotic hand that moves with precision and agility previously thought only human hands could achieve. It performs fine, delicate tasks – not just grab and release.  
                
                **What it means:**  
                The gap between "robot doing repetitive tasks" and "robot doing skilled human work" is closing fast. Industries that relied on human dexterity as a barrier to automation no longer can. Hardware is catching up to the AI software moment.  
                
                **Why you should care:**  
                - If your operations involve manual, detail‑oriented work (assembly, healthcare, logistics, lab work), the timeline for automation just got shorter.  
                - This is not a lab prototype – it's a signal that dexterous robotics is entering deployment range.  
                - Leaders who understand this shift now will make better workforce and investment decisions.  
                
                **Which industry gets disrupted first?**  
                Healthcare (surgery assistance), electronics assembly, and last‑mile logistics are prime candidates.
                """,
                "audio_text": "China's BrainCo unveiled a dexterous robotic hand that mimics human precision. It performs fine tasks, not just gripping. This signals that skilled manual work automation is arriving sooner than expected. Industries like healthcare, assembly, and logistics should prepare."
            }
        }
    },
    "French": {
        "code": "fr",
        "voice": "fr-FR-HenriNeural",
        "login_title": "🔐 Accès requis",
        "login_sub": "2 informations essentielles – LLM et robotique dextre",
        "login_password": "Entrez le mot de passe pour accéder",
        "login_btn": "Se connecter",
        "login_error": "Mot de passe incorrect. Accès refusé.",
        "sidebar_progress": "Votre progression",
        "sidebar_completed": "sur 2",
        "sidebar_founder": "Fondateur et développeur :",
        "sidebar_price": "**49 $ USD** (informations complètes, code source inclus)",
        "sidebar_logout": "Déconnexion",
        "module_prefix": "Module",
        "duration_label": "Temps de lecture",
        "next_module": "Module suivant",
        "prev_module": "Module précédent",
        "footer_caption": "🤖 IA et robotique – restez en avance.",
        "modules": {
            1: {
                "title": "Introduction aux LLM (cours de Stanford)",
                "duration": "2 heures (à votre rythme)",
                "content": """
                **Ce que vous apprendrez :**  
                Ce cours de Stanford de 2 heures explique comment les modèles comme GPT, Gemini et Claude sont réellement construits – plus clairement que ce que beaucoup de personnes dans des postes IA de haut niveau n'ont jamais vu.  
                
                **Points clés :**  
                - Comment les grands modèles de langage sont entraînés (pré‑entraînement, ajustement fin, RLHF).  
                - L'architecture des transformateurs et des mécanismes d'attention.  
                - Pourquoi l'échelle et la qualité des données comptent plus que le nombre de paramètres.  
                - Limites pratiques : hallucinations, fenêtres de contexte, coûts d'inférence.  
                
                **Pourquoi c'est important :**  
                Comprendre les fondamentaux des LLM vous donne un avantage considérable pour utiliser l'IA dans votre travail, quel que soit votre niveau technique.  
                
                **Action :**  
                Réservez deux heures ce week‑end pour regarder la conférence complète. Cela pourrait être la chose la plus utile que vous apprendrez de la semaine.  
                
                🔗 Lien vers la vidéo dans les commentaires (ou contactez‑nous pour l'URL directe).
                """,
                "audio_text": "Introduction aux grands modèles de langage. Ce cours de Stanford explique comment GPT, Gemini et Claude sont construits. Sujets clés : entraînement, transformeurs, attention et limites pratiques."
            },
            2: {
                "title": "Robotique dextre – la percée de BrainCo",
                "duration": "15 min de lecture",
                "content": """
                **Ce qui s'est passé :**  
                BrainCo, une entreprise chinoise, a dévoilé une main robotique dextre de nouvelle génération qui imite la précision et l'agilité d'une main humaine. Elle peut effectuer des tâches fines et délicates – pas seulement saisir et relâcher.  
                
                **Ce que cela signifie :**  
                L'écart entre « robot effectuant des tâches répétitives » et « robot effectuant un travail qualifié » se réduit rapidement. Les industries qui comptaient sur la dextérité humaine comme barrière à l'automatisation ne le peuvent plus. Le matériel rattrape le moment de l'IA logicielle.  
                
                **Pourquoi vous devriez vous y intéresser :**  
                - Si vos opérations impliquent un travail manuel et méticuleux (assemblage, soins de santé, logistique, travail de laboratoire), le calendrier d'automatisation vient de se raccourcir.  
                - Ce n'est pas un prototype de laboratoire – c'est un signal que la robotique dextre entre dans la phase de déploiement.  
                - Les leaders qui comprennent ce changement maintenant prendront de meilleures décisions en matière de main‑d'œuvre et d'investissement.  
                
                **Quel secteur sera perturbé en premier ?**  
                Les soins de santé (assistance chirurgicale), l'assemblage électronique et la logistique du dernier kilomètre sont des candidats de choix.
                """,
                "audio_text": "BrainCo a dévoilé une main robotique dextre imitant la précision humaine. Elle effectue des tâches fines, pas seulement la préhension. Cela signale que l'automatisation du travail manuel qualifié arrive plus tôt que prévu."
            }
        }
    },
    "Spanish": {
        "code": "es",
        "voice": "es-ES-AlvaroNeural",
        "login_title": "🔐 Acceso requerido",
        "login_sub": "2 ideas esenciales – LLM y robótica diestra",
        "login_password": "Ingrese la contraseña para acceder",
        "login_btn": "Iniciar sesión",
        "login_error": "Contraseña incorrecta. Acceso denegado.",
        "sidebar_progress": "Tu progreso",
        "sidebar_completed": "de 2",
        "sidebar_founder": "Fundador y desarrollador:",
        "sidebar_price": "**$49 USD** (información completa, código fuente incluido)",
        "sidebar_logout": "Cerrar sesión",
        "module_prefix": "Módulo",
        "duration_label": "Tiempo de lectura",
        "next_module": "Siguiente módulo",
        "prev_module": "Módulo anterior",
        "footer_caption": "🤖 IA y robótica – mantente a la vanguardia.",
        "modules": {
            1: {
                "title": "Introducción a los LLM (conferencia de Stanford)",
                "duration": "2 horas (a su ritmo)",
                "content": "...",
                "audio_text": "..."
            },
            2: {
                "title": "Robótica diestra – el avance de BrainCo",
                "duration": "15 min de lectura",
                "content": "...",
                "audio_text": "..."
            }
        }
    },
    "Portuguese": {
        "code": "pt",
        "voice": "pt-BR-FranciscaNeural",
        "login_title": "🔐 Acesso necessário",
        "login_sub": "2 insights essenciais – LLM e robótica hábil",
        "login_password": "Digite a senha para acessar",
        "login_btn": "Entrar",
        "login_error": "Senha incorreta. Acesso negado.",
        "sidebar_progress": "Seu progresso",
        "sidebar_completed": "de 2",
        "sidebar_founder": "Fundador e desenvolvedor:",
        "sidebar_price": "**$49 USD** (insights completos, código fonte incluído)",
        "sidebar_logout": "Sair",
        "module_prefix": "Módulo",
        "duration_label": "Tempo de leitura",
        "next_module": "Próximo módulo",
        "prev_module": "Módulo anterior",
        "footer_caption": "🤖 IA e robótica – fique à frente.",
        "modules": {
            1: {
                "title": "Introdução aos LLMs (aula de Stanford)",
                "duration": "2 horas (auto‑ritmo)",
                "content": "...",
                "audio_text": "..."
            },
            2: {
                "title": "Robótica hábil – o avanço da BrainCo",
                "duration": "15 min de leitura",
                "content": "...",
                "audio_text": "..."
            }
        }
    }
}

# ---------- Helper functions ----------
def set_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0a0f1f, #0e1a2a, #0a0f1f); }
        .main-header { background: linear-gradient(135deg, #00d4ff, #0077ff, #0033aa); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, pre, code, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: #ffffff !important; }
        .stText { color: #ffffff !important; font-size: 1rem; background: transparent !important; }
        .stButton button { background-color: #0077ff; color: white !important; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #00d4ff; color: black !important; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0a0f1f, #0e1a2a); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #1e2a3a; border: 1px solid #0077ff; border-radius: 10px; }
        div[data-baseweb="popover"] ul { background-color: #1e2a3a; border: 1px solid #0077ff; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #1e2a3a; }
        div[data-baseweb="popover"] li:hover { background-color: #0077ff; }
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
                <text x="50" y="65" font-size="40" text-anchor="middle" fill="white" font-weight="bold">🧠</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

def generate_audio(text, output_path, voice):
    cmd = ["edge-tts", "--voice", voice, "--text", text, "--write-media", output_path]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
    except Exception as e:
        st.error(f"Audio error: {e}")

def play_audio(text, key, voice):
    if st.button(f"🔊 Listen / Écouter / Escuchar / Ouvir", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            generate_audio(text, tmp.name, voice)
            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            os.unlink(tmp.name)

# ---------- Authentication ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "module_index" not in st.session_state:
    st.session_state.module_index = 0

if not st.session_state.authenticated:
    set_style()
    lang = st.session_state.lang
    st.title(LANGUAGES[lang]["login_title"])
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>AI & Robotics Insights</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #00d4ff;'>{LANGUAGES[lang]['login_sub']}</p>", unsafe_allow_html=True)
        password_input = st.text_input(LANGUAGES[lang]["login_password"], type="password")
        if st.button(LANGUAGES[lang]["login_btn"]):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(LANGUAGES[lang]["login_error"])
    st.stop()

# ---------- Main app ----------
set_style()
lang = st.session_state.lang
ui = LANGUAGES[lang]

# Language selector in sidebar
with st.sidebar:
    st.image("https://flagcdn.com/w320/ht.png", width=60)
    st.selectbox("🌐 Language", options=list(LANGUAGES.keys()), key="lang")
    st.markdown("---")
    show_logo()
    st.markdown(f"## 🎯 {ui['module_prefix']}")
    module_number = st.selectbox("", [1, 2], index=st.session_state.module_index, format_func=lambda x: f"{ui['module_prefix']} {x}: {ui['modules'][x]['title'][:30]}...", label_visibility="collapsed")
    st.session_state.module_index = module_number - 1
    st.markdown("---")
    st.markdown(f"### 📚 {ui['sidebar_progress']}")
    st.progress(module_number / 2)
    st.markdown(f"✅ {ui['module_prefix']} {module_number} {ui['sidebar_completed']}")
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

# ---------- Display current module ----------
module = ui['modules'][module_number]
st.markdown(f"## {ui['module_prefix']} {module_number}: {module['title']}")
st.markdown(f"⏱️ **{ui['duration_label']}:** {module['duration']}")
st.markdown("---")
st.markdown(module['content'])

# Audio
play_audio(module['audio_text'], f"audio_{module_number}_{lang}", ui['voice'])

# Navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if module_number > 1:
        if st.button(f"⬅️ {ui['prev_module']}", use_container_width=True):
            st.session_state.module_index = module_number - 2
            st.rerun()
with col3:
    if module_number < 2:
        if st.button(f"{ui['next_module']} ➡️", use_container_width=True):
            st.session_state.module_index = module_number
            st.rerun()

if module_number == 2:
    st.markdown("---")
    st.markdown("## 🎓 You have completed both insights.")
    st.markdown("""
    ### 📞 To get more advanced content or support:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [GlobalInternet.py](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    Keep learning – the future belongs to those who understand AI and robotics.
    """)

st.markdown("---")
st.caption(ui['footer_caption'])
