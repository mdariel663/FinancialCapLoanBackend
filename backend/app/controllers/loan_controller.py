from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Loan
from ..schemas import LoanCreate, Loan

router = APIRouter()

@router.post("/", response_model=Loan)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = Loan(**loan.dict())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.get("/", response_model=list[Loan])
def get_loans(db: Session = Depends(get_db), status: str = None):
    query = db.query(Loan)
    if status:
        query = query.filter(Loan.status == status)
    return query.all()

@router.get("/{loanId}", response_model=Loan)
def get_loan(loanId: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loanId).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan

@router.put("/{loanId}", response_model=Loan)
def update_loan(loanId: int, loan: LoanCreate, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loanId).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    for key, value in loan.dict().items():
        setattr(db_loan, key, value)
    
    db.commit()
    db.refresh(db_loan)
    return db_loan

@router.delete("/{loanId}", status_code=204)
def delete_loan(loanId: int, db: Session = Depends(get_db)):
    db_loan = db.query(Loan).filter(Loan.id == loanId).first()
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    db.delete(db_loan)
    db.commit()