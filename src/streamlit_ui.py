import streamlit as st
from bot import ChatBot
import uuid

# Streamlit Interface
st.set_page_config(layout="wide")
st.title("Simulation de discussion à l'Universidad de Chile avec Correcteur")
st.write("Vous venez d'arriver à l'Université de Chile. Interpellez un étudiant chilien et commencez une conversation. Sur le côté, un professeur corrigera vos phrases.")

# Language selection for conversation
languages = {"Français": "fr", "English": "en", "Español": "es"}
selected_learning_language = st.selectbox("Choisissez la langue d'apprentissage:", list(languages.keys()))

# Scenario selection
scenarios = ChatBot.get_available_scenarios()
selected_scenario = st.selectbox("Choisissez un scénario:", scenarios)

# Initialize the chatbot instance with the selected scenario and learning language
if (
    "bot" not in st.session_state or 
    st.session_state["bot"].scenario != selected_scenario or 
    st.session_state["bot"].learning_language != languages[selected_learning_language]
):
    st.session_state["bot"] = ChatBot(
        selected_scenario, 
        learning_language=languages[selected_learning_language]
    )

bot = st.session_state["bot"]

# Text input field for user messages
user_input = st.text_input("Votre message (en langue d'apprentissage):", key="user_input", on_change=None)

# Generate a unique session ID for every new session
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# Initialize conversation history in Streamlit session state
if "conversation" not in st.session_state:
    st.session_state["conversation"] = []

# Initialize a list for professor corrections
if "corrections" not in st.session_state:
    st.session_state["corrections"] = []

# Layout: Main conversation and Professor side-by-side
col1, col2 = st.columns([3, 1])

# Handle user input
if st.button("Envoyer") and user_input:
    # Get response from the bot, considering the selected scenario
    bot_response = bot.get_response(user_message=user_input, session_id=st.session_state["session_id"])
    
    # Get corrections from the professor bot
    correction = bot.correct_errors(user_message=user_input)
    
    # Save conversation and correction to session state
    st.session_state["conversation"].append({"role": "user", "content": user_input})
    st.session_state["conversation"].append({"role": "assistant", "content": bot_response})
    st.session_state["corrections"].append({"user_message": user_input, "correction": correction})

# Main conversation in the left column
with col1:
    st.subheader("Conversation avec Sofía")
    chat_display = ""
    for message in st.session_state["conversation"]:
        if message["role"] == "user":
            chat_display += f'<div style="text-align: left; color: blue; padding: 5px; border-radius: 10px; background-color: #e0f7fa; margin-bottom: 10px;"><strong>😃 Vous:</strong> {message["content"]}</div>'
        elif message["role"] == "assistant":
            chat_display += f'<div style="text-align: right; color: green; padding: 5px; border-radius: 10px; background-color: #e8f5e9; margin-bottom: 10px;"><strong>🤖 Sofía:</strong> {message["content"]}</div>'
    st.markdown(chat_display, unsafe_allow_html=True)

# Professor corrections in the right column
with col2:
    st.subheader(f"Corrections du Professeur (en {selected_learning_language})")
    for idx, correction in enumerate(st.session_state["corrections"], 1):
        with st.expander(f"Correction {idx} - Votre phrase : {correction['user_message']}"):
            st.markdown(f"**Correction :** {correction['correction']}")