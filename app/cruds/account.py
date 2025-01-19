from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.schemas.account import AccountRequest, AccountResponse
from fastapi import HTTPException

def create_account(db: Session, account: AccountRequest):
    try:
        query_str = text(
            """
            INSERT INTO ACCOUNTS (IMAGE, USERNAME, PASSWORD, EMAIL, PHONE)
            OUTPUT inserted.ID, inserted.IMAGE, inserted.USERNAME, inserted.EMAIL, inserted.PHONE
            VALUES (:image, :username, :password, :email, :phone);
            """
        )

        db_account = db.execute(
            query_str,
            {
                "image": account.image,
                "username": account.username,
                "password": account.password,
                "email": account.email,
                "phone": account.phone,
            },
        ).fetchone()
        db.commit()
        return {
            "id": db_account.ID,
            "image": db_account.IMAGE,
            "username": db_account.USERNAME,
            "email": db_account.EMAIL,
            "phone": db_account.PHONE,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_account(db: Session, account_id: int):
    try:
        query_str = text(
            """
            SELECT ID, IMAGE, USERNAME, EMAIL, PHONE
            FROM ACCOUNTS
            WHERE ID = :account_id;
            """
        )

        db_account = db.execute(query_str, {"account_id": account_id}).fetchone()
        return {
            "id": db_account.ID,
            "image": db_account.IMAGE,
            "username": db_account.USERNAME,
            "email": db_account.EMAIL,
            "phone": db_account.PHONE,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    try:
        query_str = text(
            """
            SELECT ID, IMAGE, USERNAME, EMAIL, PHONE
            FROM ACCOUNTS
            ORDER BY ID DESC
            OFFSET :skip ROWS FETCH NEXT :limit ROWS ONLY;
            """
        )

        db_accounts = db.execute(query_str, {"skip": skip, "limit": limit}).fetchall()
        result = []
        for account in db_accounts:
            result.append(
                {
                    "id": account[0],
                    "image": account[1],
                    "username": account[2],
                    "email": account[3],
                    "phone": account[4],
                }
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_account(db: Session, account_id: int, account: AccountRequest):
    try:
        query_str = text(
            """
            UPDATE ACCOUNTS
            SET IMAGE = :image, USERNAME = :username, PASSWORD = :password, EMAIL = :email, PHONE = :phone
            WHERE ID = :account_id
            """
        )

        db.execute(
            query_str,
            {
                "account_id": account_id,
                "image": account.image,
                "username": account.username,
                "password": account.password,
                "email": account.email,
                "phone": account.phone,
            },
        )
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_account(db: Session, account_id: int):
    try:
        query_str = text(
            """
            DELETE FROM ACCOUNTS
            WHERE ID = :account_id
            """
        )

        db.execute(query_str, {"account_id": account_id})
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))