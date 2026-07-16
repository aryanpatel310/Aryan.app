import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Story Generator")
st.title("AI Story Generator")
st.write("Generate stories based on your prompts")

@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="gpt2"
    )
generator = load_model()

topic = st.text_input(
    "story topic",
    placeholder="A dragon that loves pizza"
)

genre = st.selectbox(
    "Select Genre",
    [
        "adventure",
        "fantasy",
        "sci-fi",
        "mystery",
        "comedy",
        "horror",
    ]
)

length = st.slider(
    "Select Story Length",
    100,
    400,
    200,
    step=50
)

if st.button("Generate Story"):

    if topic.strip() == "":
        st.warning("Please enter a story topic.")
        st.stop()
    
    prompt = f"""
Title: {topic}
Genre: {genre}

story:
Once upon a time,
"""
    
    with st.spinner("Generating story..."):
        result = generator(
            prompt,
            max_new_tokens=length,
            temperature=0.9,
            do_sample=True,
            top_p=0.95,
            repetition_penalty=1.2,
            pad_token_id=50256,
        )

    story = result[0]["generated_text"]

    story = story.replace(prompt, "").strip()
    st.subheader("Generated Story")
    st.write(story)

