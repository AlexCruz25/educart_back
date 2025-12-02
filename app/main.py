from fastapi import FastAPI

from app.core.database import init_db

from app.routers import auth_router
from app.routers import cart_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router
from app.routers.dashboard_router import router as dashboard_router


app = FastAPI(title="EduCart")


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(product_router)
app.include_router(auth_router.router)
app.include_router(cart_router.router)
app.include_router(order_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Educart api funciona"}