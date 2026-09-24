from flask import Flask, render_template, request, redirect

from database import (
    add_expense,
    get_expenses,
    get_expenses_by_date,
    get_expenses_by_category,
    get_expenses_by_date_and_category,
    delete_expense,
    get_total_expenses,
    get_total_expenses_by_date,
    get_total_expenses_by_category,
    get_total_expenses_by_date_and_category,
    get_category_totals,
    update_expense
)


app = Flask(__name__)


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):

    delete_expense(expense_id)

    return redirect("/")


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit(expense_id):

    if request.method == "POST":

        description = request.form["description"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]

        try:
            amount = float(amount)

            if amount <= 0:
                return "Amount must be greater than 0."

            if amount > 100000000:
                return "Amount cannot be greater than ₹10 crore."

        except ValueError:
            return "Please enter a valid amount."

        update_expense(
            expense_id,
            description,
            amount,
            category,
            expense_date
        )

        return redirect("/")

    expenses = get_expenses()

    expense = None

    for item in expenses:

        if item[0] == expense_id:
            expense = item
            break

    if expense is None:
        return "Expense not found."

    return render_template(
        "edit.html",
        expense=expense
    )


@app.route("/", methods=["GET", "POST"])
def hello():

    if request.method == "POST":

        description = request.form["description"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]

        try:
            amount = float(amount)

            if amount <= 0:
                return "Amount must be greater than 0."

            if amount > 100000000:
                return "Amount cannot be greater than ₹10 crore."

        except ValueError:
            return "Please enter a valid amount."

        add_expense(
            description,
            amount,
            category,
            expense_date
        )

        print("Expense saved!")

    # Get filters

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    category_filter = request.args.get("category_filter")


    # No filters

    if not from_date and not to_date and not category_filter:

        expenses = get_expenses()

        total_expenses = get_total_expenses()


    # Date + Category

    elif from_date and to_date and category_filter:

        expenses = get_expenses_by_date_and_category(
            from_date,
            to_date,
            category_filter
        )

        total_expenses = get_total_expenses_by_date_and_category(
            from_date,
            to_date,
            category_filter
        )


    # Date only

    elif from_date and to_date:

        expenses = get_expenses_by_date(
            from_date,
            to_date
        )

        total_expenses = get_total_expenses_by_date(
            from_date,
            to_date
        )


    # Category only

    elif category_filter:

        expenses = get_expenses_by_category(
            category_filter
        )

        total_expenses = get_total_expenses_by_category(
            category_filter
        )


    # Incomplete filter

    else:

        expenses = get_expenses()

        total_expenses = get_total_expenses()


    # Get category totals

    category_totals = get_category_totals()


    return render_template(
        "index.html",
        expenses=expenses,
        total_expenses=total_expenses,
        category_totals=category_totals,
        from_date=from_date or "",
        to_date=to_date or "",
        category_filter=category_filter or ""
    )


if __name__ == "__main__":

    app.run(debug=True)