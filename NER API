from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy

# Load the custom NER model
try:
    nlp = spacy.load("custom_ner_model")
except Exception as e:
    raise Exception("Failed to load model: " + str(e))

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/')
def home():
    return "✅ NER API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"]
    doc = nlp(text)

    results = []
    for ent in doc.ents:
        results.append({
            "text": ent.text,
            "label": ent.label_
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Required for Render
