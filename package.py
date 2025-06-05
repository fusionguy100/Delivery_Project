class Package:
    #Constructor for packages
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight_kilo, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight_kilo = weight_kilo
        self.special_notes = special_notes
        self.delivery_status = 'At Hub'
        self.delivery_time = None

    def __str__(self):
        return (f"Package({self.package_id}): {self.address}, {self.city}, {self.state} {self.zip_code} | "
                f"Deadline: {self.delivery_deadline} | Weight: {self.weight_kilo}kg | Notes: {self.special_notes} | "
                f"Delivery Status: {self.delivery_status} | Delivery Time: {self.delivery_time}")


    def set_status(self,status):
        self.delivery_status = status


    def package_look_up(self, package_id):
        print(self.address)