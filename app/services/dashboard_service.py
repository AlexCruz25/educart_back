from datetime import datetime
from sqlalchemy import func
from sqlmodel import Session, select

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardKPIs,
    TopSeller,
    InventoryDistribution,
    AlertProduct,
)


class DashboardService:
    def __init__(self, session: Session):
        self.session = session

    def get_dashboard(self) -> DashboardResponse:
        kpis = self._build_kpis()
        top_sellers = self._get_top_sellers()
        distribution = self._get_inventory_distribution()
        alerts = self._get_alerts()

        return DashboardResponse(
            kpis=kpis,
            top_sellers=top_sellers,
            inventory_distribution=distribution,
            alerts=alerts,
        )

    def _build_kpis(self) -> DashboardKPIs:
        now = datetime.utcnow()
        month_start = datetime(now.year, now.month, 1)

        sales_statement = select(func.coalesce(func.sum(Order.total), 0)).where(
            Order.status == OrderStatus.CONFIRMED, Order.created_at >= month_start
        )
        sales_total = self.session.exec(sales_statement).one()

        pending_statement = select(func.count(Order.id)).where(
            Order.status == OrderStatus.CONFIRMED
        )
        pending_orders = self.session.exec(pending_statement).one()

        low_stock_statement = select(func.count(Product.id)).where(
            (Product.stock_actual == 0) | (Product.stock_actual <= Product.stock_minimo)
        )
        low_stock_products = self.session.exec(low_stock_statement).one()

        inventory_value_statement = select(
            func.coalesce(func.sum(Product.price * Product.stock_actual), 0)
        )
        inventory_value = self.session.exec(inventory_value_statement).one()

        return DashboardKPIs(
            sales_total_month=float(sales_total),
            pending_orders=int(pending_orders),
            low_stock_products=int(low_stock_products),
            inventory_value=float(inventory_value),
        )

    def _get_top_sellers(self) -> list[TopSeller]:
        statement = (
            select(
                OrderItem.product_id,
                OrderItem.name,
                func.sum(OrderItem.quantity).label("quantity_sold"),
            )
            .join(Order, Order.id == OrderItem.order_id)
            .where(Order.status == OrderStatus.CONFIRMED)
            .group_by(OrderItem.product_id, OrderItem.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(5)
        )
        results = self.session.exec(statement).all()
        return [
            TopSeller(product_id=row.product_id, name=row.name, quantity_sold=row.quantity_sold)
            for row in results
        ]

    def _get_inventory_distribution(self) -> list[InventoryDistribution]:
        statement = (
            select(Product.category, func.sum(Product.stock_actual).label("stock_total"))
            .group_by(Product.category)
            .order_by(Product.category)
        )
        results = self.session.exec(statement).all()
        return [
            InventoryDistribution(category=row.category, stock_total=row.stock_total)
            for row in results
        ]

    def _get_alerts(self) -> list[AlertProduct]:
        statement = select(Product).where(
            (Product.stock_actual == 0) | (Product.stock_actual <= Product.stock_minimo)
        )
        products = self.session.exec(statement).all()
        alerts: list[AlertProduct] = []
        for product in products:
            alerts.append(
                AlertProduct(
                    id=product.id,
                    sku=product.sku,
                    name=product.name,
                    category=product.category,
                    stock_actual=product.stock_actual,
                    stock_minimo=product.stock_minimo,
                    stock_status=product.stock_status,
                )
            )
        return alerts