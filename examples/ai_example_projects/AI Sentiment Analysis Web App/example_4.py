
### Step 3: Create a Frontend
Create a simple HTML form in a file named `templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analysis</title>
</head>
<body>
    <h1>Sentiment Analysis</h1>
    <form action="/analyze" method="post">
        <textarea name="text" rows="4" cols="50"></textarea>
        <br>
        <button type="submit">Analyze</button>
    </form>
    <div id="result"></div>

    <script>
        const form = document.querySelector('form');
        const resultDiv = document.getElementById('result');
        form.onsubmit = async (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });

            const result = await response.json();
            resultDiv.textContent = `Label: ${result.label}, Score: ${result.score.toFixed(4)}`;
        };
    </script>
</body>
</html>
```