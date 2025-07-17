from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Pydantic Schema
class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str = None
    email: str = None


# DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "FastAPI + MySQL"}


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted"}
