import csv
import datetime
from HashMap import *
from truck import Truck
from package import Package
#starting location is the same for all trucks
STARTING_LOCATION = "4001 South 700 East"


def load_packages_from_csv(package_table):
    #load packages into hashtable from the csv
    with open("Packages.csv", newline='') as datafile:
       data = csv.reader(datafile)
       for row in data:
            package = Package(
                package_id=int(row[0]),
                address = row[1],
                city= row[2],
                state= row[3],
                zip_code=row[4],
                delivery_deadline=row[5],
                weight_kilo=row[6],
                special_notes=row[7] if len(row) > 7 else '')

            package_table.add(package.package_id, package)

def load_address_list():
    #load addresses into a list from the csv
    with open("Addresses.csv") as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        addresses = []
        for row in reader:
            addresses.append(row[1])
    return addresses


def load_distance_table():
    #load distance table
    with open("distance_data.csv") as file:
        reader = csv.reader(file)
        return list(reader)


def create_distance_matrix(distance_table):
    #create full distance matrix, easier to look through and use
    size = len(distance_table)
    new_matrix = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(len(distance_table[i])):
            value = distance_table[i][j]
            if value != '':
                distance = float(value)
                new_matrix[i][j] = distance
                new_matrix[j][i] = distance  # Mirror to make symmetric
    return new_matrix

def load_trucks(truck, package_table):
    #manually load packages onto the trucks and set start times
    if truck.truck_id == 1:
        truck_1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
        for package_id in truck_1_packages:
            truck.load_package(package_id)
            #start at 8am
            truck.start_time = datetime.datetime(hour=8,minute=0, year=2025, month=1, day=1)
            truck.current_time = truck.start_time
            package = package_table.get(package_id)
            package.truck_start_time = truck.start_time


    if truck.truck_id == 2:
        truck_2_packages = [3,6,18,25,28,32,36,38,5,2,4]
        for package_id in truck_2_packages:
            truck.load_package(package_id)
            #start at 9:05 for the late packages
            truck.start_time = datetime.datetime(hour=9,minute=5, year=2025, month=1, day=1)
            truck.current_time = truck.start_time
            package = package_table.get(package_id)
            package.truck_start_time = truck.start_time

    if truck.truck_id == 3:
        truck_3_packages = [7,8,9,10,11,12,17,21,22,23,24,26,27,33,35,39]
        for package_id in truck_3_packages:
            truck.load_package(package_id)
            #start at 11:08, truck 2 final stop is at 10:42, to get back to hub is 25.33+ minutes, rounded up to get 11:08 start time
            truck.start_time = datetime.datetime(hour=11, minute=8, year=2025, month=1, day=1)
            truck.current_time = truck.start_time
            package = package_table.get(package_id)
            package.truck_start_time = truck.start_time

    #get distance between two locations
def get_distance_between(address1, address2, address_list, distance_matrix):
     i = address_list.index(address1)
     j = address_list.index(address2)
     #print(f"This is i: {i}, and this is j: {j}") testing to make sure correct index
     return distance_matrix[i][j]


def deliver_packages(truck, package_table, distance_matrix, address_list):
    # starting location for  all trucks is the hub
    current_location = STARTING_LOCATION
    #while packages ie not empty
    while truck.packages:
        route = []
        min_distance = float('inf') #infinity
        nearest_package = None
        for package_id in truck.packages: #go through packages and sort
            package = package_table.get(package_id)
            distance = get_distance_between(current_location, package.address, address_list, distance_matrix)
            if distance < min_distance:
                min_distance = distance
                nearest_package = package
                nearest_package.set_status = "En-Route"
                # print(f"This is the nearest_package: {nearest_package}") (DEBUGGING PURPOSES)

        truck.add_miles(min_distance)
        #print(f"Delivering package: {nearest_package.package_id}, with the distance: {min_distance}") (DEBUGGING PURPOSES)
        truck.packages.remove(nearest_package.package_id)
        nearest_package.delivery_status = "Delivered"
        nearest_package.delivery_time = truck.current_time
        #print(f"Total distance traveled so far: {truck.total_distance}") (DEBUGGING PURPOSES)

        current_location = nearest_package.address
        truck.set_status(current_location)
        route.append(nearest_package)

    #get distance between last package and HUB for truck 3:
    #distance = get_distance_between(current_location, STARTING_LOCATION, address_list, distance_matrix)
    #print(f'Result of distance: {distance}')
    #print("Done")

    #CLI Report

