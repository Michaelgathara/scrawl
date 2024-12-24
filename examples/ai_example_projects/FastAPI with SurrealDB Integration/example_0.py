### App.py

```python
from fastapi import FastAPI, WebSocket
import asyncio
import websockets

app = FastAPI()

database_url = "ws://localhost:8000/rpc"

db_user = "root"
db_pass = "root"

async def connect_to_db():
    websocket = await websockets.connect(database_url)
    await websocket.send(f'{{"id":"1","method":"signin","params":["{db_user}","{db_pass}"]}}')
    response = await websocket.recv()
    print("Connected to SurrealDB:", response)
    return websocket

@app.on_event("startup")
async def startup_event():
    global db_connection
    db_connection = await connect_to_db()

async def surreal_query(query: str):
    await db_connection.send(query)
    response = await db_connection.recv()
    return response

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    query = f'{{"id":"2","method":"select","params":["item", ["{item_id}"]]}}'
    result = await surreal_query(query)
    return result
```

### Running the Application

Ensure that SurrealDB is running. Then, start your FastAPI app by running:

```bash
uvicorn app:app --reload
```

### Testing the Endpoint

Open your browser and visit: `http://127.0.0.1:8000/items/<item_id>`

You'll see the JSON response from SurrealDB for the item requested.