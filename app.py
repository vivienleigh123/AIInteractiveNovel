from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import os
from langchain.memory import FileChatMessageHistory
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Constants
MODEL_A_URL = "http://localhost:11434/api/generate"
MODEL_B_URL = "http://localhost:11534/api/generate"
MEMORY_DIR = r"D:\Program Files\novel"
NOVEL_FILE = os.path.join(MEMORY_DIR, "novel.txt")

# Create directories if they don't exist
os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(os.path.join(MEMORY_DIR, "model_a_memory"), exist_ok=True)
os.makedirs(os.path.join(MEMORY_DIR, "model_b_memory"), exist_ok=True)

def save_to_memory(content, model_type):
    """Save conversation to memory using LangChain"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    memory_file = os.path.join(MEMORY_DIR, f"{model_type}_memory", f"memory_{timestamp}.json")
    history = FileChatMessageHistory(memory_file)
    history.add_ai_message(content)

def append_to_novel(content):
    """Append content to the novel file"""
    with open(NOVEL_FILE, 'a', encoding='utf-8') as f:
        f.write(content + "\n\n")

def generate_model_response(prompt, model_url):
    """Generate response from Ollama model"""
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "qwen2:7b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(model_url, headers=headers, json=data)
    return response.json().get('response', '')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/interact_a', methods=['POST'])
def interact_with_model_a():
    data = request.json
    prompt = data.get('prompt', '')
    response = generate_model_response(prompt, MODEL_A_URL)
    save_to_memory(response, "model_a")
    return jsonify({"response": response})

@app.route('/interact_b', methods=['POST'])
def interact_with_model_b():
    data = request.json
    prompt = data.get('prompt', '')
    response = generate_model_response(prompt, MODEL_B_URL)
    save_to_memory(response, "model_b")
    append_to_novel(response)
    return jsonify({"response": response})

@app.route('/start_auto_interaction', methods=['POST'])
def start_auto_interaction():
    data = request.json
    initial_prompt = data.get('prompt', '')
    
    # Start with Model A
    model_a_response = generate_model_response(initial_prompt, MODEL_A_URL)
    save_to_memory(model_a_response, "model_a")
    
    # Send to Model B
    model_b_response = generate_model_response(model_a_response, MODEL_B_URL)
    save_to_memory(model_b_response, "model_b")
    append_to_novel(model_b_response)
    
    return jsonify({
        "model_a_response": model_a_response,
        "model_b_response": model_b_response
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
