from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import get_password_hash, verify_password
from datetime import date

# User-related CRUD operations

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Transaction-related CRUD operations

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionCreate):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction:
        for key, value in transaction.dict().items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction

# Category-related CRUD operations

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

# Budget-related CRUD operations

def create_budget(db: Session, budget: schemas.BudgetCreate):
    db_budget = models.Budget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Budget).offset(skip).limit(limit).all()

def get_budget_by_category(db: Session, category_name: str):
    return db.query(models.Budget).filter(models.Budget.category == category_name).first()

# Report-related CRUD operations

def generate_summary_report(db: Session):
    total_income = db.query(models.Transaction).filter(models.Transaction.amount > 0).sum(models.Transaction.amount)
    total_expenses = db.query(models.Transaction).filter(models.Transaction.amount < 0).sum(models.Transaction.amount)
    return {
        "total_income": total_income or 0,
        "total_expenses": total_expenses or 0,
        "net_balance": (total_income or 0) + (total_expenses or 0)
    }

def generate_category_report(db: Session, category_name: str):
    category_total = db.query(models.Transaction).filter(models.Transaction.category == category_name).sum(models.Transaction.amount)
    return {
        "category": category_name,
        "total_spent": category_total or 0
    }
