"""
ReadMe Forge — AI-powered README.md generator
Stack: Streamlit + LangChain + DeepSeek

Run:  streamlit run readme_forge.py
"""

import json

import streamlit as st
import streamlit.components.v1 as components

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReadMe Forge",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS — MODERN DARK GLASS THEME
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(ellipse 80% 50% at 10% -10%, rgba(16,185,129,0.16), transparent 60%),
            radial-gradient(ellipse 65% 50% at 92% 0%, rgba(6,182,212,0.14), transparent 60%),
            radial-gradient(ellipse 70% 60% at 50% 110%, rgba(99,102,241,0.10), transparent 60%),
            #0a0f14;
        color: #e6edf3;
        font-family: 'Plus Jakarta Sans', ui-sans-serif, sans-serif;
        color-scheme: dark;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981, #22d3ee, #818cf8);
        z-index: 999;
    }

    .block-container {
        padding: 2rem 1rem 4rem;
        max-width: 1150px;
        margin: 0 auto;
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    ::selection { background: rgba(16,185,129,0.40); }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.14);
        border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }

    /* ---------- HERO ---------- */

    @keyframes rise {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: none; }
    }

    @keyframes gradient-flow {
        to { background-position: 300% center; }
    }

    .hero {
        text-align: center;
        animation: rise 0.6s ease both;
        margin-bottom: 24px;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        color: #9aa5b1;
        font-size: 12.5px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin: 0 0 10px 0;
        background: linear-gradient(90deg, #34d399, #22d3ee, #818cf8, #34d399);
        background-size: 300% auto;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-flow 6s linear infinite;
    }

    .hero-sub {
        color: #8b93a7;
        font-size: 16.5px;
        margin: 0 0 18px 0;
    }

    .hero-sub b { color: #c7cdd9; }

    .pills {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 999px;
        background: rgba(16,185,129,0.10);
        border: 1px solid rgba(16,185,129,0.28);
        color: #6ee7b7;
        font-size: 12.5px;
        font-weight: 600;
    }

    /* ---------- TITLES ---------- */

    .section-title {
        font-size: 17px;
        font-weight: 700;
        margin: 6px 0 10px 0;
        color: #eef2f7;
    }

    [data-testid="stWidgetLabel"] p {
        color: #9aa5b1 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* ---------- INPUTS ---------- */

    .stTextInput input,
    .stTextArea textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: #eef2f7 !important;
        caret-color: #34d399;
        transition: border-color .25s ease, box-shadow .25s ease;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: rgba(16,185,129,0.60) !important;
        box-shadow: 0 0 0 4px rgba(16,185,129,0.12) !important;
    }

    .stTextArea textarea::placeholder,
    .stTextInput input::placeholder {
        color: #5b6472 !important;
    }

    /* ---------- SELECT / MULTISELECT ---------- */

    [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        min-height: 44px;
        color: #eef2f7 !important;
        transition: border-color .2s ease;
    }

    [data-baseweb="select"] > div:hover {
        border-color: rgba(16,185,129,0.5) !important;
    }

    [data-baseweb="popover"] {
        background: #141b24 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    [data-baseweb="popover"] [role="option"] { color: #e6edf3 !important; }

    [data-baseweb="popover"] [role="option"]:hover {
        background: rgba(16,185,129,0.16) !important;
    }

    [data-baseweb="tag"] {
        background: rgba(16,185,129,0.14) !important;
        border: 1px solid rgba(52,211,153,0.38) !important;
        border-radius: 8px !important;
    }

    [data-baseweb="tag"] span { color: #d1fae5 !important; }
    [data-baseweb="tag"] svg { fill: #a7f3d0; }

    /* ---------- CHECKBOX ---------- */

    [data-testid="stCheckbox"] label {
        color: #c7cdd6 !important;
        font-size: 14px !important;
        transition: color .15s ease;
    }

    [data-testid="stCheckbox"] label:hover { color: #ffffff !important; }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        color: #dbe0ea;
        border-radius: 12px;
        font-weight: 600;
        padding: 9px 18px;
        font-size: 13.5px;
        transition: all .22s ease;
    }

    .stButton > button:hover {
        border-color: rgba(16,185,129,0.60);
        background: rgba(16,185,129,0.10);
        transform: translateY(-1px);
    }

    button[kind="primary"],
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #10b981, #0891b2) !important;
        border: none !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        height: 54px;
        border-radius: 15px !important;
        box-shadow: 0 8px 26px rgba(16,185,129,0.35);
        transition: all .25s ease;
    }

    button[kind="primary"]:hover,
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px);
        filter: brightness(1.12);
        box-shadow: 0 14px 34px rgba(16,185,129,0.48);
    }

    .stDownloadButton > button {
        background: rgba(16,185,129,0.10) !important;
        border: 1px solid rgba(52,211,153,0.45) !important;
        color: #6ee7b7 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        height: 46px;
        transition: all .22s ease;
    }

    .stDownloadButton > button:hover {
        background: rgba(16,185,129,0.20) !important;
        transform: translateY(-1px);
    }

    /* ---------- CARDS / CONTAINERS ---------- */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 18px !important;
    }

    /* ---------- TABS ---------- */

    [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 8px 18px;
        color: #8b93a7;
        font-weight: 600;
        border-bottom: 2px solid transparent;
    }

    [data-baseweb="tab"] p { color: inherit !important; }

    [data-baseweb="tab"][aria-selected="true"] {
        color: #34d399 !important;
        border-bottom: 2px solid #34d399;
        background: rgba(16,185,129,0.08);
    }

    /* ---------- CODE ---------- */

    .stCode {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        overflow: hidden;
    }

    /* ---------- EXPANDER / MISC ---------- */

    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        overflow: hidden;
        transition: border-color .2s ease;
    }

    [data-testid="stExpander"]:hover {
        border-color: rgba(16,185,129,0.40) !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stCaptionContainer"] { color: #7d8794 !important; }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: rgba(11,16,21,0.90);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    .side-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }

    .side-logo {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: linear-gradient(135deg, #10b981, #0891b2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 8px 20px rgba(16,185,129,0.32);
    }

    .side-name { font-weight: 800; font-size: 17px; color: #f1f5f9; }
    .side-tag  { font-size: 11.5px; color: #7d8794; margin-top: 1px; }

    .side-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 14px;
        margin-top: 12px;
    }

    .side-card-title {
        font-size: 13px;
        font-weight: 700;
        color: #c7cdd9;
        margin-bottom: 8px;
        letter-spacing: 0.3px;
    }

    .step { font-size: 13px; color: #aab3bd; padding: 3px 0; }

    .status {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        font-weight: 600;
        color: #c7cdd9;
        margin-top: 10px;
    }

    .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
    .dot-green { background: #34d399; box-shadow: 0 0 8px #34d399; }
    .dot-amber { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }

    @media (max-width: 768px) {
        .hero-title { font-size: 34px; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "readme" not in st.session_state:
    st.session_state.readme = ""

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# CONSTANTS
# ============================================================

PROJECT_TYPES = [
    "🌐 Web App",
    "🤖 AI / ML Project",
    "🛠️ CLI Tool",
    "📚 Library / Package",
    "🔌 API / Backend",
    "📱 Mobile App",
    "🖥️ Desktop App",
    "⚙️ Automation Script",
    "🎮 Game",
    "📊 Data Project",
]

DETAIL_STYLES = ["Detailed", "Standard", "Concise", "Beginner-friendly"]

STACKS = [
    "Python", "JavaScript", "TypeScript", "React", "Next.js", "Vue",
    "Node.js", "Streamlit", "LangChain", "FastAPI", "Flask", "Django",
    "PyTorch", "TensorFlow", "Scikit-learn", "Docker", "Kubernetes",
    "PostgreSQL", "MongoDB", "Redis", "Tailwind CSS", "Flutter", "Go", "Rust",
]

LICENSES = [
    "MIT License",
    "Apache License 2.0",
    "GNU GPL v3",
    "BSD 3-Clause",
    "Mozilla Public License 2.0",
    "The Unlicense",
    "No license yet",
]

SECTION_OPTIONS = [
    ("sec_badges",    "🏅 Badges"),
    ("sec_features",  "✨ Features"),
    ("sec_stack",     "🧰 Tech Stack table"),
    ("sec_install",   "📦 Installation"),
    ("sec_usage",     "🚀 Usage / Examples"),
    ("sec_shots",     "🖼️ Screenshots placeholder"),
    ("sec_structure", "🗂️ Project Structure"),
    ("sec_contrib",   "🤝 Contributing"),
    ("sec_roadmap",   "🗺️ Roadmap"),
    ("sec_faq",       "❓ FAQ"),
    ("sec_license",   "📄 License section"),
    ("sec_thanks",    "🙏 Acknowledgements"),
]

SECTION_PROMPTS = {
    "sec_badges":    "Badges (shields.io) at the top",
    "sec_features":  "Features list",
    "sec_stack":     "Tech Stack table",
    "sec_install":   "Prerequisites + Installation steps",
    "sec_usage":     "Usage / Examples with code blocks",
    "sec_shots":     "Screenshots section with an image placeholder",
    "sec_structure": "Project Structure (file tree — use the provided structure if available)",
    "sec_contrib":   "Contributing guidelines",
    "sec_roadmap":   "Roadmap",
    "sec_faq":       "FAQ",
    "sec_license":   "License section",
    "sec_thanks":    "Acknowledgements",
}

SYSTEM_PROMPT = """
You are ReadMe Forge, an elite technical writer and
open-source documentation expert.

You transform project descriptions into world-class
README.md files — the kind seen in top GitHub repositories.

==================================================
OUTPUT FORMAT — STRICT RULES
==================================================

1. Return ONLY the README content as raw Markdown.

2. Do NOT wrap the README in code fences.
   (No triple backticks at the beginning or end.)

3. Do NOT add any explanation before or after.

4. Start with a single H1 title, then the tagline
   as an italic line, then badges.

5. Use Markdown image syntax for badges:
   ![Badge](https://img.shields.io/badge/...)
   Never use raw <img> tags for badges.

6. You MAY use minimal HTML such as
   <div align="center"> ... </div>
   for the header block.

==================================================
CONTENT RULES
==================================================

1. Use the project brief as the source of truth.

2. Never invent features or facts that were not
   provided in the brief.

3. If information is missing, insert a clear
   placeholder such as:
   <!-- TODO: add ... -->
   instead of making things up.

4. Include ONLY the sections listed under
   "SECTIONS TO INCLUDE".

5. Installation and usage commands must match
   the given tech stack (pip for Python,
   npm for Node, cargo for Rust, etc.).

6. Use fenced code blocks with correct language tags.

7. Use tables where they help (tech stack,
   environment variables, options).

8. Write clear, friendly, professional prose.

9. When the style is "Detailed", include a
   Table of Contents with anchor links after badges.

10. Use emoji in section headings sparingly
    and consistently.

==================================================
STYLE
==================================================

Detail level: {style}
"""


# ============================================================
# HELPERS
# ============================================================

def clean_markdown(text: str) -> str:

    """Strip accidental code fences the model may add."""

    text = text.strip()

    if text.startswith("```"):

        lines = text.split("\n")

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


def render_copy_button(text: str) -> None:

    """Client-side copy button in its own iframe."""

    payload = json.dumps(text).replace("<", "\\u003c")

    components.html(
        f"""
        <html>
        <body style="margin:0; background:transparent;">
          <button id="copyBtn"
            style="
              display:inline-flex; align-items:center; gap:6px;
              background:rgba(255,255,255,0.06);
              border:1px solid rgba(255,255,255,0.16);
              color:#e6edf3; border-radius:12px;
              padding:11px 20px; font-size:13.5px; font-weight:600;
              cursor:pointer; font-family:'Plus Jakarta Sans',sans-serif;
              transition:all .2s ease;"
            onmouseover="this.style.borderColor='rgba(16,185,129,0.7)'"
            onmouseout="this.style.borderColor='rgba(255,255,255,0.16)'">
            📋 Copy README
          </button>
          <script>
            const __text = {payload};
            const btn = document.getElementById('copyBtn');
            btn.addEventListener('click', async () => {{
              try {{
                await navigator.clipboard.writeText(__text);
              }} catch (e) {{
                const ta = document.createElement('textarea');
                ta.value = __text;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
              }}
              btn.innerHTML = '✅ Copied!';
              setTimeout(() => {{ btn.innerHTML = '📋 Copy README'; }}, 1600);
            }});
          </script>
        </body>
        </html>
        """,
        height=52,
        scrolling=False,
    )


# ============================================================
# GENERATION FUNCTION
# ============================================================

def generate_readme(
    project_name: str,
    tagline: str,
    description: str,
    repo_url: str,
    project_type: str,
    stack: list,
    features: str,
    author: str,
    license_name: str,
    file_tree: str,
    extra_notes: str,
    sections: list,
    style: str,
    model_name: str,
    api_key: str,
) -> str:

    """Generate a full README.md using DeepSeek through LangChain."""

    if not api_key:
        raise ValueError("DeepSeek API key is missing.")

    api_key = api_key.strip()

    if not api_key:
        raise ValueError("DeepSeek API key is empty.")

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://api.deepseek.com",
        temperature=0.4,
    )

    # --------------------------------------------------------
    # Build blocks
    # --------------------------------------------------------

    features_block = (
        "\n".join(
            f"- {line.strip()}"
            for line in features.splitlines()
            if line.strip()
        )
        if features
        else "(not provided — infer sensible features from the description)"
    )

    sections_block = "\n".join(
        f"- {section}" for section in sections
    )

    stack_block = ", ".join(stack) if stack else "(not specified — infer from description)"

    # --------------------------------------------------------
    # Project brief
    # --------------------------------------------------------

    brief = f"""PROJECT BRIEF
==============

Name: {project_name}
Tagline: {tagline if tagline else "(not provided — write a fitting one-line tagline)"}
Description: {description}
Repository URL: {repo_url if repo_url else "(not provided)"}
Project type: {project_type}
Tech stack: {stack_block}

Main features:
{features_block}

Author: {author if author else "(not provided)"}
License: {license_name}

Project file structure (optional):
{file_tree if file_tree else "(not provided)"}

Extra notes (optional):
{extra_notes if extra_notes else "(none)"}

SECTIONS TO INCLUDE
-------------------
{sections_block}
"""

    # --------------------------------------------------------
    # Chain
    # --------------------------------------------------------

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{brief}"),
        ]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "brief": brief,
            "style": style,
        }
    )

    result = response.content

    if isinstance(result, list):
        result = "".join(str(item) for item in result)

    result = clean_markdown(str(result))

    if not result:
        raise ValueError("DeepSeek returned an empty response.")

    return result


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="side-brand">
            <div class="side-logo">📖</div>
            <div>
                <div class="side-name">ReadMe Forge</div>
                <div class="side-tag">AI README Generator</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model = st.selectbox(
        "Model",
        [
            "deepseek-v4-flash",
            "deepseek-v4-pro",
        ],
        index=0,
    )

    st.divider()

    st.markdown(
        '<div class="side-card-title">🔑 DeepSeek API Key</div>',
        unsafe_allow_html=True,
    )

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-...",
        label_visibility="collapsed",
        help="Enter your DeepSeek API key.",
    )

    if api_key:
        st.markdown(
            '<div class="status"><span class="dot dot-green"></span> Ready to forge</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status"><span class="dot dot-amber"></span> API key required</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        """
        <div class="side-card">
            <div class="side-card-title">🛠️ HOW IT WORKS</div>
            <div class="step">1️⃣ Describe your project</div>
            <div class="step">2️⃣ Pick sections &amp; style</div>
            <div class="step">3️⃣ Generate, copy, ship</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption("Powered by DeepSeek + LangChain")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">⚡ Powered by DeepSeek + LangChain</div>
        <h1 class="hero-title">📖 ReadMe Forge</h1>
        <p class="hero-sub">
            Turn project details into a
            <b>beautiful, professional README.md</b> — in seconds
        </p>
        <div class="pills">
            <span class="pill">🧠 Stack-aware commands</span>
            <span class="pill">🏅 Shields.io badges</span>
            <span class="pill">🧩 12 sections</span>
            <span class="pill">📦 Instant download</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DEMO PROJECT LOADER
# ============================================================

if st.button("🎲  Load example project"):

    st.session_state.update(
        {
            "project_name": "NeuraChat",
            "repo_url": "https://github.com/yourname/neurachat",
            "tagline": "A privacy-first AI chat assistant that runs fully on your machine",
            "description": (
                "NeuraChat is an open-source chat application that lets you talk to "
                "local large language models without sending a single byte to the cloud. "
                "It ships with conversation memory, streaming replies and a clean dark UI."
            ),
            "project_type": "🤖 AI / ML Project",
            "detail_style": "Detailed",
            "stack_multi": ["Python", "Streamlit", "LangChain", "FastAPI"],
            "license_sel": "MIT License",
            "author": "Your Name",
            "features": (
                "Chat with local LLMs (Ollama, llama.cpp)\n"
                "Streaming token-by-token responses\n"
                "Conversation memory\n"
                "Export chats as Markdown\n"
                "Fully offline & private"
            ),
            "file_tree": (
                "neurachat/\n"
                "├── app.py\n"
                "├── core/\n"
                "│   ├── engine.py\n"
                "│   └── memory.py\n"
                "├── ui/\n"
                "│   └── components.py\n"
                "├── requirements.txt\n"
                "└── README.md"
            ),
            "extra_notes": "Mention that Ollama must be installed locally.",
            **{key: True for key, _ in SECTION_OPTIONS},
        }
    )

    st.rerun()


# ============================================================
# PROJECT FORM
# ============================================================

with st.container(border=True):

    st.markdown('<div class="section-title">📝 Project Details</div>', unsafe_allow_html=True)

    col_name, col_repo = st.columns(2)

    with col_name:
        project_name = st.text_input(
            "Project name",
            placeholder="e.g. NeuraChat",
            key="project_name",
        )

    with col_repo:
        repo_url = st.text_input(
            "GitHub URL (optional)",
            placeholder="https://github.com/user/repo",
            key="repo_url",
        )

    tagline = st.text_input(
        "One-line tagline",
        placeholder="A short, catchy summary of your project",
        key="tagline",
    )

    description = st.text_area(
        "What does it do?",
        placeholder=(
            "Describe your project in a few sentences:\n"
            "what problem it solves, how it works, who it's for..."
        ),
        height=110,
        key="description",
    )

    col_stack, col_type, col_style = st.columns([2, 1, 1])

    with col_stack:
        stack = st.multiselect(
            "Tech stack",
            STACKS,
            key="stack_multi",
        )

    with col_type:
        project_type = st.selectbox(
            "Project type",
            PROJECT_TYPES,
            key="project_type",
        )

    with col_style:
        style = st.selectbox(
            "Detail level",
            DETAIL_STYLES,
            key="detail_style",
        )

    features = st.text_area(
        "Key features (one per line)",
        placeholder="Fast\nPrivacy-first\nEasy setup",
        height=100,
        key="features",
    )

    col_license, col_author = st.columns(2)

    with col_license:
        license_name = st.selectbox(
            "License",
            LICENSES,
            key="license_sel",
        )

    with col_author:
        author = st.text_input(
            "Author (optional)",
            placeholder="Your name or org",
            key="author",
        )

    with st.expander("🗂️ Advanced (optional)"):

        file_tree = st.text_area(
            "Project file structure",
            placeholder=(
                "myapp/\n"
                "├── main.py\n"
                "├── utils/\n"
                "└── requirements.txt"
            ),
            height=130,
            key="file_tree",
        )

        extra_notes = st.text_area(
            "Extra notes for the AI",
            placeholder="Anything specific to mention or emphasize...",
            key="extra_notes",
        )


# ============================================================
# SECTION PICKER
# ============================================================

st.markdown('<div class="section-title">🧩 Sections to include</div>', unsafe_allow_html=True)

section_cols = st.columns(4)

for index, (key, label) in enumerate(SECTION_OPTIONS):

    with section_cols[index % 4]:
        st.checkbox(label, value=True, key=key)


# ============================================================
# GENERATE
# ============================================================

st.write("")

generate_clicked = st.button(
    "✨  Generate README",
    type="primary",
    use_container_width=True,
)


if generate_clicked:

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    if not project_name.strip():
        st.warning("📝 Please enter a project name.")
        st.stop()

    if not description.strip():
        st.warning(
            "📝 Please add a short description so the AI "
            "knows what to write about."
        )
        st.stop()

    if not api_key.strip():
        st.warning("🔑 Please enter your DeepSeek API key in the sidebar.")
        st.stop()

    # --------------------------------------------------------
    # Collect selected sections
    # --------------------------------------------------------

    selected_sections = [
        SECTION_PROMPTS[key]
        for key, _ in SECTION_OPTIONS
        if st.session_state.get(key)
    ]

    if not selected_sections:
        selected_sections = [
            "Features list",
            "Installation steps",
            "Usage with code blocks",
        ]

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    try:

        with st.spinner("✍️ ReadMe Forge is writing your documentation..."):

            result = generate_readme(
                project_name=project_name.strip(),
                tagline=tagline.strip(),
                description=description.strip(),
                repo_url=repo_url.strip(),
                project_type=project_type,
                stack=stack,
                features=features.strip(),
                author=author.strip(),
                license_name=license_name,
                file_tree=file_tree.strip(),
                extra_notes=extra_notes.strip(),
                sections=selected_sections,
                style=style,
                model_name=model,
                api_key=api_key,
            )

        st.session_state.readme = result

        st.session_state.history.insert(
            0,
            {
                "name": project_name.strip(),
                "type": project_type,
                "readme": result,
            },
        )

        st.session_state.history = st.session_state.history[:10]

        st.toast("README generated!", icon="📖")

    except Exception as error:

        st.error(f"❌ Generation failed: {error}")


# ============================================================
# OUTPUT
# ============================================================

if st.session_state.readme:

    st.divider()

    st.markdown('<div class="section-title">📄 Your README is ready</div>', unsafe_allow_html=True)

    readme_md = st.session_state.readme

    st.caption(
        f"📊 {len(readme_md.splitlines())} lines · "
        f"{len(readme_md.split())} words · "
        f"{len(readme_md)} characters"
    )

    tab_preview, tab_source = st.tabs(["👁 Preview", "📝 Markdown Source"])

    with tab_preview:
        st.markdown(readme_md, unsafe_allow_html=True)

    with tab_source:
        st.code(readme_md, language="markdown")

    action_left, action_right, _ = st.columns([1, 1, 2])

    with action_left:
        st.download_button(
            "⬇️  Download README.md",
            data=readme_md,
            file_name="README.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with action_right:
        render_copy_button(readme_md)


# ============================================================
# HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.markdown('<div class="section-title">🕘 Recently generated</div>', unsafe_allow_html=True)

    for index, item in enumerate(st.session_state.history):

        with st.expander(f"{item['name']} — {item['type']}"):

            st.code(item["readme"], language="markdown")

            st.download_button(
                "⬇️ Download",
                data=item["readme"],
                file_name=f"{item['name']}_README.md",
                mime="text/markdown",
                key=f"hist_dl_{index}",
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption("📖 ReadMe Forge • AI README Generator • DeepSeek + LangChain")