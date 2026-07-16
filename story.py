import streamlit as st

from local_ai import build_story_text


def build_fallback_story(topic: str, genre: str, length: int) -> str:
    return build_story_text(topic, genre, length)


def render_story_ui():
    st.header("AI Story Generator")
    st.write("Generate stories based on your prompts")

    topic = st.text_input(
        "story topic",
        placeholder="A dragon that loves pizza",
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
        ],
    )

    length = st.slider("Select Story Length", 100, 400, 200, step=50)

    if st.button("Generate Story"):
        if topic.strip() == "":
            st.warning("Please enter a story topic.")
            st.stop()

        with st.spinner("Generating story..."):
            story = build_fallback_story(topic, genre, length)
            st.info("Using the built-in local story generator for this environment.")

        st.subheader("Generated Story")
        st.write(story)


def render_story_app():
    st.set_page_config(page_title="AI Story Generator", layout="wide")
    st.title("AI Story Generator")
    st.write("Generate stories based on your prompts")
    render_story_ui()


if __name__ == "__main__":
    render_story_app()

