from datetime import datetime, timezone

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session

from connection.connectionManager import ConnectionManager
from db import Base, engine, SessionLocal
from models.models import User, Conversation, Message, Participant


# manager = ConnectionManager()

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MessageCreate(BaseModel):
    conversation_id: int
    sender_id: int
    content: str


@app.post("/send-message")
def create_message(payload: MessageCreate, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(
        Participant.conversation_id == payload.conversation_id,
        Participant.user_id == payload.sender_id,
    ).first()
    if not participant:
        return {"error": "User is not a participant of the conversation"}
    message = Message(
        conversation_id=payload.conversation_id,
        sender_id=payload.sender_id,
        content=payload.content,
        created_at=datetime.now(timezone.utc),
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "sender_id": message.sender_id,
        "content": message.content,
        "created_at": message.created_at,
    }


@app.get("/messages/{conversation_id}")
def list_messages(conversation_id: int, db: Session = Depends(get_db)):
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )
    return [
        {
            "id": m.id,
            "conversation_id": m.conversation_id,
            "sender_id": m.sender_id,
            "content": m.content,
            "created_at": m.created_at,
        }
        for m in messages
    ]


# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: str):
#     await manager.connect(websocket)
#     await manager.broadcast(f"Client #{client_id} joined the chat")
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(f"Client #{client_id}: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)