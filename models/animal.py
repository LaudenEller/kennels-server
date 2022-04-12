class Animal():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, breed, customer_id, status = "", location_id = "", location = None, customer = None):
        self.id = id
        self.name = name
        self.breed = breed
        self.customer_id = customer_id
        self.status = status
        self.location_id = location_id
        self.location = location
        self.customer = customer