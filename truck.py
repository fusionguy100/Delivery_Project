import datetime

class Truck:
    def __init__(self, truck_id, capacity=16, speed=18):
        self.truck_id = truck_id                # Truck number (1, 2, or 3)
        self.capacity = capacity                # Max number of packages
        self.speed = speed                      # MPH
        self.packages = []                      # List of package IDs
        self.current_location = "HUB"           # Start at the HUB
        self.total_distance = 0.0               # Track miles traveled
        self.route = []                         # Delivered packages in order
        self.start_time = None                  # Set in main.py
        self.current_time = None                # Will track delivery time

    def load_package(self, package_id):
        #Add package if it has room.
        if len(self.packages) < self.capacity:
            print(f"Loading package: {package_id}")
            self.packages.append(package_id)
            return True
        return print("Truck is full!")

    def set_status(self,address):
        self.current_location = address


    def add_miles(self, miles):
        #Update milage and time/speed
        self.total_distance += miles
        time_needed = datetime.timedelta(hours=miles / self.speed)
        if self.current_time:
            self.current_time += time_needed
        else:
            self.current_time = self.start_time + time_needed
    def current_packages(self):
        if self.packages:
            print(f"This truck currently has: ")
            for package in self.packages:
                print(f"{package}")
        else:
            print("This truck is empty!")