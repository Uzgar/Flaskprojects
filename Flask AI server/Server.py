from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Replace with your LM Studio API key
LM_STUDIO_API_KEY = "YOUR_LM_STUDIO_API_KEY"

# Set up OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key=LM_STUDIO_API_KEY)

history = [
    {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
]

@app.route('/')
def chat():
    return render_template('chat.html', history=history)

@app.route('/generate_response', methods=['POST'])
def generate_response():
    user_input = request.form['user_input']

    # Communicate with LM Studio using 'client' variable
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=history + [{"role": "user", "content": user_input}],
        temperature=0.7,
    )

    # Extract assistant's reply from the completion
    assistant_reply = completion.choices[0].message.content

    new_message = {"role": "assistant", "content": assistant_reply}
    history.append(new_message)

    # Return the response as JSON
    return jsonify({'assistant_reply': assistant_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500)
