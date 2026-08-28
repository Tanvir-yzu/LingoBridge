import streamlit as st

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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 44px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 17px;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .feature-box {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.20);
        margin-top: 10px;
    }

    .example-box {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.20);
        margin-top: 10px;
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
# LANGUAGES
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


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌍 LingoBridge</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        AI-powered multilingual translator with Banglish understanding
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model = st.selectbox(
        "DeepSeek Model",
        [
            "deepseek-v4-flash",
            "deepseek-v4-pro",
        ],
        index=0,
    )

    # --------------------------------------------------------
    # Tone
    # --------------------------------------------------------

    tone = st.selectbox(
        "Translation Tone",
        [
            "Natural",
            "Casual",
            "Formal",
            "Professional",
            "Friendly",
        ],
        index=0,
    )

    # --------------------------------------------------------
    # Context
    # --------------------------------------------------------

    context = st.selectbox(
        "Context",
        [
            "General",
            "Chat",
            "Business",
            "Education",
            "Travel",
            "Social Media",
        ],
        index=0,
    )

    st.divider()

    # --------------------------------------------------------
    # API KEY
    # --------------------------------------------------------

    st.subheader("🔑 DeepSeek API Key")

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-...",
        help="Enter your DeepSeek API key.",
    )

    if api_key:
        st.success("API key entered.")

    else:
        st.warning(
            "Enter your DeepSeek API key to use the translator."
        )

    st.divider()

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    st.subheader("✨ Features")

    st.write("✅ Banglish understanding")
    st.write("✅ Multiple languages")
    st.write("✅ Natural translation")
    st.write("✅ Tone control")
    st.write("✅ Context control")

    st.divider()

    st.caption("Powered by DeepSeek + LangChain")


# ============================================================
# LANGUAGE SELECTION
# ============================================================

left_col, arrow_col, right_col = st.columns(
    [1, 0.15, 1]
)


with left_col:

    st.markdown(
        '<div class="section-title">📝 Your Text</div>',
        unsafe_allow_html=True,
    )


with arrow_col:

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:30px;
            margin-top:28px;
        ">
            →
        </div>
        """,
        unsafe_allow_html=True,
    )


with right_col:

    st.markdown(
        '<div class="section-title">🌐 Target Language</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# INPUT
# ============================================================

input_text = st.text_area(
    "Input text",
    placeholder=(
        "Example:\n"
        "apni camon acen\n\n"
        "or\n\n"
        "How are you?"
    ),
    height=230,
    label_visibility="collapsed",
)


# ============================================================
# TARGET LANGUAGE
# ============================================================

target_display = st.selectbox(
    "Select target language",
    list(LANGUAGES.keys()),
    index=2,
)

target_language = LANGUAGES[target_display]


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

    # --------------------------------------------------------
    # Validate API key
    # --------------------------------------------------------

    if not api_key:

        raise ValueError(
            "DeepSeek API key is missing."
        )

    api_key = api_key.strip()

    if not api_key:

        raise ValueError(
            "DeepSeek API key is empty."
        )

    # --------------------------------------------------------
    # DeepSeek LLM
    # --------------------------------------------------------

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url="https://api.deepseek.com",
        temperature=0,
    )

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
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

==================================================
TRANSLATION SETTINGS
==================================================

Target language:
{target_language}

Tone:
{tone}

Context:
{context}

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

==================================================
"""
            ),
            (
                "human",
                "{text}",
            ),
        ]
    )

    # --------------------------------------------------------
    # Chain
    # --------------------------------------------------------

    chain = prompt | llm

    # --------------------------------------------------------
    # Invoke
    # --------------------------------------------------------

    response = chain.invoke(
        {
            "text": text,
            "target_language": target_language,
            "tone": tone,
            "context": context,
        }
    )

    # --------------------------------------------------------
    # Extract content
    # --------------------------------------------------------

    result = response.content

    if isinstance(result, list):

        result = "".join(
            str(item)
            for item in result
        )

    result = str(result).strip()

    if not result:

        raise ValueError(
            "DeepSeek returned an empty response."
        )

    return result


# ============================================================
# TRANSLATE BUTTON
# ============================================================

st.write("")

translate_clicked = st.button(
    "🌐 Translate",
    type="primary",
    use_container_width=True,
)


if translate_clicked:

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not input_text.strip():

        st.warning(
            "📝 Please enter some text first."
        )

        st.stop()

    # --------------------------------------------------------
    # Validate API key
    # --------------------------------------------------------

    if not api_key.strip():

        st.warning(
            "🔑 Please enter your DeepSeek API key "
            "in the sidebar."
        )

        st.stop()

    # --------------------------------------------------------
    # Translate
    # --------------------------------------------------------

    try:

        with st.spinner(
            "🤖 DeepSeek is understanding and translating..."
        ):

            result = translate_text(
                text=input_text,
                target_language=target_language,
                tone=tone,
                context=context,
                model_name=model,
                api_key=api_key,
            )

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        st.session_state.translation = result

        # ----------------------------------------------------
        # History
        # ----------------------------------------------------

        st.session_state.history.insert(
            0,
            {
                "input": input_text,
                "target": target_language,
                "output": result,
            },
        )

        # Keep only latest 10
        st.session_state.history = (
            st.session_state.history[:10]
        )

    except Exception as error:

        st.error(
            f"❌ Translation failed: {error}"
        )


# ============================================================
# RESULT
# ============================================================

if st.session_state.translation:

    st.divider()

    st.subheader(
        f"✨ Translation — {target_display}"
    )

    st.text_area(
        "Translated text",
        value=st.session_state.translation,
        height=230,
    )

    st.success(
        "✅ Translation completed successfully."
    )

    # --------------------------------------------------------
    # Copy button
    # --------------------------------------------------------

    # Streamlit's text_area allows selecting/copying.
    # A dedicated JS copy button can be added later.


# ============================================================
# TRANSLATION HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader("🕘 Recent Translations")

    for index, item in enumerate(
        st.session_state.history
    ):

        preview = item["input"].replace(
            "\n",
            " ",
        )

        if len(preview) > 60:

            preview = preview[:60] + "..."

        with st.expander(
            f"{item['target']} — {preview}"
        ):

            st.markdown("**Input**")

            st.write(item["input"])

            st.markdown("**Translation**")

            st.write(item["output"])


# ============================================================
# EXAMPLE
# ============================================================

st.divider()

st.subheader("💡 Example")

example_left, example_right = st.columns(2)


with example_left:

    st.markdown(
        """
        **Input 🇧🇩**

        `apni camon acen`
        """
    )


with example_right:

    st.markdown(
        """
        **Chinese 🇨🇳**

        `你好吗？`
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "LingoBridge • AI Multilingual Translator"  
)