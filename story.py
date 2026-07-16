import streamlit as st


def build_fallback_story(topic: str, genre: str, length: int) -> str:
    topic_text = topic.strip() or "a brave adventurer"
    paragraphs = [
        f"In the {genre} realm of {topic_text}, a curious traveler discovered a hidden path that shimmered beneath the moonlight.",
        "Every step along that path revealed a new surprise, from speaking lanterns to clocks that ran backward, until the traveler understood that destiny had been waiting all along.",
        "By dawn, the journey had changed the traveler forever, and the world felt brighter, stranger, and more magical than before.",
    ]

    story = "\n\n".join(paragraphs)
    if len(story) < length:
        story = story + "\n\n" + ("The adventure continued long after sunset, carrying hope, wonder, and a little bit of mischief into every new day. " * 2)
    return story[:length] + "..."


def render_story_app():
    st.set_page_config(page_title="AI Story Generator", layout="wide")
    st.title("AI Story Generator")
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
            st.info("The local AI model backend is unavailable in this environment, so a built-in story generator is being used instead.")

        st.subheader("Generated Story")
        st.write(story)


if __name__ == "__main__":
    render_story_app()

