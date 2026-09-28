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
    get_category_totals_by_date,
    get_category_totals_by_category,
    get_category_totals_by_date_and_category,
    get_daily_totals,
    update_expense
)


app = Flask(__name__)


# =================================
# DELETE EXPENSE
# =================================

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):

    delete_expense(expense_id)

    return redirect("/")


# =================================
# EDIT EXPENSE
# =================================

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


# =================================
# MAIN DASHBOARD
# =================================

@app.route("/", methods=["GET", "POST"])
def hello():

    # =================================
    # ADD EXPENSE
    # =================================

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

        return redirect("/")


    # =================================
    # FILTER VALUES
    # =================================

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    category_filter = request.args.get("category_filter")


    # =================================
    # NO FILTER
    # =================================

    if not from_date and not to_date and not category_filter:

        expenses = get_expenses()

        total_expenses = get_total_expenses()

        category_totals = get_category_totals()


    # =================================
    # DATE + CATEGORY
    # =================================

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

        category_totals = get_category_totals_by_date_and_category(
            from_date,
            to_date,
            category_filter
        )


    # =================================
    # DATE ONLY
    # =================================

    elif from_date and to_date:

        expenses = get_expenses_by_date(
            from_date,
            to_date
        )

        total_expenses = get_total_expenses_by_date(
            from_date,
            to_date
        )

        category_totals = get_category_totals_by_date(
            from_date,
            to_date
        )


    # =================================
    # CATEGORY ONLY
    # =================================

    elif category_filter:

        expenses = get_expenses_by_category(
            category_filter
        )

        total_expenses = get_total_expenses_by_category(
            category_filter
        )

        category_totals = get_category_totals_by_category(
            category_filter
        )


    # =================================
    # INCOMPLETE DATE FILTER
    # =================================

    else:

        expenses = get_expenses()

        total_expenses = get_total_expenses()

        category_totals = get_category_totals()


    # =================================
    # DAILY SPENDING DATA
    # =================================

    daily_totals = get_daily_totals(
        from_date=from_date,
        to_date=to_date,
        category=category_filter
    )


    # =================================
    # SPENDING INSIGHTS
    # =================================

    highest_category = None
    highest_category_amount = 0

    if category_totals:

        highest_category = category_totals[0][0]
        highest_category_amount = category_totals[0][1]


    highest_spending_day = None
    highest_spending_day_amount = 0

    if daily_totals:

        highest_day = max(
            daily_totals,
            key=lambda item: item[1]
        )

        highest_spending_day = highest_day[0]
        highest_spending_day_amount = highest_day[1]


    average_daily_spending = 0

    if daily_totals:

        average_daily_spending = (
            sum(
                item[1]
                for item in daily_totals
            )
            /
            len(daily_totals)
        )


    # =================================
    # SEND DATA TO HTML
    # =================================

    return render_template(
        "index.html",

        expenses=expenses,

        total_expenses=total_expenses,

        category_totals=category_totals,

        daily_totals=daily_totals,

        highest_category=highest_category,

        highest_category_amount=highest_category_amount,

        highest_spending_day=highest_spending_day,

        highest_spending_day_amount=highest_spending_day_amount,

        average_daily_spending=average_daily_spending,

        from_date=from_date or "",

        to_date=to_date or "",

        category_filter=category_filter or ""
    )


# =================================
# START FLASK
# =================================

if __name__ == "__main__":

    app.run(debug=True)