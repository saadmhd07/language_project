import openai
import os

class ChatBot:
    def __init__(self):
        # Initialiser le client API
        self.client = openai.OpenAI(
            api_key=os.getenv("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1"
        )
        # Conversation initiale avec le chatbot
        self.conversation = [{"role": "system", "content": "You are a helpful chatbot."}]

    def get_response(self, user_message):
        # Ajouter le message de l'utilisateur à la conversation
        self.conversation.append({"role": "user", "content": user_message})
        
        # Faire une requête à l'API pour obtenir la réponse du bot
        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=self.conversation
        )
        
        # Extraire la réponse et l'ajouter à la conversation
        bot_message = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": bot_message})
        
        return bot_message