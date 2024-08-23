from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Report
from ..schemas import ReportCreate, Report

router = APIRouter()

@router.post("/", response_model=Report)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/", response_model=list[Report])
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).all()