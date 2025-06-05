import csv
from datetime import *

from HashMap import *
from truck import Truck
from package import Package
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

def load_trucks(truck):
    #manually load packages onto the trucks
    truck_1_packages = [1,6,13,14,15,16,19,20,29,30,31,34]
    for package in truck_1_packages:
        truck.load_package(package)


def get_distance_between(address1, address2, address_list, distance_matrix):
     i = address_list.index(address1)
     j = address_list.index(address2)
     #print(f"This is i: {i}, and this is j: {j}") testing to make sure correct index
     return distance_matrix[i][j]


def deliver_packages(truck, package_table, distance_matrix, address_list):
    #
    current_location = STARTING_LOCATION



    while truck.packages:
        route = []
        min_distance = 999
        nearest_package = None
        for package_id in truck.packages:
            package = package_table.get(package_id)
            distance = get_distance_between(current_location,package.address, address_list,distance_matrix)
            if distance < min_distance:
                min_distance =  distance
                nearest_package = package
                #print(f"This is the nearest_package: {nearest_package}")




        truck.packages.remove(nearest_package.id)
        truck.add_miles(min_distance)
        current_location = nearest_package
        truck.set_status(current_location)
        route.append(nearest_package)

    print("DOne")

def main():
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)
    package_table =  HashMap()
    load_packages_from_csv(package_table)
    distance_table = load_distance_table()
    address_list=load_address_list()
    print(address_list)
    distance_matrix = create_distance_matrix(distance_table)
    load_trucks(truck1)
    df1 = package_table.get(1)

    deliver_packages(truck1,package_table,distance_matrix,address_list)

if __name__ == "__main__":
    main()
