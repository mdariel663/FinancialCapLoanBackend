from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Transaction
from ..schemas import TransactionCreate, Transaction

router = APIRouter()

@router.post("/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=list[Transaction])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

@router.get("/{transactionId}", response_model=Transaction)
def get_transaction(transactionId: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transactionId).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaction

@router.delete("/{transactionId}", status_code=204)
def delete_transaction(transactionId: int, db: Session = Depends(get_db)):
    db_transaction = db.query(Transaction).filter(Transaction.id == transactionId).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    db.delete(db_transaction)
    db.commit()