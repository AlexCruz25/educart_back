from fastapi import FastAPI

from app.core.database import init_db
from app.routers.product_router import router as product_router
from app.routers import auth_router

app=FastAPI(title="EduCart")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(product_router)
app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"status":"ok", "message": "Educart api funciona"}