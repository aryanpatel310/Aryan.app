from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define the function to extract and categorize intents and entities using OpenAI API
def extract_and_categorize(text):
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
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=150)
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("Intents and Entities Extraction with Categorization using GPT-3.5-turbo")
user_input = st.text_input("Enter your query:")

if user_input:
    result = extract_and_categorize(user_input)
    st.write("Extracted and Categorized Intents and Entities:")
    st.json(result)
