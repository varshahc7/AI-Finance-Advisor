from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine
from models import Expense

app = FastAPI(title="AI Finance Advisor API")


# Create database tables
from database import Base
Base.metadata.create_all(bind=engine)


# -----------------------------
# Database session
# -----------------------------

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Expense schema
# -----------------------------

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    description: str


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {"message": "AI Finance Advisor API is running!"}


# -----------------------------
# Add Expense
# -----------------------------

@app.post("/expense")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):

    new_expense = Expense(
        category=expense.category,
        amount=expense.amount,
        description=expense.description
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return {
        "message": "Expense added successfully",
        "expense": {
            "id": new_expense.id,
            "category": new_expense.category,
            "amount": new_expense.amount,
            "description": new_expense.description
        }
    }
@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):

    expenses = db.query(Expense).all()

    return expenses
@app.delete("/expense/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):

    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        return {"message": "Expense not found"}

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully",
        "id": expense_id
    }