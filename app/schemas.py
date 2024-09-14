from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# User Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    amount: float
    date: date
    category: str
    description: Optional[str] = None

class Transaction(BaseModel):
    id: int
    user_id: int
    amount: float
    date: date
    category: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str

class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class BudgetCreate(BaseModel):
    category: str
    amount: float
    period: str

class Budget(BaseModel):
    id: int
    category: str
    amount: float
    period: str

    class Config:
        orm_mode = True
