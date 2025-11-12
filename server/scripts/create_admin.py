import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from passlib.hash import pbkdf2_sha256
from app.db import SessionLocal, Base, engine
from app.db_models import User

def main():
    Base.metadata.create_all(bind=engine)
    username = os.getenv("DEFAULT_ADMIN_USER", "admin")
    password = os.getenv("DEFAULT_ADMIN_PASS", "ChangeMe_123!")
    with SessionLocal() as db:
        if not db.query(User).filter(User.username == username).first():
            hashed = pbkdf2_sha256.hash(password)
            db.add(User(username=username, password_hash=hashed, role="admin"))
            db.commit()
            print("Admin created:", username)
        else:
            print("Admin already exists")

if __name__ == "__main__":
    main()
