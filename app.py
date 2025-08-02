import uuid
from database import SessionLocal, create_db_and_tables, get_db
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import auth # Import your new auth file

# Import your new models and the session/db creation functions
import models
from database import SessionLocal, create_db_and_tables

# Create the database tables if they don't exist
create_db_and_tables()

app = FastAPI(
    title="PayCheck API v2",
    description="A mock credit bill payment simulation API with a real database.",
    version="2.0.0"
)

# --- Dependency to get DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Models ---

class User(BaseModel):
    user_id: str
    name: str
    model_config = ConfigDict(from_attributes=True)

class Bill(BaseModel):
    bill_id: str
    amount: float
    status: str
    model_config = ConfigDict(from_attributes=True)

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    status: str
    model_config = ConfigDict(from_attributes=True)

class PaymentRequest(BaseModel):
    user_id: str
    bill_id: str
    amount: float

# --- API Endpoints ---

@app.get("/health", tags=["Monitoring"])
def health_check():
    """Basic health check for the service."""
    return {"status": "ok"}

@app.get("/users", response_model=List[User], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    """List all mock users."""
    return db.query(models.User).all()

@app.post("/login", tags=["Authentication"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.get_user(db, user_id=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- UPDATED: Protected Bills Endpoint ---
@app.get("/bills/{user_id}", response_model=List[Bill], tags=["Bills"])
def get_user_bills(user_id: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Authorization check: Make sure the logged-in user is requesting their own bills
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    # The query is now simpler because we use current_user
    due_bills = db.query(models.Bill).filter(models.Bill.user_id == current_user.id, models.Bill.status == "DUE").all()
    return due_bills

@app.post("/pay", response_model=Transaction, tags=["Payments"])
def process_payment(payment: PaymentRequest, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Add this authorization check
    if current_user.user_id != payment.user_id:
        raise HTTPException(status_code=403, detail="You can only process payments for your own account.")
    """Accepts payment info and marks a bill as paid."""
    # --- Validation ---
    db_user = db.query(models.User).filter(models.User.user_id == payment.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_bill = db.query(models.Bill).filter(models.Bill.bill_id == payment.bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    if db_bill.owner.id != db_user.id:
        raise HTTPException(status_code=403, detail="Bill does not belong to user")
    if db_bill.status == "PAID":
        raise HTTPException(status_code=400, detail="Bill already paid")
    if db_bill.amount != payment.amount:
        raise HTTPException(status_code=400, detail="Payment amount does not match bill amount")

    # --- Process Payment ---
    db_bill.status = "PAID"
    
    new_txn = models.Transaction(
        transaction_id=f"txn_{uuid.uuid4().hex[:6]}",
        user_id=db_user.id,
        bill_id=db_bill.id,
        amount=payment.amount,
        status="SUCCESS"
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn) # Refresh to get the new object state from the DB
    
    return new_txn

@app.get("/transactions/{user_id}", response_model=List[Transaction], tags=["Transactions"])
def get_user_transactions(user_id: str, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Add this authorization check
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    """List all past transactions for a user."""
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user_transactions = db.query(models.Transaction).filter(models.Transaction.user_id == db_user.id).all()
    return user_transactions