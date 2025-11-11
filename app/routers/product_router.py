

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService
from app.core.database import get_session
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.security.auth_utils import require_admin


router=APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductRead])
def list_products(session: Session = Depends(get_session)):
    service = ProductService(session)
    return service.get_all_products()

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    service = ProductService(session)
    return service.get_product_by_id(product_id)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate, 
    session: Session = Depends(get_session),
    current_user=Depends(require_admin)
    ):
    service = ProductService(session)
    return service.create_product(product)

@router.put(
    "/{product_id}", 
    response_model=ProductRead
    )
def update_product(
    product_id: int, 
    product: ProductUpdate, 
    session: Session = Depends(get_session),
    current_user=Depends(require_admin)):
    service = ProductService(session)
    return service.update_product(product_id, product)

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    service = ProductService(session)
    return service.delete_product(product_id)

# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJicmlhbiIsImV4cCI6MTc2Mjg3NTI5Nn0.LFnnRDxi1SPWrQRJKB7Qp4sgvefvCWKl2KXXoENmmEk",
#   "token_type": "bearer"
# }