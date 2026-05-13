from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.db import engine, Base

# Import all models so Alembic can detect them
from app.models import user, lead, product, lead_product, invoice, contract, activity, attachment, payment

# Import routers
from app.api.v1 import products, invoices, contracts, activities, payments as payments_router, leads_crm, attachments, users

# Create tables (for development; use alembic for production)
Base.metadata.create_all(bind=engine)

# Create storage directory
os.makedirs(settings.FILE_STORAGE_PATH, exist_ok=True)
os.makedirs(f"{settings.FILE_STORAGE_PATH}/invoices", exist_ok=True)
os.makedirs(f"{settings.FILE_STORAGE_PATH}/contracts", exist_ok=True)
os.makedirs(f"{settings.FILE_STORAGE_PATH}/templates", exist_ok=True)
os.makedirs(f"{settings.FILE_STORAGE_PATH}/attachments", exist_ok=True)
os.makedirs(f"{settings.FILE_STORAGE_PATH}/signed", exist_ok=True)

app = FastAPI(title="PACETEL ERP CRM API", version="1.0.0", docs_url="/api/docs", redoc_url="/api/redoc")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for storage
if os.path.exists(settings.FILE_STORAGE_PATH):
    app.mount("/storage", StaticFiles(directory=settings.FILE_STORAGE_PATH), name="storage")

# Register routers
app.include_router(leads_crm.router, prefix="/api/leads", tags=["Leads CRM"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(contracts.router, prefix="/api/contracts", tags=["Contracts"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])
app.include_router(payments_router.router, prefix="/api/payments", tags=["Payments"])
app.include_router(attachments.router, prefix="/api/attachments", tags=["Attachments"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "PACETEL ERP CRM", "version": "1.0.0"}

# Start scheduler on startup
from app.core.scheduler import start_scheduler

@app.on_event("startup")
def startup_event():
    start_scheduler()
