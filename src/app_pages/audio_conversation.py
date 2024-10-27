# audio_conversation.py

import streamlit as st
from st_audiorec import st_audiorec  # Import the audio recorder component
from gtts import gTTS
import os
import uuid
import whisper  # Import Whisper correctly from OpenAI's implementation
from bot import ChatBot

# Directory for storing audio files
AUDIO_FOLDER = "audio_conversations"
os.makedirs(AUDIO_FOLDER, exist_ok=True)  # Ensure the folder exists

# Load the Whisper model
model = whisper.load_model("base")  # Make sure this works after proper installation

def convert_audio_to_text_whisper(audio_path, language="en"):
    # Use Whisper to transcribe the audio and specify the language
    result = model.transcribe(audio_path, language=language)
    return result['text']

def audio_conversation():
    st.title("Conversation Naturelle Audio")
    st.write("Commencez à parler, et le chatbot vous répondra directement par audio.")

    # Language selection for conversation
    languages = {"🇫🇷 Français": "fr", "🇬🇧 English": "en", "🇪🇸 Español": "es"}
    selected_learning_language = st.selectbox("Choisissez la langue d'apprentissage:", list(languages.keys()))
    
    # **NEW: Select the language for Whisper transcription**
    transcription_language = st.selectbox("Choisissez la langue pour la transcription audio:", ["fr", "es", "en"])

    # Scenario selection (same as the chat page)
    scenarios = ChatBot.get_available_scenarios()
    selected_scenario = st.selectbox("Choisissez un scénario:", scenarios)

    # Initialize the chatbot with the selected scenario and learning language
    if (
        "bot_audio" not in st.session_state or 
        st.session_state["bot_audio"].scenario != selected_scenario or 
        st.session_state["bot_audio"].learning_language != languages[selected_learning_language]
    ):
        st.session_state["bot_audio"] = ChatBot(
            scenario=selected_scenario, 
            learning_language=languages[selected_learning_language]
        )

    bot = st.session_state["bot_audio"]

    # Audio Recorder Integration
    st.write("Enregistrez votre message en appuyant sur le bouton ci-dessous.")
    audio_bytes = st_audiorec()  # Use the audio recorder component

    if audio_bytes:
        # Save the recorded audio
        audio_input_path = os.path.join(AUDIO_FOLDER, f"{str(uuid.uuid4())}_input.wav")
        with open(audio_input_path, "wb") as f:
            f.write(audio_bytes)

        st.write("Audio enregistré, en cours de traitement...")

        # Convert recorded audio to text, specifying the language for Whisper
        user_text = convert_audio_to_text_whisper(audio_input_path, language=transcription_language)
        st.write(f"**Texte converti :** {user_text}")

        # Show the prompt that will be used by the bot
        llm_prompt = bot.generate_prompt(user_message=user_text)
        st.write("**Prompt envoyé au LLM :**")
        st.text_area("Prompt", llm_prompt, height=150)

        bot_response = bot.get_response(user_message=user_text)

        # Generate a response in audio format
        tts = gTTS(bot_response, lang=languages[selected_learning_language])
        audio_output_path = os.path.join(AUDIO_FOLDER, f"{str(uuid.uuid4())}_response.mp3")
        tts.save(audio_output_path)
        st.audio(audio_output_path)