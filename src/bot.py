import os
import json
from langchain_together import ChatTogether
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# Charger les prompts à partir du fichier JSON
def load_prompts(file_path="data/prompts.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# Initialize the Together AI model
llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    api_key=os.getenv("TOGETHER_API_KEY"),
    temperature=0.7,
    max_tokens=200
)

# Utiliser SQL pour l'historique des conversations
def get_chat_history(session_id):
    return SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///conversation_history.db"
    )

# Charger les prompts
prompts = load_prompts()

# Classe pour le ChatBot
class ChatBot:
    def __init__(self, scenario, learning_language="fr"):
        self.scenario = scenario
        self.learning_language = learning_language
        self.bot_prompt = prompts[scenario]["bot_prompt"][learning_language]
        self.professor_prompt = prompts[scenario]["professor_prompt"][learning_language]

        # Créer les templates de prompt
        bot_template = ChatPromptTemplate.from_messages([
            ("system", self.bot_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        professor_template = ChatPromptTemplate.from_messages([
            ("system", self.professor_prompt),
            ("human", "{input}")
        ])

        # Créer les chaînes
        self.chain = bot_template | llm
        self.professor_chain = professor_template | llm

        # Configurer l'historique des messages pour la chaîne
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
        # Utiliser le professeur pour corriger
        response = self.professor_chain.invoke({"input": user_message})
        return response.content
    
    def generate_prompt(self, user_message):
    # Create the full prompt using the user message
        return f"{self.bot_prompt}\nUser: {user_message}"

    @staticmethod
    def get_available_scenarios():
        return list(prompts.keys())