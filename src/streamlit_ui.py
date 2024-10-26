import streamlit as st
from bot import ChatBot
import uuid

# Initialize the chatbot instance
bot = ChatBot()

# Streamlit Interface
st.title("Simulation de discussion à l'Universidad de Chile avec Correcteur")
st.write("Vous venez d'arriver à l'Université de Chile. Interpellez un étudiant chilien et commencez une conversation. Sur le côté, un professeur corrigera vos phrases.")

# Text input field for user messages
user_input = st.text_input("Votre message:", key="user_input", on_change=None)

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
    # Get response from the bot
    bot_response = bot.get_response(user_input, session_id=st.session_state["session_id"])
    
    # Get corrections from the professor bot
    correction = bot.correct_errors(user_input)
    
    # Save conversation and correction to session state
    st.session_state["conversation"].append({"role": "user", "content": user_input})
    st.session_state["conversation"].append({"role": "assistant", "content": bot_response})
    st.session_state["corrections"].append({"user_message": user_input, "correction": correction})


# Main conversation in the left column
with col1:
    st.subheader("Conversation avec Sofía")
    for message in st.session_state["conversation"]:
        if message["role"] == "user":
            st.markdown(f'<div style="text-align: left; color: blue;"><strong>😃 Vous:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f'<div style="text-align: right; color: green;"><strong>🤖 Sofía:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Professor corrections in the right column
with col2:
    st.subheader("Corrections du Professeur")
    for correction in st.session_state["corrections"]:
        st.markdown(f"**Votre phrase :** {correction['user_message']}")
        st.markdown(f"**Correction :** {correction['correction']}")