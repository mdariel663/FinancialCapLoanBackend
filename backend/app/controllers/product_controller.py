from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from ..models import Product as ProductModel
from ..database import get_session
from ..schemas import ProductCreate, Product

router = APIRouter()

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate):
    session = next(get_session())
    new_product = ProductModel(**product.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@router.get("/", response_model=list[Product])
async def get_products():
    session = next(get_session())
    return session.query(ProductModel).all()

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int):
    session = next(get_session())
    product = session.query(ProductModel).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product