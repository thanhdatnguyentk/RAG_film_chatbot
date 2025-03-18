from flask import Blueprint, request, jsonify, render_template
from app.services import generate_answer
from app.backend import MongoDb
import os
api_bp = Blueprint("api", __name__)

def register_routes(app):
    app.register_blueprint(api_bp)

@api_bp.route("/")
def home():
    #check path
    return render_template("index.html")

@api_bp.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    db = MongoDb()
    retrieved_text = db.get_search_result(query=question)
    answer = generate_answer(question, retrieved_text)

    return jsonify({"question": question, "retrieved_text": retrieved_text, "answer": answer})
