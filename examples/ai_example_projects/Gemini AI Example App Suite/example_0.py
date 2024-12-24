### Chatbot with Gemini AI
```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Example API request to Gemini AI
    response = requests.post('https://api.geminiai.com/chat', json={
        'message': user_message,
        'apiKey': 'YOUR_API_KEY'
    })
    data = response.json()
    
    return jsonify({'response': data.get('reply')})

if __name__ == '__main__':
    app.run(debug=True)
```

### Instructions
1. Replace `https://api.geminiai.com/chat` with the actual API endpoint.
2. Substitute `'YOUR_API_KEY'` with your actual Gemini AI API key.
3. Use a client like Postman or curl to test the endpoint by sending a JSON payload, for example: `{'message': 'Hello, Gemini!'}`.