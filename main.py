#Jacob Newell, ID:011742870
import csv
import datetime
from HashMap import *
from truck import Truck
from package import Package

# starting location is the same for all trucks
STARTING_LOCATION = "4001 South 700 East"


def load_packages_from_csv(package_table):
    # load packages into hash table from the CSV
    with open("Packages.csv", newline='') as datafile:
        data = csv.reader(datafile)
        for row in data:
            package = Package(
                package_id=int(row[0]),
                address=row[1],
                city=row[2],
                state=row[3],
                zip_code=row[4],
                delivery_deadline=row[5],
                weight_kilo=row[6],
                special_notes=row[7] if len(row) > 7 else ''
            )
            package_table.add(package.package_id, package)


def load_address_list():
    # load addresses into a list from the CSV
    with open("Addresses.csv") as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # skip header
        addresses = [row[1] for row in reader]
    return addresses


def load_distance_table():
    #load distance table
    with open("distance_data.csv") as file:
        reader = csv.reader(file)
        return list(reader)


def create_distance_matrix(distance_table):
    #create full distance matrix, easier to look through and use
    size = len(distance_table)
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(len(distance_table[i])):
            if distance_table[i][j] != '':
                d = float(distance_table[i][j])
                matrix[i][j] = d
                matrix[j][i] = d
    return matrix


def load_trucks(truck, package_table):
    #manually load packages onto the trucks and set start times

    if truck.truck_id == 1:
        start = datetime.datetime(2025, 1, 1, 8, 0)
        # start at 8am
        truck.start_time = start
        truck.current_time = start
        truck_1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
        for package_id in truck_1_packages:
            truck.load_package(package_id)
            package = package_table.get(package_id)
            package.truck_start_time = start
            package.assigned_truck = truck.truck_id

    if truck.truck_id == 2:
        # start at 9:05 for the late packages
        start = datetime.datetime(2025, 1, 1, 9, 5)
        truck.start_time = start
        truck.current_time = start
        truck_2_packages = [3,6,18,25,28,32,36,38,5,2,4]
        for package_id in truck_2_packages:
            truck.load_package(package_id)
            package = package_table.get(package_id)
            package.truck_start_time = start
            package.assigned_truck = truck.truck_id


    if truck.truck_id == 3:
        # start at 11:08, truck 2 final stop is at 10:42, to get back to hub is 25.33+ minutes, rounded up to get 11:08 start time
        start = datetime.datetime(2025, 1, 1, 11, 8)
        truck.start_time = start
        truck.current_time = start
        truck_3_packages = [7,8,9,10,11,12,17,21,22,23,24,26,27,33,35,39]
        for package_id in truck_3_packages:
            truck.load_package(package_id)
            package = package_table.get(package_id)
            package.truck_start_time = start
            package.assigned_truck = truck.truck_id


    #get distance between two locations
def get_distance_between(addr1, addr2, address_list, distance_matrix):
    i = address_list.index(addr1)
    j = address_list.index(addr2)
    # print(f"This is i: {i}, and this is j: {j}") testing to make sure correct index
    return distance_matrix[i][j]


def deliver_packages(truck, package_table, distance_matrix, address_list):
    # starting location for  all trucks is the hub
    current_location = STARTING_LOCATION
    correction_time = datetime.datetime(
        truck.start_time.year,
        truck.start_time.month,
        truck.start_time.day,
        10,20
    )

    #Tracking if we've applied the correction to #9
    corrected = False

    #while packages ie not empty
    while truck.packages:
        #Before picking the next package, check if it’s time to correct #9
        if not corrected and truck.current_time >= correction_time and 9 in truck.packages:
            package9 = package_table.get(9)
            package9.address = "410 S State St"
            package9.zip_code = '84111'
            corrected = True  # don’t repeat

        min_distance = float('inf') #infinity
        nearest_package = None
        for package_id in truck.packages: #go through packages and sort
            package = package_table.get(package_id)
            distance = get_distance_between(current_location, package.address, address_list, distance_matrix)
            if distance < min_distance:
                min_distance = distance
                nearest_package = package
                # print(f"This is the nearest_package: {nearest_package}") (DEBUGGING PURPOSES)


        # drive to nearest
        truck.add_miles(min_distance)
        #print(f"Delivering package: {nearest_package.package_id}, with the distance: {min_distance}") (DEBUGGING PURPOSES)
        truck.packages.remove(nearest_package.package_id)
        nearest_package.delivery_status = "Delivered"
        nearest_package.delivery_time = truck.current_time
        #print(f"Total distance traveled so far: {truck.total_distance}") (DEBUGGING PURPOSES)

        current_location = nearest_package.address
        truck.set_status(current_location)
        truck.route.append((truck.current_time, truck.total_distance))
        # get distance between last package and HUB for truck 3:
        # distance = get_distance_between(current_location, STARTING_LOCATION, address_list, distance_matrix)
        # print(f'Result of distance: {distance}')
        # print("Done")



        #CLI REPORT
