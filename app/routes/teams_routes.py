from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.teams_schemas import TeamCreate, TeamUpdate, TeamResponse
from app.controllers.teams_controller import (
    create_team, get_teams, get_team_by_id, update_team, delete_team
)

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamResponse)
def create(data: TeamCreate, db: Session = Depends(get_db)):
    return create_team(db, data)


@router.get("/", response_model=list[TeamResponse])
def get_all(db: Session = Depends(get_db)):
    return get_teams(db)


@router.get("/{team_id}", response_model=TeamResponse)
def get_by_id(team_id: int, db: Session = Depends(get_db)):
    return get_team_by_id(db, team_id)


@router.put("/{team_id}", response_model=TeamResponse)
def update(team_id: int, data: TeamUpdate, db: Session = Depends(get_db)):
    return update_team(db, team_id, data)


@router.delete("/{team_id}")
def delete(team_id: int, db: Session = Depends(get_db)):
    return delete_team(db, team_id)