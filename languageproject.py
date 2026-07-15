import streamlit as st
from transformers import pipeline
st.set.page_config(page_title="AI Language Translator")

st.title("AI language translator")
st.write("translates english into different languages")
@st.cache_resource
def load_model():
    return pipeline(
        "translation",
        model="helsinki-NLP/opus-mt-en-fr"
    )
translator = load_model()

languages = {
    "French":"Helsinki-NLP/opus-mt-en-fr",
    "German":"Helsinki-NLP/opus-mt-en-de",
    "Spanish":"Helsinki-NLP/opus-mt-en-es",
    "Italian":"Helsinki-NLP.opus-me-en-it",
}

language = st.selectbox(
    "Select Language",
    list(languages.keys())
)

text = st.text_area("Enter text here")
if st.button("translate"):

    with st.spinner("Loading model..."):

        translator = pipeline(
            "translation",
            model=languages[language]
        )

        result = translator(text)

        st.success(result[0]["translation_text"])
