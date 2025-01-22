import whisper
from gtts import gTTS
import os
import uuid

# Dossier où seront stockés les fichiers audio
AUDIO_FOLDER = "audio_conversations"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Charger le modèle Whisper pour la transcription
model = whisper.load_model("small")

def convert_audio_to_text(audio_file, language="en"):
    """
    Convertit un fichier audio en texte à l'aide de Whisper.
    
    :param audio_file: Fichier audio à transcrire (objet de type fichier).
    :param language: Langue de transcription (ex. "fr", "en", "es").
    :return: Texte transcrit.
    """
    audio_path = os.path.join(AUDIO_FOLDER, f"{uuid.uuid4()}_input.wav")

    # Enregistrer le fichier audio sur le disque
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())

    # Transcrire l'audio en texte
    result = model.transcribe(audio_path, language=language)
    return result['text']

def synthesize_text_to_speech(text, language="en"):
    """
    Génère un fichier audio à partir de texte en utilisant gTTS.
    
    :param text: Texte à convertir en audio.
    :param language: Langue de la synthèse vocale (ex. "fr", "en", "es").
    :return: Chemin du fichier audio généré.
    """
    audio_output_path = os.path.join(AUDIO_FOLDER, f"{uuid.uuid4()}_response.mp3")

    # Générer la synthèse vocale
    tts = gTTS(text=text, lang=language)
    tts.save(audio_output_path)

    return audio_output_path