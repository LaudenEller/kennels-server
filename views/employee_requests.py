import sqlite3
import json
from models import Employee

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id
        FROM employee a
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # employee class above.
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)

def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
       SELECT
            a.id,
            a.name,
            a.address,
            a.location
        FROM employee a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(data['id'], data['name'], data['address'], data['email'], data['password'], data['location_id'])

        return json.dumps(employee.__dict__)



# EMPLOYEES = [
#         {
#             "id": 1,
#             "name": "Robert Platt"
#         },
#         {
#             "id": 2,
#             "name": "Saori Habuta"
#         }
#     ]

# def get_all_employees():
#     return EMPLOYEES

# # Function with a single parameter
# def get_single_employee(id):
#     # Variable to hold the found employee, if it exists
#     requested_employee = None

#     # Iterate the employeeS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for employee in EMPLOYEES:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if employee["id"] == id:
#             requested_employee = employee

#     return requested_employee

# def create_employee(employee):
#     # Get the id value of the last employee in the list
#     max_id = EMPLOYEES[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the employee dictionary
#     employee["id"] = new_id

#     # Add the employee dictionary to the list
#     EMPLOYEES.append(employee)

#     # Return the dictionary with `id` property added
#     return employee

# def delete_employee(id):
#     # Initial -1 value for employee index, in case one isn't found
#     employee_index = -1

#     # Iterate the employeeS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the employee. Store the current index.
#             employee_index = index

#     # If the employee was found, use pop(int) to remove it from list
#     if employee_index >= 0:
#         EMPLOYEES.pop(employee_index)
        
# def update_employee(id, new_employee):
#     # Iterate the employeeS list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the employee. Update the value.
#             EMPLOYEES[index] = new_employee
#             break