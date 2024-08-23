from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    interest_rate = Column(Float)
    duration = Column(Integer)
    borrower_id = Column(Integer, ForeignKey("users.id"))
    documents = Column(JSON)

class Collateral(Base):
    __tablename__ = "collaterals"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    value = Column(Float)
    loan_id = Column(Integer, ForeignKey("loans.id"))

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    date = Column(DateTime)


class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float, nullable=False)