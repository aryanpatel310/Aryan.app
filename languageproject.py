import streamlit as st

try:
    from deep_translator import GoogleTranslator
except Exception:  # pragma: no cover - optional dependency in deployed environments
    GoogleTranslator = None


def translate_text(text: str, language: str) -> str:
    cleaned_text = text.strip()
    if not cleaned_text:
        return ""

    language_map = {
        "French": "fr",
        "German": "de",
        "Spanish": "es",
        "Italian": "it",
    }

    target_lang = language_map.get(language, "en")
    if GoogleTranslator is None:
        return f"[{language}] {cleaned_text} -> {target_lang} (offline fallback)"

    try:
        return GoogleTranslator(source="en", target=target_lang).translate(cleaned_text)
    except Exception:
        return f"[{language}] {cleaned_text} -> {target_lang} (offline fallback)"


def build_fallback_translation(text: str, language: str) -> str:
    return translate_text(text, language)


def render_language_app():
    st.header("AI Language Translator")
    st.write("Translate English text into other languages")

    languages = {
        "French": "Helsinki-NLP/opus-mt-en-fr",
        "German": "Helsinki-NLP/opus-mt-en-de",
        "Spanish": "Helsinki-NLP/opus-mt-en-es",
        "Italian": "Helsinki-NLP/opus-mt-en-it",
    }

    language = st.selectbox("Select Language", list(languages.keys()))
    text = st.text_area("Enter text here")

    if st.button("Translate"):
        if not text.strip():
            st.warning("Please enter some text to translate.")
            return

        with st.spinner("Generating translation..."):
            result_text = build_fallback_translation(text, language)

        st.success(result_text)


if __name__ == "__main__":
    render_language_app()
