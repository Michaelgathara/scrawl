// package.json - A simple package.json for a React app
{
  "name": "react-app-example",
  "version": "1.0.0",
  "description": "An example React application",
  "main": "index.js",
  "scripts": {
    "start": "node server.js",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "author": "Example Author",
  "license": "ISC",
  "dependencies": {
    "express": "^4.17.1",
    "react": "^16.13.1",
    "react-dom": "^16.13.1",
    "react-scripts": "3.4.1"
  },
  "proxy": "http://localhost:5000"
}