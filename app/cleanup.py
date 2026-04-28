from datetime import datetime
from .db import SessionLocal
from . import models

def cleanup():
    db = SessionLocal()
    try:
        deleted = db.query(models.URL).filter(
            models.URL.expiry != None,
            models.URL.expiry < datetime.utcnow()
        ).delete()

        db.commit()

        print(f"🧹 Deleted {deleted} expired URLs")

    except Exception as e:
        print("Cleanup error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    cleanup()
    