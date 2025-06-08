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
            if self.special_notes.lower() in "delayed on flight":
                self.delivery_status = 'In air'
            else:
                self.delivery_status = 'At Hub'
            self.delivery_time = None
            self.truck_start_time = None
            self.assigned_truck = None


    #in conjunction without lookup function
    def __str__(self):
        return (f"Package({self.package_id}): {self.address}, {self.city}, {self.state} {self.zip_code} | "
                f"Deadline: {self.delivery_deadline} | Weight: {self.weight_kilo}kg | Notes: {self.special_notes} | "
                f"Delivery Status: {self.delivery_status} | Delivery Time: {self.delivery_time} | "
                f"On Truck: {self.assigned_truck}")




    def set_status(self,status):
        self.delivery_status = status

    # used for debugging purposes /redundant
    #def package_look_up(self, package_id):
        #print(self.address)