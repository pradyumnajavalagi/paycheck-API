from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base

# Define the database URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./paycheck.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    name = Column(String)
    # Add this new field
    hashed_password = Column(String) 
    
    # We don't need the credit_balance field for now
    # credit_balance = Column(Float)

    bills = relationship("Bill", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, unique=True, index=True)
    amount = Column(Float)
    status = Column(Enum("DUE", "PAID", name="bill_status_enum"), default="DUE")
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bills")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    amount = Column(Float)
    status = Column(Enum("SUCCESS", "FAILED", name="txn_status_enum"))

    user_id = Column(Integer, ForeignKey("users.id"))
    bill_id = Column(Integer, ForeignKey("bills.id"))
    
    owner = relationship("User", back_populates="transactions")