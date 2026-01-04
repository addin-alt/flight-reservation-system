import sqlite3
from datetime import datetime, timedelta
import random

# ================= CONNECT =================
conn = sqlite3.connect("FRS.db")
cur = conn.cursor()

# ================= DROP TABLES IF EXIST =================
tables = ["Users", "Places", "Flights", "PassengerBookings"]
for t in tables:
    cur.execute(f"DROP TABLE IF EXISTS {t}")

# ================= USERS =================
cur.execute("""
CREATE TABLE Users(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE,
    Password TEXT,
    Role TEXT CHECK(Role IN ('User','Admin'))
)
""")

# ================= PLACES =================
cur.execute("""
CREATE TABLE Places(
    PlaceID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlaceName TEXT UNIQUE
)
""")
places = [
    "Dhaka","Chittagong","Khulna","Sylhet","Barishal",
    "Rajshahi","Rangpur","Mymensingh","Cox's Bazar",
    "Comilla","Gazipur","Narsingdi","Tangail","Patuakhali"
]
for p in places:
    cur.execute("INSERT INTO Places (PlaceName) VALUES (?)",(p,))

# ================= FLIGHTS =================
cur.execute("""
CREATE TABLE Flights(
    FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
    FlightName TEXT,
    Airline TEXT,
    Source TEXT,
    Destination TEXT,
    Departure TEXT,
    Arrival TEXT,
    SeatsAvailable INTEGER,
    Day TEXT,
    Date TEXT
)
""")

# Airlines and base flight names
airlines = ["Biman Bangladesh","US-Bangla","Novoair","Regent Airways","Sky Airlines"]
base_flight_names = ["101","202","303","404","505","606","707","808","909","010"]

# Days of week and next 7 dates
today = datetime.now()
days_of_week = [(today + timedelta(days=d)).strftime("%A") for d in range(1,8)]
dates_of_week = [(today + timedelta(days=d)).strftime("%Y-%m-%d") for d in range(1,8)]

# ================= CREATE FLIGHTS =================
for day_name, flight_date in zip(days_of_week, dates_of_week):
    for src in places:
        for dest in places:
            if src == dest:
                continue  # Skip same source/destination
            num_flights = random.randint(1,5)  # 1 to 5 flights per src/dest/day
            for _ in range(num_flights):
                airline = random.choice(airlines)
                flight_num = random.choice(base_flight_names)
                flight_name = f"{airline.split()[0]} {flight_num}"
                dep_hour = random.randint(6,18)
                arr_hour = dep_hour + 1
                seats = random.randint(60,70)
                cur.execute("""
                    INSERT INTO Flights 
                    (FlightName, Airline, Source, Destination, Departure, Arrival, SeatsAvailable, Day, Date)
                    VALUES (?,?,?,?,?,?,?,?,?)
                """, (flight_name, airline, src, dest, f"{dep_hour:02d}:00", f"{arr_hour:02d}:00", seats, day_name, flight_date))

# ================= PASSENGER BOOKINGS =================
cur.execute("""
CREATE TABLE PassengerBookings(
    BookingID TEXT PRIMARY KEY,
    UserID INTEGER,
    FlightID INTEGER,
    Status TEXT CHECK(Status IN ('Booked','Cancelled')) DEFAULT 'Booked',
    PaymentStatus TEXT CHECK(PaymentStatus IN ('Pending','Paid','Denied')) DEFAULT 'Pending',
    PaymentMethod TEXT,
    TransactionID TEXT,
    FOREIGN KEY(UserID) REFERENCES Users(UserID),
    FOREIGN KEY(FlightID) REFERENCES Flights(FlightID)
)
""")

conn.commit()
conn.close()
print("✅ FRS.db database created successfully!")
print("✅ Flights table now has 1-5 flights for every Source→Destination per day (next 7 days).")
