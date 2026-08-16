
const API_URL = "http://127.0.0.1:8000";

// -----------------------------
// Add Expense
// -----------------------------
async function addExpense() {
    const category = document.getElementById("category").value.trim();
    const amount = parseFloat(document.getElementById("amount").value);
    const description = document.getElementById("description").value.trim();

    if (!category || !amount || amount <= 0 || !description) {
        alert("Please enter a valid category, amount, and description.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/expense`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                category: category,
                amount: amount,
                description: description
            })
        });

        if (!response.ok) {
            throw new Error("Failed to add expense");
        }

        alert("Expense added successfully!");

        document.getElementById("category").value = "";
        document.getElementById("amount").value = "";
        document.getElementById("description").value = "";

        loadDashboard();

    } catch (error) {
        console.error(error);
        alert("Could not add expense. Make sure the backend is running.");
    }
}


// -----------------------------
// Load Expenses
// -----------------------------
async function getExpenses() {
    try {
        const response = await fetch(`${API_URL}/expenses`);

        if (!response.ok) {
            throw new Error("Failed to fetch expenses");
        }

        const expenses = await response.json();

        const expenseList = document.getElementById("expense-list");

        expenseList.innerHTML = "";

        if (expenses.length === 0) {
            expenseList.innerHTML = "<p>No expenses recorded yet.</p>";
            return;
        }

        expenses.forEach(expense => {
            const expenseItem = document.createElement("div");

            expenseItem.className = "expense-item";

            expenseItem.innerHTML = `
                <div>
                    <strong>${escapeHTML(expense.category)}</strong>
                    - ${escapeHTML(expense.description)}
                    <br>
                    <span>₹${Number(expense.amount).toFixed(2)}</span>
                </div>

                <button onclick="deleteExpense(${expense.id})">
                    Delete
                </button>
            `;

            expenseList.appendChild(expenseItem);
        });

    } catch (error) {
        console.error(error);
        alert("Could not load expenses.");
    }
}


// -----------------------------
// Delete Expense
// -----------------------------
async function deleteExpense(id) {
    const confirmed = confirm("Are you sure you want to delete this expense?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/expense/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Failed to delete expense");
        }

        loadDashboard();

    } catch (error) {
        console.error(error);
        alert("Could not delete expense.");
    }
}


// -----------------------------
// Get Financial Summary
// -----------------------------
async function getSummary() {
    try {
        const response = await fetch(`${API_URL}/summary`);

        if (!response.ok) {
            throw new Error("Failed to fetch summary");
        }

        const data = await response.json();

        const totalElement = document.getElementById("total-spending");
        const highestElement = document.getElementById("highest-category");

        if (totalElement) {
            totalElement.textContent = `₹${Number(data.total_spending).toFixed(2)}`;
        }

        if (highestElement) {
            highestElement.textContent =
                data.highest_spending_category || "None";
        }

    } catch (error) {
        console.error(error);
    }
}


// -----------------------------
// Get AI Advice
// -----------------------------
async function getAIAdvice() {
    try {
        const response = await fetch(`${API_URL}/ai-advice`);

        if (!response.ok) {
            throw new Error("Failed to fetch AI advice");
        }

        const data = await response.json();

        const totalElement = document.getElementById("ai-total-spending");
        const categoryElement = document.getElementById("ai-highest-category");
        const adviceElement = document.getElementById("ai-advice");

        if (totalElement) {
            totalElement.textContent =
                `₹${Number(data.total_spending).toFixed(2)}`;
        }

        if (categoryElement) {
            categoryElement.textContent =
                data.highest_spending_category || "None";
        }

        if (adviceElement) {
            adviceElement.innerHTML = "";

            if (data.ai_advice && data.ai_advice.length > 0) {
                data.ai_advice.forEach(advice => {
                    const li = document.createElement("li");
                    li.textContent = advice;
                    adviceElement.appendChild(li);
                });
            } else {
                adviceElement.innerHTML =
                    "<li>No advice available yet.</li>";
            }
        }

    } catch (error) {
        console.error(error);
        alert("Could not load AI advice.");
    }
}


// -----------------------------
// Refresh Everything
// -----------------------------
function loadDashboard() {
    getExpenses();
    getSummary();
    getAIAdvice();
}


// -----------------------------
// Security helper
// -----------------------------
function escapeHTML(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


// -----------------------------
// Load dashboard when page opens
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});
