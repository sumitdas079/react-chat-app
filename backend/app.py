from datetime import datetime, timezone

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from connection.connectionManager import ConnectionManager
from db import Base, engine, SessionLocal
from models.models import User, Conversation, Message, Participant
from utils.participant_enums import ConversationType, ParticipantNumber, validate_conversation_type


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

class ConversationCreate(BaseModel):
    type: int
    participant_ids: list[int]


@app.post("/create-conversation")
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    try:
        conv_type = validate_conversation_type(payload.type)
    except ValueError as e:
        return {"error": str(e)}

    participant_ids = list(set(payload.participant_ids))
    max_participants = ParticipantNumber[conv_type.name].value
    
    # validate the no. of participants based on the conversation type
    if conv_type == ConversationType.ONE_ON_ONE:
        if len(participant_ids) != max_participants:
            return {"error": f"ONE_ON_ONE conversation requires exactly {max_participants} participants"}
    else:
        if len(participant_ids) < 2:
            return {"error": "GROUP conversation requires at least 2 participants"}
        if len(participant_ids) > max_participants:
            return {"error": f"GROUP conversation allows at most {max_participants} participants"}

    # Validate that all participant_ids correspond to existing users in the database
    existing_users = db.query(User.id).filter(User.id.in_(participant_ids)).all()
    found_ids = {u.id for u in existing_users}
    missing = sorted(set(participant_ids) - found_ids)
    if missing:
        return {"error": "Some participant_ids do not correspond to existing users", "missing_ids": missing}

    # Check if a ONE_ON_ONE conversation already exists between the two users to avoid a separate thread to start between the two
    if conv_type == ConversationType.ONE_ON_ONE:
        user_a, user_b = participant_ids[0], participant_ids[1]
        convs_a = db.query(Participant.conversation_id).filter(Participant.user_id == user_a).subquery()
        convs_b = db.query(Participant.conversation_id).filter(Participant.user_id == user_b).subquery()
        existing = db.query(Conversation).filter(
            Conversation.id.in_(convs_a),
            Conversation.id.in_(convs_b),
            Conversation.type == conv_type.name,
        ).first()
        if existing:
            return {"error": "A ONE_ON_ONE conversation already exists between these users", "conversation_id": existing.id}

    conversation = Conversation(type=conv_type.name, created_at=datetime.now(timezone.utc))
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    for user_id in participant_ids:
        db.add(Participant(conversation_id=conversation.id, user_id=user_id))

    db.commit()

    return {
        "id": conversation.id,
        "type": conversation.type,
        "created_at": conversation.created_at,
    }


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