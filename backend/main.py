from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Base
from models import Expense


app = FastAPI(title="AI Finance Advisor API")

# Create database tables
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
    return {
        "message": "AI Finance Advisor API is running!"
    }


# -----------------------------
# Add Expense
# -----------------------------

@app.post("/expense")
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):

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


# -----------------------------
# Get all expenses
# -----------------------------

@app.get("/expenses")
def get_expenses(
    db: Session = Depends(get_db)
):

    expenses = db.query(Expense).all()

    return expenses


# -----------------------------
# Delete expense
# -----------------------------

@app.delete("/expense/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )

    if expense is None:
        return {
            "message": "Expense not found"
        }

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully",
        "id": expense_id
    }


# -----------------------------
# Spending summary
# -----------------------------

@app.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):

    expenses = db.query(Expense).all()

    total = sum(
        expense.amount
        for expense in expenses
    )

    category_totals = {}

    for expense in expenses:

        category = expense.category

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense.amount

    highest_category = None

    if category_totals:
        highest_category = max(
            category_totals,
            key=category_totals.get
        )

    return {
        "total_spending": round(total, 2),
        "category_spending": {
            category: round(amount, 2)
            for category, amount in category_totals.items()
        },
        "highest_spending_category": highest_category
    }


# -----------------------------
# Financial advice
# -----------------------------

@app.get("/advice")
def get_advice(
    db: Session = Depends(get_db)
):

    expenses = db.query(Expense).all()

    if not expenses:
        return {
            "message": "No expenses found.",
            "advice": [
                "Start tracking your expenses to receive financial advice."
            ]
        }

    total = sum(
        expense.amount
        for expense in expenses
    )

    category_totals = {}

    for expense in expenses:

        category = expense.category

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense.amount

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_amount = category_totals[highest_category]

    highest_percentage = (
        highest_amount / total
    ) * 100

    advice = []

    # Highest spending category
    advice.append(
        f"{highest_category} is your highest spending category, "
        f"accounting for {highest_percentage:.1f}% of your spending."
    )

    # Spending concentration
    if highest_percentage >= 50:

        advice.append(
            f"More than half of your spending is on {highest_category}. "
            "Consider setting a budget limit for this category."
        )

    elif highest_percentage >= 30:

        advice.append(
            f"{highest_category} represents a significant portion "
            "of your spending. Monitor this category closely."
        )

    else:

        advice.append(
            "Your spending is reasonably distributed across categories."
        )

    # Category-specific recommendations
    for category, amount in category_totals.items():

        percentage = (
            amount / total
        ) * 100

        category_lower = category.lower()

        if category_lower in [
            "food",
            "dining",
            "restaurant"
        ]:

            if percentage >= 30:

                advice.append(
                    "Your food spending is relatively high. "
                    "Consider preparing more meals at home "
                    "and setting a weekly food budget."
                )

        elif category_lower in [
            "shopping",
            "entertainment"
        ]:

            if percentage >= 20:

                advice.append(
                    f"{category} accounts for {percentage:.1f}% "
                    "of your spending. Consider reducing "
                    "non-essential purchases."
                )

        elif category_lower in [
            "travel",
            "vacation"
        ]:

            if percentage >= 25:

                advice.append(
                    "Travel expenses are taking a significant "
                    "portion of your spending. Consider planning "
                    "a separate travel budget."
                )

        elif category_lower in [
            "transport",
            "transportation"
        ]:

            if percentage >= 20:

                advice.append(
                    "Transportation costs are significant. "
                    "Consider using public transport or "
                    "combining trips where possible."
                )

    # Overall spending advice
    if total >= 10000:

        advice.append(
            "Your recorded spending is relatively high. "
            "Review your largest categories and identify "
            "expenses that can be reduced."
        )

    else:

        advice.append(
            "Keep tracking your expenses regularly to "
            "identify spending patterns and improve your savings."
        )

    return {
        "total_spending": round(total, 2),

        "category_spending": {
            category: round(amount, 2)
            for category, amount in category_totals.items()
        },

        "highest_spending_category": highest_category,

        "advice": advice
    }


# -----------------------------
# AI-style financial advice
# FREE VERSION
# -----------------------------

@app.get("/ai-advice")
def get_ai_advice(
    db: Session = Depends(get_db)
):

    expenses = db.query(Expense).all()

    if not expenses:

        return {
            "message": "No expenses found.",
            "ai_advice": [
                "Start adding expenses so the system can analyze your spending."
            ]
        }

    total = sum(
        expense.amount
        for expense in expenses
    )

    category_totals = {}

    for expense in expenses:

        category = expense.category

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense.amount

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    highest_amount = category_totals[highest_category]

    highest_percentage = (
        highest_amount / total
    ) * 100

    recommendations = []

    # Main recommendation
    if highest_percentage >= 50:

        recommendations.append(
            f"Your spending is heavily concentrated in "
            f"{highest_category}. Try reducing spending in "
            "this category and set a monthly budget."
        )

    elif highest_percentage >= 30:

        recommendations.append(
            f"{highest_category} is your largest expense category. "
            "Monitor it carefully and consider setting a spending limit."
        )

    else:

        recommendations.append(
            "Your expenses are distributed across several categories. "
            "Continue tracking them to maintain good spending habits."
        )

    # Analyze categories
    for category, amount in category_totals.items():

        percentage = (
            amount / total
        ) * 100

        category_lower = category.lower()

        if category_lower in [
            "food",
            "dining",
            "restaurant"
        ]:

            if percentage >= 30:

                recommendations.append(
                    "Food spending is high. Consider cooking at home "
                    "more often and setting a weekly food budget."
                )

        elif category_lower in [
            "shopping",
            "entertainment"
        ]:

            if percentage >= 20:

                recommendations.append(
                    f"{category} makes up {percentage:.1f}% of your spending. "
                    "Consider reducing unnecessary purchases."
                )

        elif category_lower in [
            "transport",
            "transportation"
        ]:

            if percentage >= 20:

                recommendations.append(
                    "Transportation costs are significant. "
                    "Look for cheaper transportation alternatives."
                )

    # Savings recommendation
    recommendations.append(
        "A good goal is to review your expenses regularly and "
        "allocate part of your income toward savings before "
        "spending on non-essential items."
    )

    return {

        "analysis": "Personalized financial analysis",

        "total_spending": round(total, 2),

        "highest_spending_category": highest_category,

        "highest_category_percentage": round(
            highest_percentage,
            2
        ),

        "category_spending": {
            category: round(amount, 2)
            for category, amount in category_totals.items()
        },

        "ai_advice": recommendations
    }