
# from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session
# from app.domain.interfaces.product_repository_port import IProductRepository
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, session:Session):
        self.repo=ProductRepository(session)
        
    def create_product(self, product_data: ProductCreate) -> Product:
        # validar nombres repetidos
        existing_products = self.repo.get_all()
        if any(p.name.lower() == product_data.name.lower() for p in existing_products):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un producto con ese nombre"
            )

        product = Product(**product_data.dict())
        return self.repo.create(product)
        
    def get_all_products(self) -> list[Product]:
        products = self.repo.get_all()
        if not products:
            # No es un error crítico, pero informativo
            return []
        return products
    
    def get_product_by_id(self, product_id: int) -> Product:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado."
            )
        return product
    
    
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado para actualizar"
            )

        updated = self.repo.update(product_id, product_data.dict(exclude_unset=True))
        return updated
    
    def delete_product(self, product_id: int) -> dict:
        deleted = self.repo.delete(product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        return {"detail": "Producto eliminado correctamente"}
    
    