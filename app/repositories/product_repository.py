

from typing import List, Optional
from sqlmodel import Session, select
# from app.domain.interfaces.product_repository_port import IProductRepository
from app.models.product import Product


class ProductRepository:
    def __init__(self, session:Session):
        self.session=session
        
    def create(self, product:Product)->Product:
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product
        
    def get_all(self)->List[Product]:
        return self.session.exec(select(Product)).all()
    
    def get_by_id(self, product_id:int)->Optional[Product]:
        return self.session.get_by_id(Product, product_id)
    
    
    def update(self, product_id:int, product_data:Product)->Optional[Product]:
        db_product=self.session.get(Product, product_id)
        if not db_product:
            return None
        
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(db_product,key, value)
            
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product
    
    def delete(self, product_id:int)->bool:
        db_product=self.session.get(Product, product_id)
        if not db_product:
            return False
        
        self.session.delete(db_product)
        self.session.commit()
        return True
    