from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import databases
import uuid

import requests

DATABASE_URL = "sqlite:///./comments.db"
database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Comment(Base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True)
    content = Column(String, index=True)
    user_id = Column(String, index=True)
    user_name = Column(String, default=None)
    picture = Column(String)
    article_id = Column(String, index=True)

class CommentManager:
    @classmethod
    def create_comment(cls, db: Session, comment_data: dict, user_id: str):
        comment_data["id"] = str(uuid.uuid4())
        
        try:
            user = requests.get(f"http://bqp-auth-profile-service:6001/users/me/{user_id}/").json()
            comment_data['user_name'] = user['full_name']
            comment_data['picture'] = user['picture']
        except Exception as e:
            print("################", e)
        
        db_comment = Comment(**comment_data, user_id=user_id)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @classmethod
    def get_comment_by_article_id(cls, db: Session, article_id: str):
        return db.query(Comment).filter(Comment.article_id == article_id).all()
    
    

    @classmethod
    def update_comment(cls, db: Session, comment_id: str, comment_data: dict):
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if db_comment is None:
            return None
        for key, value in comment_data.items():
            setattr(db_comment, key, value)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @classmethod
    def delete_comment(cls, db: Session, comment_id: str):
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if db_comment is None:
            return None
        db.delete(db_comment)
        db.commit()
        return {"message": "Comment deleted successfully"}
