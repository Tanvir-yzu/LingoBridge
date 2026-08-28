import json

import streamlit as st
import streamlit.components.v1 as components

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LingoBridge",
    page_icon="🌍",
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
            radial-gradient(ellipse 80% 50% at 15% -10%, rgba(99,102,241,0.20), transparent 60%),
            radial-gradient(ellipse 60% 50% at 90% 5%, rgba(168,85,247,0.16), transparent 60%),
            radial-gradient(ellipse 70% 60% at 50% 110%, rgba(6,182,212,0.12), transparent 60%),
            #0b0e17;
        color: #e8ecf4;
        font-family: 'Plus Jakarta Sans', ui-sans-serif, sans-serif;
        color-scheme: dark;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #22d3ee);
        z-index: 999;
    }

    .block-container {
        padding: 2rem 1rem 4rem;
        max-width: 1150px;
        margin: 0 auto;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    ::selection {
        background: rgba(99,102,241,0.45);
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.14);
        border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.25);
    }

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
        margin-bottom: 26px;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 16px;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        color: #9aa3b8;
        font-size: 12.5px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 54px;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin: 0 0 10px 0;
        background: linear-gradient(90deg, #818cf8, #c084fc, #22d3ee, #818cf8);
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
        background: rgba(99,102,241,0.10);
        border: 1px solid rgba(99,102,241,0.28);
        color: #a5b4fc;
        font-size: 12.5px;
        font-weight: 600;
    }

    /* ---------- LABELS ---------- */

    [data-testid="stWidgetLabel"] p {
        color: #9aa3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* ---------- INPUT / TEXTAREA ---------- */

    .stTextArea textarea,
    [data-testid="stTextArea"] textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 16px !important;
        color: #eef1f8 !important;
        caret-color: #a5b4fc;
        padding: 18px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: border-color .25s ease, box-shadow .25s ease;
    }

    .stTextArea textarea:focus {
        border-color: rgba(99,102,241,0.65) !important;
        box-shadow: 0 0 0 4px rgba(99,102,241,0.14) !important;
    }

    .stTextArea textarea::placeholder {
        color: #5b6478 !important;
    }

    [data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        color: #eef1f8 !important;
    }

    /* ---------- SELECTBOX ---------- */

    [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        min-height: 46px;
        color: #eef1f8 !important;
        transition: border-color .2s ease;
    }

    [data-baseweb="select"] > div:hover {
        border-color: rgba(99,102,241,0.5) !important;
    }

    [data-baseweb="popover"] {
        background: #161a2b !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    [data-baseweb="popover"] [role="option"] {
        color: #e8ecf4 !important;
    }

    [data-baseweb="popover"] [role="option"]:hover {
        background: rgba(99,102,241,0.16) !important;
    }

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
        border-color: rgba(99,102,241,0.6);
        background: rgba(99,102,241,0.10);
        transform: translateY(-1px);
    }

    button[kind="primary"],
    [data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #6366f1, #a855f7) !important;
        border: none !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        height: 54px;
        border-radius: 15px !important;
        box-shadow: 0 8px 26px rgba(99,102,241,0.38);
        transition: all .25s ease;
    }

    button[kind="primary"]:hover,
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px);
        filter: brightness(1.12);
        box-shadow: 0 14px 34px rgba(99,102,241,0.5);
    }

    /* ---------- PANELS ---------- */

    .panel-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 10px;
        color: #eef1f8;
    }

    .panel-chip {
        font-size: 11px;
        font-weight: 600;
        color: #a5b4fc;
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(99,102,241,0.3);
        padding: 2px 9px;
        border-radius: 999px;
    }

    .arrow-circle {
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-size: 20px;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(99,102,241,0.45);
        margin: 85px auto 0 auto;
    }

    .output-card {
        background: linear-gradient(180deg, rgba(99,102,241,0.08), rgba(168,85,247,0.05));
        border: 1px solid rgba(99,102,241,0.28);
        border-radius: 16px;
        padding: 20px;
        min-height: 190px;
        max-height: 320px;
        overflow-y: auto;
        font-size: 15.5px;
        line-height: 1.7;
        white-space: pre-wrap;
        color: #eef1f8;
        animation: rise 0.45s ease both;
    }

    .empty-card {
        border: 1.5px dashed rgba(255,255,255,0.14);
        border-radius: 16px;
        min-height: 190px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 8px;
        color: #7d8598;
        text-align: center;
    }

    .empty-icon { font-size: 34px; opacity: 0.8; }
    .empty-title { font-weight: 700; font-size: 14.5px; color: #9aa3b8; }
    .empty-sub { font-size: 12.5px; }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: rgba(13,17,28,0.88);
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
        background: linear-gradient(135deg, #6366f1, #a855f7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 8px 20px rgba(99,102,241,0.35);
    }

    .side-name { font-weight: 800; font-size: 17px; color: #f1f3f9; }
    .side-tag  { font-size: 11.5px; color: #7d8598; margin-top: 1px; }

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

    .feat { font-size: 13px; color: #aab1c4; padding: 3px 0; }

    .status {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        font-weight: 600;
        color: #c7cdd9;
        margin-top: 10px;
    }

    .dot {
        width: 8px; height: 8px; border-radius: 50%;
        display: inline-block;
    }
    .dot-green { background: #34d399; box-shadow: 0 0 8px #34d399; }
    .dot-amber { background: #fbbf24; box-shadow: 0 0 8px #fbbf24; }

    /* ---------- MISC ---------- */

    hr, [data-testid="stDivider"] {
        border: none !important;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stExpander"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        overflow: hidden;
        transition: border-color .2s ease;
    }

    [data-testid="stExpander"]:hover {
        border-color: rgba(99,102,241,0.4) !important;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600;
    }

    [data-testid="stCaptionContainer"], .stCaption {
        color: #7d8598 !important;
    }

    @media (max-width: 768px) {
        .hero-title { font-size: 36px; }
        .arrow-circle { display: none; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "translation" not in st.session_state:
    st.session_state.translation = ""

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# LANGUAGES & EXAMPLES
# ============================================================

LANGUAGES = {
    "🇬🇧 English": "English",
    "🇧🇩 Bangla": "Bangla",
    "🇨🇳 Chinese": "Chinese",
    "🇯🇵 Japanese": "Japanese",
    "🇰🇷 Korean": "Korean",
    "🇮🇳 Hindi": "Hindi",
    "🇫🇷 French": "French",
    "🇩🇪 German": "German",
    "🇪🇸 Spanish": "Spanish",
    "🇸🇦 Arabic": "Arabic",
    "🇮🇹 Italian": "Italian",
    "🇷🇺 Russian": "Russian",
}

EXAMPLES = [
    "apni camon acen",
    "ami valo asi, tumi koi aso",
    "Where can I find good street food nearby?",
]


# ============================================================
# HELPER — COPY BUTTON (client-side, in its own iframe)
# ============================================================

def render_copy_button(text: str) -> None:

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
              color:#e8ecf4; border-radius:10px;
              padding:8px 18px; font-size:13.5px; font-weight:600;
              cursor:pointer; font-family:'Plus Jakarta Sans',sans-serif;
              transition:all .2s ease;"
            onmouseover="this.style.borderColor='rgba(99,102,241,0.7)'"
            onmouseout="this.style.borderColor='rgba(255,255,255,0.16)'">
            📋 Copy translation
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
              setTimeout(() => {{ btn.innerHTML = '📋 Copy translation'; }}, 1600);
            }});
          </script>
        </body>
        </html>
        """,
        height=48,
        scrolling=False,
    )


# ============================================================
# TRANSLATION FUNCTION
# ============================================================

def translate_text(
    text: str,
    target_language: str,
    tone: str,
    context: str,
    model_name: str,
    api_key: str,
) -> str:

    """
    Translate user text using DeepSeek through LangChain.
    """

    if not api_key:
        raise ValueError("DeepSeek API key is missing.")

    api_key = api_key.strip()

    if not api_key:
        raise ValueError("DeepSeek API key is empty.")

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://api.deepseek.com",
        temperature=0,
    )

    # --------------------------------------------------------
    # Build system prompt (with pinyin for Chinese)
    # --------------------------------------------------------

    chinese_pinyin_section = ""
    chinese_pinyin_rules = ""
    if target_language == "Chinese":
        chinese_pinyin_section = """
==================================================
PINYIN REQUIREMENT (Chinese ONLY)
==================================================

When translating to Chinese, you MUST include
pinyin pronunciation in parentheses immediately
after each sentence or paragraph.

Format:
  中文汉字 (pīnyīn fā yīn)

Example:
  你好吗？我很好。
  (nǐ hǎo ma? wǒ hěn hǎo.)

Important:
- Place pinyin AFTER the Chinese characters,
  on a new line in parentheses.
- Use proper tone marks in pinyin.
- Do NOT include pinyin for any other language.
"""
        chinese_pinyin_rules = """
15. When translating to Chinese, ALWAYS include
    pinyin pronunciation in parentheses after
    the Chinese text, on a separate line.
"""

    system_prompt = f"""
You are LingoBridge, a professional
multilingual translation assistant.

Your job is to understand the user's
intended meaning and translate it naturally.

The user may write in:

- English
- Bangla
- Banglish
- Phonetic Bangla
- Chinese
- Japanese
- Korean
- Hindi
- Mixed languages
- Informal internet language

==================================================
BANGLISH UNDERSTANDING
==================================================

Banglish means Bangla written using English
or Roman characters.

Examples:

"apni camon acen"
means:
"আপনি কেমন আছেন?"

"apni kemon achen"
means:
"আপনি কেমন আছেন?"

"ami valo asi"
means:
"আমি ভালো আছি"

"ami bhalo achi"
means:
"আমি ভালো আছি"

"tumi koi aso"
means:
"তুমি কোথায় আছো?"

"ajke ki korba"
means:
"আজকে কি করবে?"

"amar sathe kotha bolo"
means:
"আমার সাথে কথা বলো"

Understand common spelling variations.
{chinese_pinyin_section}
==================================================
TRANSLATION SETTINGS
==================================================

Target language:
{{target_language}}

Tone:
{{tone}}

Context:
{{context}}

==================================================
IMPORTANT RULES
==================================================

1. Understand the intended meaning first.

2. If the input is Banglish, mentally convert
   it into the intended Bangla meaning before
   translating.

3. Correct obvious phonetic spelling variations.

4. Translate naturally rather than word-by-word.

5. Preserve the original meaning.

6. Preserve the requested tone.

7. Consider the requested context.

8. Do not explain your reasoning.

9. Do not explain the translation.

10. Return ONLY the final translated text.

11. Do not mention that the input was Banglish.

12. Do not add unnecessary quotation marks.

13. Preserve paragraphs when the input has
    multiple paragraphs.

14. Do not add information that was not
    present in the original text.
{chinese_pinyin_rules}
==================================================
"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                "{text}",
            ),
        ]
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "text": text,
            "target_language": target_language,
            "tone": tone,
            "context": context,
        }
    )

    result = response.content

    if isinstance(result, list):
        result = "".join(str(item) for item in result)

    result = str(result).strip()

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
            <div class="side-logo">🌍</div>
            <div>
                <div class="side-name">LingoBridge</div>
                <div class="side-tag">Multilingual AI Translator</div>
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

    st.markdown('<div class="side-card-title">🔑 DeepSeek API Key</div>',
                unsafe_allow_html=True)

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-...",
        label_visibility="collapsed",
        help="Enter your DeepSeek API key.",
    )

    if api_key:
        st.markdown(
            '<div class="status"><span class="dot dot-green"></span> Ready to translate</div>',
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
            <div class="side-card-title">✨ FEATURES</div>
            <div class="feat">✅ Banglish understanding</div>
            <div class="feat">✅ 12 target languages</div>
            <div class="feat">✅ Natural translation</div>
            <div class="feat">✅ Tone control</div>
            <div class="feat">✅ Context control</div>
            <div class="feat">✅ Translation history</div>
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
        <h1 class="hero-title">🌍 LingoBridge</h1>
        <p class="hero-sub">
            AI-powered multilingual translator with
            <b>Banglish</b> understanding
        </p>
        <div class="pills">
            <span class="pill">🗣️ Banglish AI</span>
            <span class="pill">🌐 12 Languages</span>
            <span class="pill">🎚️ Tone Control</span>
            <span class="pill">🎯 Context Aware</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONTROL BAR
# ============================================================

control_left, control_mid, control_right = st.columns(3)

with control_left:
    target_display = st.selectbox(
        "Translate to",
        list(LANGUAGES.keys()),
        index=2,
        key="target_lang",
    )

with control_mid:
    tone = st.selectbox(
        "Tone",
        ["Natural", "Casual", "Formal", "Professional", "Friendly"],
        index=0,
        key="tone",
    )

with control_right:
    context = st.selectbox(
        "Context",
        ["General", "Chat", "Business", "Education", "Travel", "Social Media"],
        index=0,
        key="context",
    )

target_language = LANGUAGES[target_display]


# ============================================================
# INPUT / OUTPUT PANELS
# ============================================================

st.write("")

left_col, arrow_col, right_col = st.columns([1, 0.09, 1])

with left_col:

    # Apply pending example text (set by the example chips below)
    # before the text_area widget is instantiated, so the widget
    # picks up the value on this rerun.
    if "_example" in st.session_state:
        st.session_state.input_text = st.session_state.pop("_example")

    st.markdown(
        """
        <div class="panel-title">
            📝 Original
            <span class="panel-chip">Auto-detect · EN / BN / Banglish</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    input_text = st.text_area(
        "Input text",
        key="input_text",
        placeholder=(
            "Type anything...\n\n"
            "Banglish works too:\n"
            "apni camon acen"
        ),
        height=190,
        label_visibility="collapsed",
    )

    current_text = st.session_state.get("input_text", "")

    if current_text:
        word_count = len(current_text.split())
        st.caption(f"📄 {word_count} words · {len(current_text)} characters")

with arrow_col:

    st.markdown('<div class="arrow-circle">→</div>', unsafe_allow_html=True)

with right_col:

    st.markdown(
        f"""
        <div class="panel-title">
            ✨ Translation
            <span class="panel-chip">{target_display}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.translation:

        import html as html_lib

        safe_output = html_lib.escape(st.session_state.translation)

        st.markdown(
            f'<div class="output-card">{safe_output}</div>',
            unsafe_allow_html=True,
        )

        render_copy_button(st.session_state.translation)

    else:

        st.markdown(
            """
            <div class="empty-card">
                <div class="empty-icon">✨</div>
                <div class="empty-title">Your translation appears here</div>
                <div class="empty-sub">Enter text and press Translate</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# TRANSLATE BUTTON
# ============================================================

st.write("")

translate_clicked = st.button(
    "🌐  Translate",
    type="primary",
    use_container_width=True,
)


if translate_clicked:

    if not input_text.strip():
        st.warning("📝 Please enter some text first.")
        st.stop()

    if not api_key.strip():
        st.warning("🔑 Please enter your DeepSeek API key in the sidebar.")
        st.stop()

    try:

        with st.spinner("🤖 DeepSeek is understanding and translating..."):

            result = translate_text(
                text=input_text,
                target_language=target_language,
                tone=tone,
                context=context,
                model_name=model,
                api_key=api_key,
            )

        st.session_state.translation = result

        st.session_state.history.insert(
            0,
            {
                "input": input_text,
                "target_display": target_display,
                "output": result,
            },
        )

        st.session_state.history = st.session_state.history[:10]

        st.toast("Translation complete!", icon="✅")
        st.rerun()

    except Exception as error:

        st.error(f"❌ Translation failed: {error}")


# ============================================================
# TRANSLATION HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.markdown(
        '<div class="panel-title">🕘 Recent Translations</div>',
        unsafe_allow_html=True,
    )

    for index, item in enumerate(st.session_state.history):

        preview = item["input"].replace("\n", " ")

        if len(preview) > 60:
            preview = preview[:60] + "..."

        with st.expander(f"{item['target_display']} — {preview}"):

            hist_left, hist_right = st.columns(2)

            with hist_left:
                st.markdown("**Input**")
                st.write(item["input"])

            with hist_right:
                st.markdown("**Translation**")
                st.write(item["output"])


# ============================================================
# EXAMPLE CHIPS
# ============================================================

st.divider()

st.markdown(
    '<div class="panel-title">💡 Try an example</div>',
    unsafe_allow_html=True,
)

chip_cols = st.columns(len(EXAMPLES))

for col, example in zip(chip_cols, EXAMPLES):

    with col:

        if col.button(example, key=f"chip_{example}", use_container_width=True):
            st.session_state._example = example
            st.session_state.translation = ""
            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption("🌍 LingoBridge • AI Multilingual Translator • Banglish-first by design")