from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal, Comment, CommentManager
from fastapi.middleware.cors import CORSMiddleware
from .utils import NotifierClient, UserProfileClient


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/comments/{article_id}/")
async def get_comments_by_article_id(article_id: str, db: Session = Depends(get_db)):
    db_comments = CommentManager.get_comment_by_article_id(db, article_id)
    return db_comments
    

@app.post("/comments/")
async def create_comment(comment_data: dict, user_id: str, db: Session = Depends(get_db)):
    db_comment = CommentManager.create_comment(db, comment_data, user_id=user_id)
    profile =UserProfileClient(user_id).get_user_profile()
    NotifierClient(profile['followers'], db_comment.article_id)
    return db_comment

@app.get("/comments/{comment_id}")
async def read_comment(comment_id: str, db: Session = Depends(get_db)):
    db_comment = CommentManager.get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@app.put("/comments/{comment_id}")
async def update_comment(comment_id: str, comment_data: dict, db: Session = Depends(get_db)):
    db_comment = CommentManager.update_comment(db, comment_id, comment_data)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: str, db: Session = Depends(get_db)):
    deleted_comment = CommentManager.delete_comment(db, comment_id)
    if deleted_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return deleted_comment
