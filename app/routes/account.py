from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.account import AccountRequest, AccountResponse
from app.cruds.account import create_account, get_account, get_accounts, update_account, delete_account
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/accounts/", response_model=AccountResponse)
def create_new_account(account: AccountRequest, db: Session = Depends(get_db)):
    return create_account(db, account)

@router.get("/accounts/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.get("/accounts/", response_model=list[AccountResponse])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_accounts(db, skip, limit)

@router.put("/accounts/{account_id}", response_model=bool)
def update_existing_account(account_id: int, account: AccountRequest, db: Session = Depends(get_db)):
    db_account = update_account(db, account_id, account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return True

@router.delete("/accounts/{account_id}", response_model=bool)
def delete_existing_account(account_id: int, db: Session = Depends(get_db)):
    db_account = delete_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return True