import os
import openai

# Initialisation du client Together avec compatibilité OpenAI
client = openai.OpenAI(
    api_key=os.environ.get("TOGETHER_API_KEY"),  # Assure-toi que ta clé API est définie
    base_url="https://api.together.xyz/v1",     # URL de l'API Together
)

def chat_with_bot():
    conversation = [
        {"role": "system", "content": "T'es un chatbot super desagreable"}
    ]

    print("Entrez 'quit' pour terminer la conversation.")
    
    while True:
        # Prendre l'entrée de l'utilisateur
        user_input = input("Vous: ")

        if user_input.lower() == "quit":
            print("Conversation terminée.")
            break

        # Ajouter la requête utilisateur à la conversation
        conversation.append({"role": "user", "content": user_input})

        # Faire une requête à l'API Together pour obtenir une réponse
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=conversation
        )

        # Récupérer et afficher la réponse du bot
        bot_response = response.choices[0].message.content  # Correction ici
        print(f"Bot: {bot_response}")

        # Ajouter la réponse du bot à la conversation
        conversation.append({"role": "assistant", "content": bot_response})

if __name__ == "__main__":
    chat_with_bot()