### Explanation

1. **Connect to SurrealDB**: Using the `websockets` library, the app establishes a connection to the SurrealDB instance.
2. **Startup Event**: Ensures a persistent database connection throughout the app's lifecycle.
3. **Endpoint Definition**: The FastAPI app defines an endpoint to query SurrealDB with item-specific details.
4. **Database Queries**: Performs read operations by sending the appropriate JSON-RPC query over the WebSocket connection.