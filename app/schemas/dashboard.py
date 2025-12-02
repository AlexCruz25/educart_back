from typing import List
from sqlmodel import SQLModel
from app.models.product import StockStatus


class DashboardKPIs(SQLModel):
    sales_total_month: float
    pending_orders: int
    low_stock_products: int
    inventory_value: float


class TopSeller(SQLModel):
    product_id: int
    name: str
    quantity_sold: int


class InventoryDistribution(SQLModel):
    category: str
    stock_total: int


class AlertProduct(SQLModel):
    id: int
    sku: str
    name: str
    category: str
    stock_actual: int
    stock_minimo: int
    stock_status: StockStatus

    class Config:
        orm_mode = True


class DashboardResponse(SQLModel):
    kpis: DashboardKPIs
    top_sellers: List[TopSeller]
    inventory_distribution: List[InventoryDistribution]
    alerts: List[AlertProduct]