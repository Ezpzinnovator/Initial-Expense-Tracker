import sqlite3


def create_table():
    connection = sqlite3.connect("expenses.db")

    connection.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        expense_date TEXT
    )
    """)

    connection.close()


def add_expense(description, amount, category, expense_date):

    connection = sqlite3.connect("expenses.db")

    connection.execute(
        """
        INSERT INTO expenses
        (description, amount, category, expense_date)
        VALUES (?, ?, ?, ?)
        """,
        (description, amount, category, expense_date)
    )

    connection.commit()
    connection.close()


def get_expenses():

    connection = sqlite3.connect("expenses.db")

    expenses = connection.execute(
        """
        SELECT *
        FROM expenses
        ORDER BY expense_date DESC
        """
    ).fetchall()

    connection.close()

    return expenses


def get_expenses_by_date(from_date, to_date):

    connection = sqlite3.connect("expenses.db")

    expenses = connection.execute(
        """
        SELECT *
        FROM expenses
        WHERE expense_date BETWEEN ? AND ?
        ORDER BY expense_date DESC
        """,
        (from_date, to_date)
    ).fetchall()

    connection.close()

    return expenses


def get_expenses_by_category(category):

    connection = sqlite3.connect("expenses.db")

    expenses = connection.execute(
        """
        SELECT *
        FROM expenses
        WHERE category = ?
        ORDER BY expense_date DESC
        """,
        (category,)
    ).fetchall()

    connection.close()

    return expenses


def get_expenses_by_date_and_category(
    from_date,
    to_date,
    category
):

    connection = sqlite3.connect("expenses.db")

    expenses = connection.execute(
        """
        SELECT *
        FROM expenses
        WHERE expense_date BETWEEN ?
        AND ?
        AND category = ?
        ORDER BY expense_date DESC
        """,
        (
            from_date,
            to_date,
            category
        )
    ).fetchall()

    connection.close()

    return expenses


def delete_expense(expense_id):

    connection = sqlite3.connect("expenses.db")

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()


def get_total_expenses():

    connection = sqlite3.connect("expenses.db")

    total = connection.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()[0]

    connection.close()

    return total or 0


def get_total_expenses_by_date(
    from_date,
    to_date
):

    connection = sqlite3.connect("expenses.db")

    total = connection.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        WHERE expense_date BETWEEN ? AND ?
        """,
        (
            from_date,
            to_date
        )
    ).fetchone()[0]

    connection.close()

    return total or 0


def get_total_expenses_by_category(category):

    connection = sqlite3.connect("expenses.db")

    total = connection.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        WHERE category = ?
        """,
        (category,)
    ).fetchone()[0]

    connection.close()

    return total or 0


def get_total_expenses_by_date_and_category(
    from_date,
    to_date,
    category
):

    connection = sqlite3.connect("expenses.db")

    total = connection.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        WHERE expense_date BETWEEN ?
        AND ?
        AND category = ?
        """,
        (
            from_date,
            to_date,
            category
        )
    ).fetchone()[0]

    connection.close()

    return total or 0

def get_category_totals():

    connection = sqlite3.connect("expenses.db")

    category_totals = connection.execute(
        """
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
        """
    ).fetchall()

    connection.close()

    return category_totals

def update_expense(
    expense_id,
    description,
    amount,
    category,
    expense_date
):
    connection = sqlite3.connect("expenses.db")

    connection.execute(
        """
        UPDATE expenses
        SET
            description = ?,
            amount = ?,
            category = ?,
            expense_date = ?
        WHERE id = ?
        """,
        (
            description,
            amount,
            category,
            expense_date,
            expense_id
        )
    )

    connection.commit()
    connection.close()