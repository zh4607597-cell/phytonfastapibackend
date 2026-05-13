from app.database import engine
from sqlalchemy import text

def fix_dates():
    with engine.connect() as conn:
        print("Fixing invalid dates in products table...")
        conn.execute(text("UPDATE products SET created_at = NOW() WHERE created_at = '0000-00-00 00:00:00' OR created_at IS NULL"))
        conn.execute(text("UPDATE products SET updated_at = NOW() WHERE updated_at = '0000-00-00 00:00:00' OR updated_at IS NULL"))
        conn.commit()
        print("Done.")

if __name__ == "__main__":
    fix_dates()
