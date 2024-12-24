### Image Processing with Gemini AI
```python
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO

app = FastAPI()

@app.post('/process-image/')
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    
    # Example transformation: Convert to grayscale
    grayscale_image = image.convert('L')

    response_stream = BytesIO()
    grayscale_image.save(response_stream, format='JPEG')
    response_stream.seek(0)
    
    return StreamingResponse(response_stream, media_type='image/jpeg')

# To run the app, use the command: uvicorn script_name:app --reload
```

### Instructions
1. Ensure to have `Pillow`, `fastapi`, and `uvicorn` installed via pip.
2. Modify or add processing functions as needed.
3. Use a tool like Postman to send image files to `/process-image/`.