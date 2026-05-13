from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.routes.user_routes import router as user_router
from app.routes.customer_routes import router as customer_routes
from app.routes.agent_routes import router as agent_routes
from app.routes.policy_routes import router as policy_routes
from app.routes.cost_center_routes import router as cost_center_routes
from app.routes.lead_routes import router as lead_routes
from app.routes.lead_log_routes import router as lead_log_routes
from app.routes.upgrade_routes import router as upgrade_routes
from app.routes.upgrade_log_routes import router as upgrade_log_routes
from app.routes.sub_cost_center_routes import router as sub_cost_center_routes
from app.routes.task_routes import router as task_routes
from app.routes.task_comment_routes import router as task_comment_routes
from app.routes.teams_routes import router as teams_routes
from app.routes.inventory_routes import router as inventory_routes
from app.routes.stock_movement_routes import router as stock_movement_routes
from app.routes.chat_routes import router as chat_routes
from app.routes.chat_participant_routes import router as chat_participant_routes
from app.routes.message_routes import router as message_routes
from app.routes.city_routes import router as city_routes
from app.routes.migration_routes import router as migration_routes
from app.routes.invoice_routes import router as invoice_routes
from app.routes.rbac_routes import router as rbac_routes
from app.routes.bend_routes import router as bend_routes
from app.routes.aend_routes import router as aend_routes
from app.routes.erp_routes import router as erp_routes
from app.scheduler import start_scheduler










app = FastAPI(debug=True)

@app.on_event("startup")
def on_startup():
    start_scheduler()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# GLOBAL ERROR HANDLERS (SHOW DETAILS)
# -----------------------------------

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Database Error",
            "details": str(exc.__cause__ or exc)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Server Error",
            "details": str(exc)
        }
    )

# ------------- ROUTES -------------
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(customer_routes, prefix="/api", tags=["Customers"])
app.include_router(agent_routes, prefix="/api", tags=["Agents"])
app.include_router(policy_routes, prefix="/api", tags=["Policies"])
app.include_router(cost_center_routes, prefix="/api", tags=["Cost Centers"])
app.include_router(lead_routes, prefix="/api", tags=["Leads"])
app.include_router(lead_log_routes, prefix="/api", tags=["Lead Logs"])
app.include_router(upgrade_routes, prefix="/api", tags=["Upgrades"])
app.include_router(upgrade_log_routes, prefix="/api", tags=["Upgrade Logs"])
app.include_router(sub_cost_center_routes, prefix="/api", tags=["Sub Cost Centers"])
app.include_router(task_routes, prefix="/api", tags=["Tasks"])
app.include_router(task_comment_routes, prefix="/api", tags=["Task Comments"])
app.include_router(teams_routes, prefix="/api", tags=["Teams"])
app.include_router(inventory_routes, prefix="/api", tags=["Inventory"])
app.include_router(stock_movement_routes, prefix="/api", tags=["Stock Movements"])
app.include_router(chat_routes, prefix="/api", tags=["Chats"])
app.include_router(chat_participant_routes, prefix="/api", tags=["Chat Participants"])
app.include_router(message_routes, prefix="/api", tags=["Messages"])
app.include_router(city_routes, prefix="/api", tags=["Cities"])
app.include_router(migration_routes, prefix="/api", tags=["Migration"])
app.include_router(invoice_routes, prefix="/api", tags=["Billing"])
app.include_router(rbac_routes, prefix="/api", tags=["RBAC"])
app.include_router(bend_routes, prefix="/api")
app.include_router(aend_routes, prefix="/api")
app.include_router(erp_routes, prefix="/api", tags=["ERP"])



@app.get("/")
def root():
    return {"message": "CRM Backend Running"}


