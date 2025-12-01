
from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, session: Session):
        self.repo = ProductRepository(session)
        
    def create_product(self, product_data: ProductCreate) -> Product:
       
        existing_products = self.repo.get_all()
        if any(p.name.lower() == product_data.name.lower() for p in existing_products):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un producto con ese nombre",
            )
        if self.repo.get_by_sku(product_data.sku):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un producto con ese SKU",
            )

        product = Product(**product_data.dict())
        return self.repo.create(product)
        
    def get_all_products(
        self,
        *,
        category: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_rating: float | None = None,
        search: str | None = None,
        sort_by: str | None = None,
    ) -> list[Product]:
        products = self.repo.get_filtered(
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_rating=min_rating,
            search=search,
            sort_by=sort_by,
        )
        
        return products
    
    def get_product_by_id(self, product_id: int) -> Product:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado.",
            )
        return product
    
    
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado para actualizar",
            )
        if product_data.sku and product_data.sku != product.sku:
            duplicate = self.repo.get_by_sku(product_data.sku)
            if duplicate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un producto con ese SKU",
                )

        updated = self.repo.update(product_id, product_data.dict(exclude_unset=True))
        return updated
    
    def delete_product(self, product_id: int) -> dict:
        deleted = self.repo.delete(product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",

            )
        return {"detail": "Producto eliminado correctamente"}
    
    