def show_status_at_time(package_table, check_time, truck1, truck2, truck3):
    print("------------------------------------------")
    print(f"Delivery report of all packages at {check_time.strftime('%I:%M %p')}")
    print("------------------------------------------")

    for pkg_id in range(1, 41):
        package = package_table.get(pkg_id)
        if not package:
            continue

        # 1) In Air if delayed on flight and before its truck departs
        if ("delayed on flight" in package.special_notes.lower()
                and package.truck_start_time
                and check_time < package.truck_start_time):
            status = "In Air"

        # 2) Delivered by check_time
        elif package.delivery_time and check_time >= package.delivery_time:
            status = f"Delivered at {package.delivery_time.strftime('%I:%M %p')}"

        # 3) En Route if truck has left but package not yet delivered
        elif package.truck_start_time and check_time >= package.truck_start_time:
            status = "En Route"

        # 4) Still at Hub otherwise
        else:
            status = "At Hub"

        print(f"[Package ID = {package.package_id:<2}] Truck: {package.assigned_truck} | Delivery Status: {status}")
        print(f" Address: {package.address}  City: {package.city}  ZIP: {package.zip_code}")
        print(f" Weight: {package.weight_kilo} kg  Deadline: {package.delivery_deadline}")
        print()

    #get truck mileage at specific time
    def get_mileage_at_time(truck):
        m = 0.0
        for t, dist in truck.route:
            if t <= check_time:
                m = dist
            else:
                break
        return m

    t1 = get_mileage_at_time(truck1)
    t2 = get_mileage_at_time(truck2)
    t3 = get_mileage_at_time(truck3)
    print("--- Truck Mileage Summary ---")
    print(f"Truck 1: {t1:.2f} miles")
    print(f"Truck 2: {t2:.2f} miles")
    print(f"Truck 3: {t3:.2f} miles")
    print(f"Combined: {t1 + t2 + t3:.2f} miles\n")


    #lookup function for requirement
def lookup_package(package_table):
    try:
        package_id = int(input("Enter ID of package to look up: ").strip())
        package = package_table.get(package_id)
        if not package:
            print("Package not found!")
            return
        print("|~~~~~~~~~~~~~~~~~~~~~~~~|")
        print("Package Lookup Result:")
        print(package)
        print("|~~~~~~~~~~~~~~~~~~~~~~~~|")
    except ValueError:
        print("Please enter a valid number!")


    #main function
def main():
    # Create trucks
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)

    package_table = HashMap()
    load_packages_from_csv(package_table)

    address_list = load_address_list()
    raw_dist = load_distance_table()
    distance_matrix = create_distance_matrix(raw_dist)

    # load packages & set start times
    for t in (truck1, truck2, truck3):
        load_trucks(t, package_table)

    # perform deliveries
    deliver_packages(truck1, package_table, distance_matrix, address_list)
    deliver_packages(truck2, package_table, distance_matrix, address_list)
    deliver_packages(truck3, package_table, distance_matrix, address_list)

    # interactive CLI
    print("=== Delivery CLI ===")
    print("1: Status at 9:00 AM")
    print("2: Status at 10:00 AM")
    print("3: Status at 12:30 PM")
    print("4: Custom time")
    print("5: Lookup one package")
    print("x: Exit")

    while True:
        choice = input("Choose (1/2/3/4/5/x): ").lower().strip()
        if choice == '1':
            ct = datetime.datetime(2025, 1, 1, 9, 0)
            show_status_at_time(package_table, ct, truck1, truck2, truck3)
        elif choice == '2':
            ct = datetime.datetime(2025, 1, 1, 10, 0)
            show_status_at_time(package_table, ct, truck1, truck2, truck3)
        elif choice == '3':
            ct = datetime.datetime(2025, 1, 1, 12, 30)
            show_status_at_time(package_table, ct, truck1, truck2, truck3)
        elif choice == '4':
            ts = input("Enter time (HH:MM AM/PM): ").strip()
            try:
                ct = datetime.datetime.strptime(ts, "%I:%M %p").replace(year=2025, month=1, day=1)
                show_status_at_time(package_table, ct, truck1, truck2, truck3)
            except ValueError:
                print("Invalid format; use HH:MM AM/PM.")
        elif choice == '5':
            lookup_package(package_table)
        elif choice == 'x':
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
