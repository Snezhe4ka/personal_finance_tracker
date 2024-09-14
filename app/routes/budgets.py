from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db
from typing import List

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"]
)

@router.post("/", response_model=schemas.Budget)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    return crud.create_budget(db=db, budget=budget)

@router.get("/", response_model=List[schemas.Budget])
def read_budgets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    budgets = crud.get_budgets(db, skip=skip, limit=limit)
    return budgets

@router.get("/category/{category_name}", response_model=schemas.Budget)
def get_budget_for_category(category_name: str, db: Session = Depends(get_db)):
    budget = crud.get_budget_by_category(db, category_name=category_name)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found for this category")
    return budget
