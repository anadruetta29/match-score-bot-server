# match-score-bot-server
Match Score Bot Server is a backend API built with FastAPI that powers a conversational chatbot designed to evaluate a potential romantic match. Through a structured dialogue, the chatbot asks guided questions, processes user answers, and returns a final score from 1 to 10.

The server is responsible for managing chat sessions, conversation flow, scoring logic, and feedback collection, while exposing both WebSocket and REST endpoints for real-time interaction and data persistence.

## Endpoints

### Health Check
GET /
Response: { "status": "Match Score Bot API running" }

### WebSocket – Chat
WS /ws/chat
- Handles real-time conversation
- Manages chat state and session lifecycle
- Sends questions, receives answers, and returns results

### Feedback Endpoint
POST /sessions/{session_id}/feedback?is_useful=true|false
- Stores user feedback related to a chat session
- Used to improve future iterations and model training

## Getting Started

### Requirements
    Python 3.10+
    Virtual environment (recommended)

### Installation    
    python -m venv venv
    source venv/bin/activate (On Windows: venv\\Scripts\\activate)

### Run the server
    uvicorn app.main:app --reload

### The API will be available at:
    http://localhost:8000

## Notes
This repository contains only the backend server. The frontend client is developed separately and communicates with this API via WebSocket and REST endpoints.

