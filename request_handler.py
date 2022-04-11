from curses import raw
from http.server import BaseHTTPRequestHandler, HTTPServer
import imp
import json
from views.animal_requests import get_all_animals, get_single_animal, get_animal_by_location_id # create_animal, delete_animal, update_animal
from views.location_requests import get_all_locations, get_single_location # create_location, delete_location, update_location
from views.employee_requests import get_all_employees, get_single_employee # create_employee, delete_employee, update_employee
from views.customers_requests import get_all_customers, get_single_customer, get_customers_by_email, get_customers_by_name # create_customer, delete_customer, update_customer



# WHY DID MY TWO NEW LOCATION ROWS GET IDS 3 & 4 EVEN THOUGH I DELETED THE FIRST TWO ROWS BEFORE CREATING THE NEW ONES?
# WHAT IS MY IMP IMPORT?



# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""
    
    
    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]


        #  DO I NEED TO ADD ANOTHER CONDITIONAL PARAMETER TO THE IF ON LINE 39? OR MAYBE A NESTED CONDITIONAL CHECKING RESOURCE CONTENT??


        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            raw_value = pair[1]  # 'jenna@solis.com'
            
            try:
                raw_value = int(raw_value)
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

    
            return ( resource, key, raw_value ) # Tuple with a table name, a column name and a column value

        # No query string parameter
        else:
            id = None
    # Try to get the item at index 2
            try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
                id = int(path_params[2])
                
                # WHAT IS GOING ON BELOW?
                
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)   # This is a tuple
    

    # Here's a class method
    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
            
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        
        # ARE THESE PREDEFINED METHODS(?)? - GETS METHODS FROM INHERITED CLASS
        
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
   
    def do_GET(self):
        # HOW IS THE METHODS _SET_HEADERS_ GETTING USED ON THIS LINE? - initial header code value
        self._set_headers(200)

        response = {}       # Default response - initial response value

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)       # DOES PATH COME FROM POSTMAN? - yes

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
             # Parse the URL and capture the tuple that is returned
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = f"{get_customers_by_email(value)}"
            elif key == "name" and resource == "customers":
                response = f"{get_customers_by_name(value)}"
            elif key == "location_id" and resource == "animals":
                response = f"{get_animal_by_location_id(value)}"

        self.wfile.write(response.encode())     #WHAT DOES THIS DO?? RESPONSE === LIST OF DICTIONARIES

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0)) # WHAT DOES THIS DO?
        post_body = self.rfile.read(content_len) # WHAT DOES THIS DO?? - READ METHOD ON RFILE PROPETY OF INHERITED CLASS

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new dictionary
        response = None
        # Add a new resource to the list for each possible expected request
        if resource == "animals":
            response = create_animal(post_body)
        if resource == "customers":
            response = create_customer(post_body)
        if resource == "employees":
            response = create_employee(post_body)
        if resource == "locations":
            response = create_location(post_body)
            
            # Encode the new animal and send in response
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)
        if resource == "employees":
            update_employee(id, post_body)
        if resource == "customers":
            update_customer(id, post_body)
        if resource == "locations":
            update_location(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        if resource == "customers":
            delete_customer(id)
        if resource == "employees":
            delete_employee(id)
        if resource == "locations":
            delete_location(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever() # This is a new class that is getting HandleRequests class passed as one of the arguments


# Does this invokes the main function because __name__ is __main__ somewhere else in my code?
if __name__ == "__main__":
    main()
