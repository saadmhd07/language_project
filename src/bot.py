import os
import sqlite3
from langchain_together import ChatTogether
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Initialize the chatbot with LangChain and SQLite for memory
class ChatBot:
    def __init__(self):
        # Initialize the TogetherAI LLM with LangChain's memory
        self.llm = ChatTogether(
            model="meta-llama/Llama-3-8b-chat-hf",  # You can change the model if needed
            api_key=os.getenv("TOGETHER_API_KEY"),
            temperature=0.7,
            max_tokens=200
        )

        # Initialize conversation memory
        self.memory = ConversationBufferMemory(return_messages=True)

        # Create a conversation chain with memory
        self.conversation_chain = ConversationChain(llm=self.llm, memory=self.memory)

        # Set up the SQLite database to store conversation history
        self.db_conn = sqlite3.connect('conversation_history.db')
        self.create_table()

    def create_table(self):
        # Create a table to store conversation history
        query = """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
        """
        self.db_conn.execute(query)
        self.db_conn.commit()

    def save_to_db(self, user_message, bot_response):
        # Save the conversation to the SQLite database
        query = "INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)"
        self.db_conn.execute(query, (user_message, bot_response))
        self.db_conn.commit()

    def get_response(self, user_message):
        # Get the bot response using LangChain's conversation chain
        bot_response = self.conversation_chain.run(input=user_message)

        # Save conversation to SQLite
        self.save_to_db(user_message, bot_response)

        return bot_response

    def close(self):
        # Close the SQLite connection
        self.db_conn.close()