from sqlalchemy import Column, Integer, String, DateTime
from db import Base

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'
    
class Conversation(Base):
    __tablename__ = 'Conversation'

    id = Column(Integer, primary_key=True)
    type = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Conversation {self.id}>'
    
class Message(Base):
    __tablename__ = 'Message'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, nullable=False)
    sender_id = Column(Integer, nullable=False)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Message {self.id}>'
    
class Participant(Base):
    __tablename__ = 'Participant'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Participant {self.id}>'