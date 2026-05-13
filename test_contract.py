from app.database import SessionLocal
from app.services.erp_service import ERPService
from app.models.erp_models import ContractTemplate
import sys

def test():
    db = SessionLocal()
    try:
        tmpl = db.query(ContractTemplate).first()
        if not tmpl:
            print("No template found!")
            return
        
        print(f"Attempting to generate contract for lead 1 using template {tmpl.id}...")
        c = ERPService.generate_contract(db, 1, tmpl.id)
        if c:
            print(f"Success! Contract ID: {c.id}")
            print(f"File Path: {c.file_path}")
        else:
            print("Failed (returned None). Check for errors.")
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test()
