```python
# Step 1: Install Flask
# Ensure Flask is installed in your Python environment
# You can install it via pip
pip install flask
```

```python
# Step 2: Setup Flask Web Application Structure
# Create a new directory for your project
mkdir AirfoilApp
cd AirfoilApp

# Step 3: Create Flask Application
# Create a file named `app.py`
```

```python
# Step 4: Implement Flask Application (app.py)
from flask import Flask, request, jsonify
# Hypothetical import from Airfoil
#from airfoil import compute_lift, compute_drag

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Airfoil Computation API"

@app.route('/compute', methods=['POST'])
def compute():
    data = request.json
    angle_of_attack = data.get('angle_of_attack')
    velocity = data.get('velocity')
    density = data.get('density')

    # Hypothetical computation
    lift = compute_lift(angle_of_attack, velocity, density)
    drag = compute_drag(angle_of_attack, velocity, density)

    return jsonify({
        'lift': lift,
        'drag': drag
    })

if __name__ == '__main__':
    app.run(debug=True)
```

```python
# Step 5: Run Your Flask App
# Run your Flask application to test the API
# In the terminal, execute:
python app.py

# Test with a tool like Postman or curl
# Example curl command:
# curl -X POST http://127.0.0.1:5000/compute -H "Content-Type: application/json" -d '{"angle_of_attack": 5, "velocity": 100, "density": 1.225}'
```

This setup provides a basic REST API to perform aerodynamic computations using the hypothetical Airfoil library. Note that `compute_lift` and `compute_drag` functions are assumed to be part of the imaginary "Airfoil" library. Replace these with actual computational functions as per your requirements.