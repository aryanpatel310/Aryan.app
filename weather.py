import streamlit as st
import requests
from gtts import gTTs
from io import BytesIO

st.set_page_config(
    page_title="AI Weather bot",
)

st.title("Weather Bot")
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
    elif temp < 10:
        return "it is a cold day. wear warm clothes"
    elif rain > 50:
        return "rain is very likely today. Wear a rain jacket."
    else:
        return "Weather is normal. Enjoy the day."
    
def speak(text):
    audio = BytesIO()

    tts = gTTS(text)

    tts.write_to_fp(audio)

    return audio

city = st.text_input(
    "Enter city:",
    "New York"
)

if st.button("Check Weather"):

    place = get_city(city)

    if place:

        lat = place["latitude"]
        lon = place["longitude"]
        
        weather = get_weather(
            lat,
            lon
        )

        temp_c = weather["current"]["temparature_2m"]

        temp_f = round(
            temp_c * 9/5 + 32,
            1
        )

        wind = weather["current"]["wind_speed_10m"]

        rain = weather["daily"]["precipitation_probability_mak"][0]


        msg = advice(
            temp_c
            rain
        )

        st.success(
            f"""
            {city}
            
            temperature:
            {temp_c} C || {temp_f} F

            Wind:
            {wind} km/h

            Rain:
            {rain}%

            AI advice:
            {msg}
            """
        )
speech = f"""
The temperature in {city} is {temp_c} degrees celsius or {temp_f} degrees fahrenheit.
Rain probability is {rain}%.

{msg}
"""

audio = speak(speech)

st.audio(
audio,
format="audio/mp3"
)

else:
    st.error("City not found")