import sqlite3
import json
from models import Customer

def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.address,
            a.name,
            a.email,
            a.password
        FROM customer a
        """)

        # Initialize an empty list to hold all customer representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an customer instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # customer class above.
            customer = Customer(row['id'], row['address'], row['name'], row['email'], row['password'])

            customers.append(customer.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(customers)

def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
       SELECT
            a.id,
            a.address,
            a.name,
            a.email,
            a.password
        FROM customer a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        customer = Customer(data['id'], data['address'], data['name'], data['email'], data['password'])

        return json.dumps(customer.__dict__)


def get_customers_by_name(name):
    
    # add an if that checks the name contains a space than split
    if name.__contains__("%20"):
        (customer_first_name, customer_last_name) = name.split("%20")
    #   fix name formatting to make Sql happy.
        name = f"{customer_first_name} {customer_last_name}"
    
    
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        select
            c.id,
            c.address,
            c.name,
            c.email,
            c.password
        from Customer c
        WHERE c.name LIKE ?
        """, (f'%{name}%', ))
        
        customers = []
        dataset = db_cursor.fetchall()
        
        
        for row in dataset:
            customer = Customer(row['id'], row['address'], row['name'], row['email'], row['password'])
            customers.append(customer.__dict__)
            
    return json.dumps(customers)


def get_customers_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.address,
            c.name,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['address'], row['name'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)


# CUSTOMERS = [
#         {
#             "id": 1,
#             "name": "Robert Platt"
#         },
#         {
#             "id": 2,
#             "name": "Saori Habuta"
#         }
#     ]

# def get_all_customers():
#     return CUSTOMERS

# # Function with a single parameter
# def get_single_customer(id):
#     # Variable to hold the found customer, if it exists
#     requested_customer = None

#     # Iterate the customerS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for customer in CUSTOMERS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if customer["id"] == id:
#             requested_customer = customer

#     return requested_customer

# def create_customer(customer):
#     # Get the id value of the last customer in the list
#     max_id = CUSTOMERS[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the customer dictionary
#     customer["id"] = new_id

#     # Add the customer dictionary to the list
#     CUSTOMERS.append(customer)

#     # Return the dictionary with `id` property added
#     return customer

# def delete_customer(id):
#     # Initial -1 value for customer index, in case one isn't found
#     customer_index = -1

#     # Iterate the customerS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, customer in enumerate(CUSTOMERS):
#         if customer["id"] == id:
#             # Found the customer. Store the current index.
#             customer_index = index

#     # If the customer was found, use pop(int) to remove it from list
#     if customer_index >= 0:
#         CUSTOMERS.pop(customer_index)
        
# def update_customer(id, new_customer):
#     # Iterate the customerS list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, customer in enumerate(CUSTOMERS):
#         if customer["id"] == id:
#             # Found the customer. Update the value.
#             CUSTOMERS[index] = new_customer
#             break