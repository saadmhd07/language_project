import os
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
import json

# Charger les variables d'environnement depuis .env
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Charger les prompts à partir du fichier JSON
def load_prompts(file_path="data/prompts.json"):
    with open(file_path, "r") as file:
        return json.load(file)

prompts = load_prompts()

print("TOGETHER_API_KEY:", TOGETHER_API_KEY)

# Initialisation du modèle IA avec Together AI
llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    api_key=TOGETHER_API_KEY,
    temperature=0.7,
    max_tokens=200
)

# Fonction pour gérer l'historique des conversations
def get_chat_history(session_id):
    return SQLChatMessageHistory(
        session_id=session_id, 
        connection_string="sqlite:///conversation_history.db"
    )

# Classe du chatbot pour gérer les interactions
class ChatBot:
    def __init__(self, scenario, learning_language="fr"):
        if scenario not in prompts:
            raise ValueError(f"Scénario '{scenario}' non trouvé. Scénarios disponibles : {list(prompts.keys())}")

        self.scenario = scenario
        
        if learning_language not in prompts[scenario]["bot_prompt"]:
            raise ValueError(f"Langue '{learning_language}' non supportée pour ce scénario")
        
        self.bot_prompt = prompts[scenario]["bot_prompt"].get(learning_language, "Langue non prise en charge")
        self.professor_prompt = prompts[scenario]["professor_prompt"].get(learning_language, "Langue non prise en charge")

        # Templates des messages pour le bot et le professeur
        bot_template = ChatPromptTemplate.from_messages([
            ("system", self.bot_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        professor_template = ChatPromptTemplate.from_messages([
            ("system", self.professor_prompt),
            ("human", "{input}")
        ])

        # Initialisation des chaînes de conversation
        self.chain = bot_template | llm
        self.professor_chain = professor_template | llm

        # Gestion de l'historique des messages
        self.chain_with_message_history = RunnableWithMessageHistory(
            self.chain,
            get_chat_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )

    def get_response(self, user_message, session_id="default_session"):
        config = {"configurable": {"session_id": session_id}}
        response = self.chain_with_message_history.invoke({"input": user_message}, config=config)
        return response.content

    def correct_errors(self, user_message):
        response = self.professor_chain.invoke({"input": user_message})
        return response.content
    
    def generate_prompt(self, user_message):
        return f"{self.bot_prompt}\nUser: {user_message}"

    @staticmethod
    def get_available_scenarios():
        return list(prompts.keys())