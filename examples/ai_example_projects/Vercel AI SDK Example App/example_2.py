// Step 4: Create a front-end to use the AI functionality
// HTML file (index.html)
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vercel AI Demo</title>
</head>
<body>
    <h1>AI Text Generator</h1>
    <textarea id="prompt" rows="4" cols="50" placeholder="Enter your prompt here..."></textarea>
    <button onclick="generate()">Generate Text</button>
    <div id="result"></div>

    <script>
      async function generate() {
        const prompt = document.getElementById('prompt').value;
        const response = await fetch('/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ prompt })
        });
        const data = await response.json();
        document.getElementById('result').innerText = data.text;
      }
    </script>
</body>
</html>