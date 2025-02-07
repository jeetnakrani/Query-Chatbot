import sqlite3

DB_NAME = "employees.db"

def process_query(user_input):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Normalize input to lowercase
    user_input = user_input.lower()

    try:
        if "employees in the" in user_input:
            dept = user_input.split("employees in the ")[1].split(" department")[0].strip().capitalize()
            cursor.execute("SELECT Name FROM Employees WHERE Department=?", (dept,))
            result = cursor.fetchall()
            return f"Employees in {dept}: " + ", ".join([row[0] for row in result]) if result else "No employees found."

        elif "manager of the" in user_input:
            dept = user_input.split("manager of the ")[1].split(" department")[0].strip().capitalize()
            cursor.execute("SELECT Manager FROM Departments WHERE Name=?", (dept,))
            result = cursor.fetchone()
            return f"Manager of {dept}: {result[0]}" if result else "Department not found."

        elif "hired after" in user_input:
            date = user_input.split("hired after ")[1].strip()
            cursor.execute("SELECT Name FROM Employees WHERE Hire_Date > ?", (date,))
            result = cursor.fetchall()
            return f"Employees hired after {date}: " + ", ".join([row[0] for row in result]) if result else "No employees found."

        elif "total salary expense for the" in user_input:
            dept = user_input.split("total salary expense for the ")[1].split(" department")[0].strip().capitalize()
            cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department=?", (dept,))
            result = cursor.fetchone()
            return f"Total salary expense for {dept}: {result[0]}" if result and result[0] else "Department not found."

        else:
            return "Sorry, I don't understand that query. Try asking about employees, managers, or salary."

    except Exception as e:
        return f"Error processing query: {str(e)}"

    finally:
        conn.close()
