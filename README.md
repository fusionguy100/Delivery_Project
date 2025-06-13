# WGUPS Delivery Routing Program

## Overview

This project simulates a real-world package delivery routing system for **Western Governors University Parcel Service (WGUPS)**. The goal is to optimize package deliveries using a custom routing algorithm and meet delivery deadlines, while considering business rules and constraints.



---

## Features

- Calculates the most efficient delivery routes using a greedy nearest-neighbor algorithm.
- Handles complex delivery constraints:
  - Delayed packages
  - Wrong address corrections (e.g., package #9)
  - Packages with delivery deadlines
  - Grouped packages that must be on the same truck
- Simulates the delivery process in real-time.
- Allows the user to check the status of any package at any time.

---

## Project Structure

```
/WGUPS-Delivery
│
├── main.py               # Main execution script
├── package.py            # Package class and package handling logic
├── truck.py              # Truck class and delivery logic
├── distance.py           # Handles distance calculations between addresses
├── hash_table.py         # Custom-built hash table for storing packages
├── data/
│   ├── addresses.csv     # Address/location list
│   ├── distances.csv     # Distance table between locations
│   └── packages.csv      # Package information
├── README.md             # Project documentation (this file)
└── requirements.txt      # Python dependencies (if applicable)
```

---

## Requirements

- Python 3.x

If you're using external packages (not typical for C950), include them in a `requirements.txt`.

---

## How to Run

1. Clone this repository or download the source files.
2. Make sure your CSV data files are placed in the `/data` folder.
3. Open a terminal and run:

```bash
python main.py
```

4. Follow the prompts to:
   - Check the status of all packages at a given time.
   - Look up a specific package.
   - View final delivery report and total mileage.

---

## Assumptions & Constraints

- The hub opens at **8:00 AM**. No deliveries start before this time.
- Each truck has a capacity of **16 packages**.
- Trucks travel at **18 mph**.
- **Two drivers are available**, so only **two trucks** can be on the road at a time.
- Delivery and loading times are **instantaneous**.
- Package #9’s address is corrected at **10:20 AM**.
- Total of **40 packages** must be delivered efficiently.

---

## Algorithms Used

- **Greedy Algorithm**: For choosing the nearest delivery location.
- **Hash Table**: Custom implementation for storing and retrieving package information in constant time.
- **Manual Constraint Handling**: Packages with time-sensitive or grouped constraints are pre-assigned to ensure accuracy.

---


---

## License

This project is intended for educational purposes only.
