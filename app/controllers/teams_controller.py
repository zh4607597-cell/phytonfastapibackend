from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.teams_models import Team
from app.schemas.teams_schemas import TeamCreate, TeamUpdate

def create_team(db: Session, data: TeamCreate):
    new_team = Team(**data.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


def get_teams(db: Session):
    return db.query(Team).all()


def get_team_by_id(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


def update_team(db: Session, team_id: int, data: TeamUpdate):
    team = get_team_by_id(db, team_id)
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(team, key, value)

    db.commit()
    db.refresh(team)

    return team


def delete_team(db: Session, team_id: int):
    team = get_team_by_id(db, team_id)
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}