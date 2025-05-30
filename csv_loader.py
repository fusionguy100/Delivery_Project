import csv

from package import Package

def load_packages_from_csv():
    packages = []

    with open("WGUPS_Package_File_CLEAN.csv", newline='') as datafile:
       data = csv.reader(datafile)
       for row in data:
            package = Package(
                package_id=row[0]
                package.

            )





load_packages_from_csv()