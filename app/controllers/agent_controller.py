from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.agent_models import Agent
from app.schemas.agent_schemas import AgentCreate, AgentUpdate, AgentOut

router = APIRouter(prefix="/agents", tags=["Agents"])

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database Error",
            "details": str(exc.__cause__ or exc)
        }
    )
# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ▶ GET ALL AGENTS
@router.get("/", response_model=list[AgentOut])
def get_agents(db: Session = Depends(get_db)):
    agents = db.query(Agent).all()
    return agents


# ▶ CREATE NEW AGENT
@router.post("/", response_model=AgentOut)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    new_agent = Agent(**agent.dict())
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent


# ▶ GET AGENT BY ID
@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


# ▶ UPDATE AGENT
@router.put("/{agent_id}", response_model=AgentOut)
def update_agent(agent_id: int, update_data: AgentUpdate, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Apply only provided fields
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(agent, key, value)

    db.commit()
    db.refresh(agent)
    return agent


# ▶ DELETE AGENT
@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    db.delete(agent)
    db.commit()

    return {"message": "Agent deleted successfully"}