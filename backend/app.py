from flask import Flask
from flask_cors import CORS
from api.routes import chatbot_routes

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes depuis d'autres domaines (utile pour le front-end)

# Enregistrement des routes définies dans routes.py
app.register_blueprint(chatbot_routes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)