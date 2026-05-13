from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.agent_models import Agent
from app.schemas.agent_schemas import AgentCreate, AgentOut, AgentUpdate

router = APIRouter(prefix="/agent", tags=["Agents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all agents
@router.get("/", response_model=list[AgentOut])
def get_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()

# Create agent
@router.post("/", response_model=AgentOut)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    new_agent = Agent(**agent.dict())
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

# Get one agent
@router.get("/{id}", response_model=AgentOut)
def get_agent(id: int, db: Session = Depends(get_db)):
    ag = db.query(Agent).filter(Agent.id == id).first()
    if not ag:
        raise HTTPException(status_code=404, detail="Agent not found")
    return ag

# # Update agent
# @router.put("/{id}", response_model=AgentOut)
# def update_agent(id: int, data: AgentUpdate, db: Session = Depends(get_db)):
#     agent = db.query(Agent).filter(Agent.id == id).first()
#     if not agent:
#         raise HTTPException(status_code=404, detail="Agent not found")

#     for key, value in data.dict(exclude_unset=True).items():
#         setattr(agent, key, value)

#     db.commit()
#     db.refresh(agent)
#     return agent

# # Delete agent
# @router.delete("/{id}")
# def delete_agent(id: int, db: Session = Depends(get_db)):
#     agent = db.query(Agent).filter(Agent.id == id).first()
#     if not agent:
#         raise HTTPException(status_code=404, detail="Agent not found")

#     db.delete(agent)
#     db.commit()
#     return {"message": "Agent deleted successfully"}