from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./crud_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    created_at = Column(String, default=datetime.now().isoformat())

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class Item(ItemCreate):
    id: int
    created_at: str

# FastAPI App
app = FastAPI(title="CRUD API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ItemDB).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item_update.name:
        item.name = item_update.name
    if item_update.price:
        item.price = item_update.price
    
    db.commit()
    db.refresh(item)
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return None

@app.get("/")
def root():
    return {"message": "CRUD API is running", "docs": "/docs"}
