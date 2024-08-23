from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import auth_controller, user_controller, loan_controller, collateral_controller, transaction_controller, report_controller
import app.database as database

app = FastAPI(
    title="Sistema de Préstamos API",
    description="API para la gestión en tiempo real de un sistema de préstamos.",
    version="1.0.0"
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth_controller.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(user_controller.router, prefix="/api/users", tags=["Usuarios"])
app.include_router(loan_controller.router, prefix="/api/loans", tags=["Préstamos"])
app.include_router(collateral_controller.router, prefix="/api/collaterals", tags=["Artículos Pignorados"])
app.include_router(transaction_controller.router, prefix="/api/transactions", tags=["Transacciones"])
app.include_router(report_controller.router, prefix="/api/reports", tags=["Reportes"])


@app.on_event("startup")
def startup_db():
    database.Base.metadata.create_all(bind=database.engine)