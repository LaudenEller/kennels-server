import sqlite3
import json
from models import Animal, Location

def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn: # This .connect() on the imported Sqlite library interface module
                                                        # is a method that is passing an argument of a path string that 
                                                        #   leads to my database file

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()                     # First variable with a new method being saved into new variable

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.customer_id,
                a.location_id,
                l.name location_name,
                l.address location_address
            FROM Animal a
            JOIN Location l
            ON l.id = a.location_id
            JOIN Customer c
            ON c.id = a.customer_id
                        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()                # db_cursor has value of Sql query from .execute(), converts results to data form set by line 12
                                                            # .fetchall() sets dataset to iterable python datatype

        for row in dataset:
            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['customer_id'], row['location_id'])

            # Create a Location instance from the current row
            location = Location(row['id'], row['location_name'], row['location_address'])

            # customer = Customer(row['id'], row['address'], row['name'], row['email'], row['password'])

            
            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            # animal.customer = customer.__dict__ 

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)
            
            # Compiling dictionaries as properties on dictionaries is called data composition....

        # Use `json` package to properly serialize list as JSON
        return json.dumps(animals)

def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.customer_id,
            a.status,
            a.location_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['customer_id'], data['status'],
                            data['location_id'])

        return json.dumps(animal.__dict__)
    
    
    # HOW CAN I TELL THE ALGO THAT LOCATION_ID IS A FOREIGN KEY, NOT A STRING SO THAT IT COMES IN AS AN INT???
    
def get_animal_by_location_id(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
    
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,            
                a.customer_id,
                a.status,
                a.location_id
            FROM animal a
            WHERE a.location_id = ?
            """, ( location_id, ))
        
        data = db_cursor.fetchall()
        
        for row in data:
        
            animal = Animal(row['id'], row['name'], row['breed'], row['customer_id'], row['status'], row['location_id'])
        
        return json.dumps(animal.__dict__)
    
def get_animal_by_status(string_variable):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
                
        db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,            
                a.customer_id,
                a.status,
                a.location_id
            FROM animal a
            WHERE a.status = ?
            """, ( string_variable, ))
        
        animals = []
        data = db_cursor.fetchall()
        
        for row in data:
        
            animal = Animal(row['id'], row['name'], row['breed'], row['customer_id'], row['status'], row['location_id'])
        
            animals.append(animal.__dict__)
        
        return json.dumps(animals)
    
def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))
        
def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
            WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
    
def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, status, breed, customer_id, location_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['status'],
              new_animal['breed'], new_animal['customerId'],
              new_animal['locationId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return json.dumps(new_animal)


# ANIMALS = [
#     {
#         "id": 1,
#         "name": "Snickers",
#         "species": "Dog",
#         "locationId": 1,
#         "customerId": 4,
#         "status": "Admitted"
#     },
#     {
#         "id": 2,
#         "name": "Gypsy",
#         "species": "Dog",
#         "locationId": 1,
#         "customerId": 2,
#         "status": "Admitted"
#     },
#     {
#         "id": 3,
#         "name": "Blue",
#         "species": "Cat",
#         "locationId": 2,
#         "customerId": 1,
#         "status": "Admitted"
#     }
# ]


# def get_all_animals():
#     return ANIMALS

# # Function with a single parameter
# def get_single_animal(id):
#     # Variable to hold the found animal, if it exists
#     requested_animal = None

#     # Iterate the ANIMALS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for animal in ANIMALS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if animal["id"] == id:
#             requested_animal = animal

#     return requested_animal

# def create_animal(animal):
#     # Get the id value of the last animal in the list
#     max_id = ANIMALS[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the animal dictionary
#     animal["id"] = new_id

#     # Add the animal dictionary to the list
#     ANIMALS.append(animal)

#     # Return the dictionary with `id` property added
#     return animal

# def delete_animal(id):
#     # Initial -1 value for animal index, in case one isn't found
#     animal_index = -1

#     # Iterate the ANIMALS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Store the current index.
#             animal_index = index

#     # If the animal was found, use pop(int) to remove it from list
#     if animal_index >= 0:
#         ANIMALS.pop(animal_index)
        
# def update_animal(id, new_animal):
#     # Iterate the ANIMALS list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, animal in enumerate(ANIMALS):
#         if animal["id"] == id:
#             # Found the animal. Update the value.
#             ANIMALS[index] = new_animal
#             break