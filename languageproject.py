import streamlit as st
form transformers import pipeline
st.set.page_config(page_title="AI Language Translator", page_icon=🌎)

st.title("🌎 AI language translator")
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
    
)