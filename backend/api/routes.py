from flask import Blueprint, request, jsonify
from api.chatbot_service import ChatBot
from api.models import convert_audio_to_text, synthesize_text_to_speech

# Définition du Blueprint pour organiser les routes
chatbot_routes = Blueprint("chatbot", __name__)

import logging
from flask import request, jsonify
from api.chatbot_service import ChatBot

logging.basicConfig(level=logging.DEBUG)

@chatbot_routes.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        logging.debug(f"Requête reçue : {data}")
        
        if "language" not in data or "message" not in data:
            return jsonify({"error": "Données invalides"}), 400
        
        if not data or "message" not in data or "scenario" not in data:
            logging.error("Données invalides reçues")
            return jsonify({"error": "Données invalides"}), 400

        scenario = data["scenario"]
        language = data.get("language", "fr")
        user_message = data["message"]

        bot = ChatBot(scenario, language)
        response = bot.get_response(user_message)

        logging.debug(f"Réponse envoyée : {response}")
        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"Erreur lors du traitement de la requête : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500


@chatbot_routes.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "Aucun fichier audio envoyé"}), 400

    audio_file = request.files['audio']
    language = request.form.get('language', 'en')
    
    transcription = convert_audio_to_text(audio_file, language)
    
    return jsonify({"text": transcription})


@chatbot_routes.route('/synthesize', methods=['POST'])
def synthesize_audio():
    data = request.json
    text = data.get("text")
    language = data.get("language", "en")

    if not text:
        return jsonify({"error": "Aucun texte fourni"}), 400

    audio_path = synthesize_text_to_speech(text, language)
    return jsonify({"audio_path": audio_path})