def show_status_at_time(package_table, check_time, truck1, truck2, truck3):
    print("------------------------------------------")
    print(f"Delivery report of all packages at {check_time.strftime('%I:%M %p')}")
    print("------------------------------------------")

    for pkg_id in range(1, 41):  # assuming 40 packages
        package = package_table.get(pkg_id)
        if not package:
            continue

        if package.delivery_time and check_time >= package.delivery_time:
            status = f"Delivered at {package.delivery_time.strftime('%I:%M %p')}"
        elif package.truck_start_time and package.truck_start_time <= check_time:
            status = f"En route to delivery address, expected delivery at {package.delivery_time.strftime('%I:%M %p')}"
        else:
            status = f"At the hub Address: {package.address}"

        print(f"[Package ID = {package.package_id:<2}]  Delivery Status: {status}")
        print(f"Address: {package.address}  City: {package.city}  ZIP Code: {package.zip_code}  "
              f"Package Weight: {package.weight_kilo} kilograms  Delivery Deadline: {package.delivery_deadline}")
        print()

    # === Truck mileage summary ===
    print("--- Truck Mileage Summary ---")
    t1 = get_mileage_at_time(truck1, check_time)
    t2 = get_mileage_at_time(truck2, check_time)
    t3 = get_mileage_at_time(truck3, check_time)

    print(f"Truck 1 mileage at {check_time.strftime('%I:%M %p')}: {t1:.2f} miles")
    print(f"Truck 2 mileage at {check_time.strftime('%I:%M %p')}: {t2:.2f} miles")
    print(f"Truck 3 mileage at {check_time.strftime('%I:%M %p')}: {t3:.2f} miles")
    print(f"Combined mileage: {t1 + t2 + t3:.2f} miles")


    #get truck mileage at specific time
def get_mileage_at_time(truck, check_time):
    mileage = 0.0
    for t, dist in truck.route:
        if t <= check_time:
            mileage = dist
        else:
            break
    return mileage

    #lookup function for requirement
def lookup_package(package_table):
    try:
        package_id = int(input("Enter ID of package you are looking for: ").strip())
        package = package_table.get(package_id)
        if not package:
            print("Package not found!")
            return
        print("|~~~~~~~~~~~~~~~~~~~~~~~~|")
        print(" Package Lookup Result")
        print("|~~~~~~~~~~~~~~~~~~~~~~~~|")
        print(package)
    except ValueError:
        print("Please enter a number!")



    #main function
def main():
    #Create trucks
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)

    #create variable for the total combined mileage for all trucks:
    combined_truck_mileage = 0

    package_table =  HashMap()
    load_packages_from_csv(package_table)
    distance_table = load_distance_table()
    address_list=load_address_list()
    distance_matrix = create_distance_matrix(distance_table)

    #load trucks
    load_trucks(truck1, package_table)
    load_trucks(truck2, package_table)
    load_trucks(truck3, package_table)


    #deliver packages
    deliver_packages(truck1,package_table,distance_matrix,address_list)
    deliver_packages(truck2,package_table,distance_matrix,address_list)
    deliver_packages(truck3,package_table,distance_matrix,address_list)

   # print(truck1.current_time.strftime("%I:%M %p"))  # e.g., "08:35 AM"
    #print(truck1.total_distance)


    #add combined distances
    combined_truck_mileage+= truck1.total_distance
    combined_truck_mileage += truck2.total_distance
    combined_truck_mileage += truck3.total_distance
    #print(truck2.current_time.strftime("%I:%M %p"))  # e.g., "08:35 AM"
    #print(truck2.total_distance)


    #print(truck3.current_time.strftime("%I:%M %p"))  # e.g., "08:35 AM"
    #print(truck3.total_distance)


    print(f"The total combined milage is: {combined_truck_mileage}")

    print("\n=== Delivery CLI ===")
    print("1 - Show status of all packages (8:35 AM – 9:25 AM)")
    print("2 - Show status of all packages (9:35 AM – 10:25 AM)")
    print("3 - Show status of all packages (12:03 PM – 1:12 PM)")
    print("4 - Enter a custom time to check status (e.g., 10:15 AM)")
    print("5 - Enter a specific package_id you would like the info on!")
    print("x - Exit")

    #CLI
    while True:
        user_input = input("Choose an option (1/2/3/4/x): ").strip().lower()

        if user_input == '1':
            show_status_at_time(package_table, datetime.datetime(2025, 1, 1, 9, 10), truck1,truck2,truck3)

        elif user_input == '2':
            show_status_at_time(package_table, datetime.datetime(2025, 1, 1, 10, 0),truck1,truck2,truck3 )

        elif user_input == '3':
            show_status_at_time(package_table, datetime.datetime(2025, 1, 1, 12, 30), truck1,truck2,truck3)

        elif user_input == '4':
            time_str = input("Enter time (e.g., 08:45 AM): ").strip()
            try:
                custom_time = datetime.datetime.strptime(time_str, "%I:%M %p").replace(year=2025, month=1, day=1)
                show_status_at_time(package_table, custom_time, truck1,truck2,truck3)
            except ValueError:
                print("Invalid time format. Please use HH:MM AM/PM format (e.g., 10:45 AM)")
        elif user_input == '5':
            lookup_package(package_table)
        elif user_input == 'x':
            break

        else:
            print("Invalid input. Please choose 1, 2, 3, 4, or x.")


if __name__ == "__main__":
    main()
