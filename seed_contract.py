from app.database import engine, SessionLocal
from sqlalchemy import text
from app.models.erp_models import ContractTemplate

def seed_template():
    db = SessionLocal()
    try:
        count = db.query(ContractTemplate).count()
        print(f"Existing templates: {count}")
        if count == 0:
            print("Seeding a default template...")
            tpl = ContractTemplate(
                name="Standard Service Agreement",
                file_path="", # Empty means it will use the fallback docx generation
                content="Standard terms and conditions.",
                is_active=True
            )
            db.add(tpl)
            db.commit()
            print("Template seeded!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_template()
