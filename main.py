from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

client = openai.OpenAI(
    api_key="glhf_a4c7ed88c9100b2bc434749b20239e8c",
    base_url="https://glhf.chat/api/openai/v1",
)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the messages from the request
        data = request.json
        messages = data.get('messages', [])
        
        # If messages is empty, initialize with system message
        if not messages:
            messages = [{"role": "system", "content": "You are a helpful assistant."}]
        
        # Get response from API
        completion = client.chat.completions.create(
            model="hf:Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=messages
        )
        
        # Get assistant's response
        assistant_response = completion.choices[0].message.content
        
        return jsonify({
            "response": assistant_response,
            "messages": messages + [{"role": "assistant", "content": assistant_response}]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)