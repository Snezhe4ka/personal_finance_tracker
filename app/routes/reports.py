from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from app import crud
from app.dependencies import get_db

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

@router.get("/summary")
def get_summary_report(db: Session = Depends(get_db)) -> Dict[str, float]:
    summary = crud.generate_summary_report(db)
    return summary

@router.get("/category/{category_name}")
def get_category_report(category_name: str, db: Session = Depends(get_db)) -> Dict[str, float]:
    report = crud.generate_category_report(db, category_name=category_name)
    return report
