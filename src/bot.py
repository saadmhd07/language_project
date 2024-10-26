import os
from langchain_together import ChatTogether
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

# Initialize the Together AI model
llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    api_key=os.getenv("TOGETHER_API_KEY"),
    temperature=0.7,
    max_tokens=200
)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly and helpful student at the Universidad de Chile. Your name is Sofía. You help new students get familiar with the campus and engage in friendly conversation. Speak in a casual, friendly Spanish. Have a natural conversation, your sentences shouldn't be too long."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Define the "professor" prompt for correcting mistakes
professor_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a spanish language teacher. Read the following student input. if there is any error, explain it briefly. Be concise."),
    ("human", "{input}")
])

# Use SQL-based chat message history to store messages in a database file
def get_chat_history(session_id):
    return SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///conversation_history.db"
    )

# Combine prompt and model into a chain
chain = prompt | llm
professor_chain = professor_prompt | llm

# Use `RunnableWithMessageHistory` to automatically manage message history
chain_with_message_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# Define a class to interface with the chatbot
class ChatBot:
    def get_response(self, user_message, session_id="default_session"):
        config = {"configurable": {"session_id": session_id}}
        response = chain_with_message_history.invoke({"input": user_message}, config=config)
        return response.content

    def correct_errors(self, user_message):
        # Directly use the professor chain to correct the input
        response = professor_chain.invoke({"input": user_message})
        return response.content