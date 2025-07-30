import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Supported languages and codes for UI display
LANGUAGES = {
    "German": "de",
    "English": "en",
    "Greek": "el",
    "Spanish": "es",
    "French": "fr",
    "Italian": "it",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Dutch": "nl",
}

load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error(
        "Please set your OpenAI API key in the environment "
        "variable `OPENAI_API_KEY`."
    )
    st.stop()

client = OpenAI(api_key=openai_api_key)


def translate_with_openai(client, text, source_lang, target_lang):
    prompt = (
        f"Translate the following text from {source_lang} to "
        f"{target_lang}:\n\n"
        f"{text}\n\n"
        f"Translation:"
    )

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that translates text.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content.strip()


st.title("🦜 RealTime AI Translator 🌐")

st.markdown(
    "Translate text between 10 European languages using " "OpenAI GPT models."
)

col1, col2 = st.columns(2)
with col1:
    source_language = st.selectbox(
        "Source Language", list(LANGUAGES.keys()), index=1
    )  # default English
with col2:
    target_language = st.selectbox(
        "Target Language", list(LANGUAGES.keys()), index=0
    )  # default German

text_to_translate = st.text_area("Enter text to translate", height=150)

if st.button("Translate"):
    if not text_to_translate.strip():
        st.warning("Please enter some text to translate.")
    elif source_language == target_language:
        st.info(
            "Source and target languages are the same. "
            "No translation needed."
        )
        st.write(text_to_translate)
    else:
        with st.spinner("Translating..."):
            result = translate_with_openai(
                client=client,
                text=text_to_translate,
                source_lang=source_language,
                target_lang=target_language,
            )
            st.success("Translation:")
            st.write(result)
