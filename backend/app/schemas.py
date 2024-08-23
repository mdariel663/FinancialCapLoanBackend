from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Usuario
class UserBase(BaseModel):
    username: str
    password: str
    role: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

# Préstamo
class LoanBase(BaseModel):
    amount: float
    interest_rate: float
    duration: int
    borrower_id: int
    documents: Optional[List[str]] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int

    class Config:
        orm_mode = True

# Un artículo pignorado
class CollateralBase(BaseModel):
    description: str
    value: float
    loan_id: int

class CollateralCreate(CollateralBase):
    pass

class Collateral(CollateralBase):
    id: int

    class Config:
        orm_mode = True

# Transacción
class TransactionBase(BaseModel):
    amount: float
    loan_id: int
    date: datetime

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
        


class ReportCreate(BaseModel):
    description: str
    amount: float
    

class Report(BaseModel):
    id: int
    description: str
    amount: float