from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Collateral
from ..schemas import CollateralCreate, Collateral

router = APIRouter()

@router.post("/", response_model=Collateral)
def create_collateral(collateral: CollateralCreate, db: Session = Depends(get_db)):
    db_collateral = Collateral(**collateral.dict())
    db.add(db_collateral)
    db.commit()
    db.refresh(db_collateral)
    return db_collateral

@router.get("/", response_model=list[Collateral])
def get_collaterals(db: Session = Depends(get_db)):
    return db.query(Collateral).all()

@router.get("/{collateralId}", response_model=Collateral)
def get_collateral(collateralId: int, db: Session = Depends(get_db)):
    collateral = db.query(Collateral).filter(Collateral.id == collateralId).first()
    if collateral is None:
        raise HTTPException(status_code=404, detail="Artículo pignorado no encontrado")
    return collateral

@router.delete("/{collateralId}", status_code=204)
def delete_collateral(collateralId: int, db: Session = Depends(get_db)):
    db_collateral = db.query(Collateral).filter(Collateral.id == collateralId).first()
    if db_collateral is None:
        raise HTTPException(status_code=404, detail="Artículo pignorado no encontrado")
    db.delete(db_collateral)
    db.commit()