```python
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
sentiment_pipeline = pipeline('sentiment-analysis')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text')
    result = sentiment_pipeline(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```