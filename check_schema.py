from app.database import engine
from sqlalchemy import text

def check():
    with engine.connect() as conn:
        print("--- products table ---")
        res = conn.execute(text("DESCRIBE products"))
        for r in res:
            print(dict(r._mapping))
        
        print("\n--- lead_products table ---")
        res = conn.execute(text("DESCRIBE lead_products"))
        for r in res:
            print(dict(r._mapping))

if __name__ == "__main__":
    check()
