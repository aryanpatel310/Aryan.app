import json
from io import BytesIO

import requests
import streamlit as st

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency in deployed environments
    OpenAI = None

try:
    from gtts import gTTS
except Exception:  # pragma: no cover - optional dependency in deployed environments
    gTTS = None

from languageproject import render_language_app
from story import render_story_ui


st.set_page_config(page_title="Aryan's AI Apps", layout="wide")

st.title("🤖 Welcome to Aryan's AI Apps")
st.write("Explore different AI-powered applications built with Streamlit")

home_tab, weather_tab, intent_tab, story_tab, language_tab = st.tabs(
    ["Home", "🌤️ Weather Bot", "🗣️ Intent Extraction", "✍️ Story Generator", "🌐 Language Translator"]
)

with home_tab:
    st.header("Welcome!")
    st.write(
        """
        This is your main dashboard with access to multiple AI applications:

        - **Weather Bot**: Get weather information for any city with AI-powered advice
        - **Intent Extraction**: Extract and categorize intents and entities from text using GPT
        - **Story Generator**: Create a short story from a topic and genre
        - **Language Translator**: Translate English text into other languages

        Select a tab above to get started!

        For more information, visit [GitHub](https://github.com/aryanpatel310/Aryan.app)
        """
    )

with weather_tab:
    st.header("Weather Bot")
    st.write("Enter any city and get the weather + AI advice")

    def get_city(city):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        data = requests.get(url).json()
        if "results" in data:
            return data["results"][0]
        return None

    def get_weather(lat, lon):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&current=temperature_2m,wind_speed_10m"
            "&daily=precipitation_probability_max"
        )
        return requests.get(url).json()

    def advice(temp, rain):
        if temp > 30:
            return "it is a hot day. Drink water and stay cool."
        if temp < 10:
            return "it is a cold day. wear warm clothes"
        if rain > 50:
            return "rain is very likely today. Wear a rain jacket."
        return "Weather is normal. Enjoy the day."

    def speak(text):
        if gTTS is None:
            return None
        audio = BytesIO()
        tts = gTTS(text)
        tts.write_to_fp(audio)
        return audio

    city = st.text_input("Enter city:", "New York")

    if st.button("Check Weather"):
        place = get_city(city)

        if place:
            lat = place["latitude"]
            lon = place["longitude"]
            weather = get_weather(lat, lon)

            temp_c = weather["current"]["temperature_2m"]
            temp_f = round(temp_c * 9 / 5 + 32, 1)
            wind = weather["current"]["wind_speed_10m"]
            rain = weather["daily"]["precipitation_probability_max"][0]

            msg = advice(temp_c, rain)

            st.success(
                f"""
                {city}

                Temperature:
                {temp_c}°C || {temp_f}°F

                Wind:
                {wind} km/h

                Rain:
                {rain}%

                AI Advice:
                {msg}
                """
            )

            speech = f"""
            The temperature in {city} is {temp_c} degrees celsius or {temp_f} degrees fahrenheit.
            Rain probability is {rain}%.

            {msg}
            """

            audio = speak(speech)
            if audio is not None:
                st.audio(audio, format="audio/mp3")
            else:
                st.info("Audio playback is unavailable in this environment because gTTS is not installed.")
        else:
            st.error("City not found")

with intent_tab:
    st.header("Intent & Entity Extraction")
    st.write("Extract and categorize intents and entities from your text using GPT-3.5-turbo")

    if OpenAI is None:
        st.info("The OpenAI package is not available in this environment, so the app is using a built-in local fallback for intent extraction.")

    def extract_and_categorize(text):
        if OpenAI is None:
            cleaned = (text or "").strip()
            if not cleaned:
                return json.dumps({"intents": [], "entities": []})
            return json.dumps(
                {
                    "intents": [{"intent": "request_information", "category": "general"}],
                    "entities": [{"entity": cleaned, "category": "text_input"}],
                }
            )

        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        except Exception:
            cleaned = (text or "").strip()
            if not cleaned:
                return json.dumps({"intents": [], "entities": []})
            return json.dumps(
                {
                    "intents": [{"intent": "request_information", "category": "general"}],
                    "entities": [{"entity": cleaned, "category": "text_input"}],
                }
            )

        prompt = f"""
        Extract and categorize the intents and entities from the following text:

        Text: "{text}"

        Provide the result in the following JSON format:
        {{
            "intents": [
                {{"intent": "<intent>", "category": "<category>"}}
            ],
            "entities": [
                {{"entity": "<entity>", "category": "<category>"}}
            ]
        }}

        Make sure the categories are appropriate and relevant to the context.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            cleaned = (text or "").strip()
            if not cleaned:
                return json.dumps({"intents": [], "entities": []})
            return json.dumps(
                {
                    "intents": [{"intent": "request_information", "category": "general"}],
                    "entities": [{"entity": cleaned, "category": "text_input"}],
                }
            )

    user_input = st.text_input("Enter your query:")

    if user_input:
        result = extract_and_categorize(user_input)
        st.write("Extracted and Categorized Intents and Entities:")
        try:
            st.json(json.loads(result))
        except Exception:
            st.write(result)

with story_tab:
    render_story_ui()

with language_tab:
    render_language_app()

