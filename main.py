
from flask import Flask, jsonify, request
from flask_cors import CORS

from db_connect import db
from scripts.bert_implementation.similarity import similarity
from scripts.preprocessing.preprocessing import preprocess

app = Flask(__name__)
CORS(app)

issues = db.issues


@app.route("/api/v1/issues/create", methods=['POST'])
def create_issues():
    issue = request.get_json()
    issue["tokens"] = list(set((preprocess(issue["title"]) + " " + preprocess(issue["description"])).split()))
    issues.insert_one(issue)

    return '', 204


@app.route("/api/v1/issues/read", methods=['POST'])
def read_issues():
    query = request.get_json()
    query = query["title"] + " " + query["description"]
    query_tokens = preprocess(query).split()
    query_tokens = [token for token in query_tokens if len(token) > 4]
    results = issues.find({"tokens": {"$in": query_tokens}}, {"_id": 0})

    response = []
    for result in results:
        sent = result["title"] + " " + result["description"]
        label, prob = similarity(query, sent)
        if (label == "entailment" or label == "neutral") and prob > 0.5:
            result["similarity"] = str(prob)
            response.append(result)

    return jsonify(response)
