import streamlit as st

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - optional dependency in deployed environments
    pipeline = None


@st.cache_resource
def load_model(model_name: str):
    if pipeline is None:
        return None
    try:
        return pipeline("translation", model=model_name)
    except Exception:
        return None


def build_fallback_translation(text: str, language: str) -> str:
    return f"[{language}] Translation unavailable in this environment. Entered text: {text}"


def render_language_app():
    st.set_page_config(page_title="AI Language Translator", layout="wide")
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
            st.stop()

        with st.spinner("Generating translation..."):
            translator = load_model(languages[language])
            if translator is None:
                result_text = build_fallback_translation(text, language)
                st.info("The translation model backend is unavailable in this environment, so a fallback message is shown instead.")
            else:
                try:
                    result = translator(text)
                    result_text = result[0]["translation_text"]
                except Exception:
                    result_text = build_fallback_translation(text, language)

        st.success(result_text)


if __name__ == "__main__":
    render_language_app()
