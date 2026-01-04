# Flight Reservation System (FRS)

A **Python Tkinter-based Flight Reservation System** with SQLite backend, allowing **Users** to search, book, pay, and cancel flights, and **Admins** to manage flights, bookings, and payments. Fully functional, end-to-end, with a user-friendly GUI.

---

## 🖥 Features

### User Features
- Register and login as a user.
- Search flights by **source, destination, and day**.
- Book selected flights.
- Make payments using multiple methods (Card, bKash, Nagad, Rocket).
- Cancel booked flights.
- Real-time seat availability management.
- Fallback: displays at least 3 demo flights if no exact match is found.

### Admin Features
- Register and login as an admin.
- View all bookings.
- Add new flights with source, destination, departure/arrival times, seats, day, and date.
- Update existing flights.
- Cancel passenger bookings.
- Approve or deny pending payments.

---

## 🛠 Technologies Used
- **Python 3**  
- **Tkinter** – GUI framework  
- **SQLite3** – Database management  
- **uuid & hashlib** – Unique IDs and password hashing

---

## 🗂 Project Structure

FRS/
│
├─ app.py # Main application with GUI and all functionalities
├─ db_setup.py # Script to generate and populate the database
├─ FRS.db # SQLite database (created by db_setup.py)
└─ README.md # Project documentation


---

## ⚡ Installation

1. Clone the repository:

```bash
git clone https://github.com/addin-alt/flight-reservation-system.git
cd flight-reservation-system
Make sure you have Python 3 installed.

Install dependencies (Tkinter is usually bundled with Python):

pip install tk
Run the database setup to create FRS.db:

python db_setup.py
Run the main application:

python app.py
🧑‍💻 Usage
User
Open the application and click User Login or Register.

Login with your credentials.

Search for flights by selecting Source, Destination, and Day.

Select a flight and Book.

Make payment by selecting a method.

Cancel booking if needed.

Admin
Login as admin.

Access the admin panel:

View Bookings – See all user bookings.

Add Flight – Add new flights.

Update Flight – Modify flight details.

Cancel Booking – Cancel any passenger booking.

Approve/Deny Payments – Manage pending payments.

📊 Database Schema
Tables:

Users

UserID | Username | Password | Role
Places


PlaceID | PlaceName
Flights


FlightID | FlightName | Source | Destination | Departure | Arrival | SeatsAvailable | Day | Date
PassengerBookings

BookingID | UserID | FlightID | Status | PaymentStatus | TransactionID | PaymentMethod
🔐 Security
Passwords are hashed using SHA-256 before storage.

Unique booking IDs and transaction IDs generated with UUID.

🎨 UI / UX
Clean and minimal design with Times New Roman fonts.

Hover buttons for better interactivity.

Popups inform users about actions (errors, confirmations, info).

🚀 Future Improvements
Integrate real payment gateways (bKash, Nagad).

Add flight filtering by time or price.

Export bookings to CSV/PDF.

Multi-user login sessions.

📌 Author
Al Addin

Email: info.addincse@gmail.com

GitHub: addin-alt

📄 License
This project is open-source under the MIT License.




---

