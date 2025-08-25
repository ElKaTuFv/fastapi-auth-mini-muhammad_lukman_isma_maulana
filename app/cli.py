import argparse
from sqlalchemy.orm import Session
from . import database, models, utils
from datetime import datetime, timezone


def create_admin(email: str, password: str):
    db: Session = database.SessionLocal()
    try:
        existing_admin = db.query(models.User).filter(models.User.is_admin == True).first()
        if existing_admin:
            print("Admin already exists:", existing_admin.email)
            return
        hashed_pw = utils.hash_password(password)
        admin = models.User(
            email=email,
            password_hash=hashed_pw,
            is_admin=True,
            is_verified=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(admin)
        db.commit()
        print(f"Admin created successfully: {email}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="CLI for FastAPI Auth App")
    subparsers = parser.add_subparsers(dest="command")

    create_admin_parser = subparsers.add_parser("create-admin", help="Create the first admin user")
    create_admin_parser.add_argument("--email", required=True, help="Admin email")
    create_admin_parser.add_argument("--password", required=True, help="Admin password")

    args = parser.parse_args()

    if args.command == "create-admin":
        create_admin(args.email, args.password)


if __name__ == "__main__":
    main()
