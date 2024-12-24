### Step 2: Set Up a Simple Flask Application

Create a new file named `app.py` for your Flask web application:

```python
from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# Load a pre-trained sentiment-analysis pipeline
sentiment_analysis = pipeline("sentiment-analysis")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    text = request.form['text']
    analysis = sentiment_analysis(text)[0]
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)
```