from flask import Blueprint, request, jsonify, render_template
from app.services import generate_answer
from app.backend import MongoDb
import os
api_bp = Blueprint("api", __name__)

def register_routes(app):
    app.register_blueprint(api_bp)

@api_bp.route("/")
def home():
    render_template("index.html")
    return "Hello, World!"
@api_bp.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    retrieved_text = MongoDb.get_search_result(question)
    answer = generate_answer(question, retrieved_text)

    return jsonify({"question": question, "retrieved_text": retrieved_text, "answer": answer})
