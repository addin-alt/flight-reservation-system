import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, hashlib, uuid
from datetime import datetime, timedelta

# ================= THEME =================
BG = "#B1E8F4"
CARD = "#000000"
TEXT = "#000000"
INPUT_BG = "#000000"
PRIMARY = "#060A5D"
PRIMARY_H = "#D6A914"
DANGER = "#D7263D"
SUCCESS = "#02647A"

FONT_MAIN = ("Times New Roman", 14)
FONT_HEADER = ("Times New Roman", 20, "bold")

# ================= BUTTON =================
class HoverButton(tk.Label):
    def __init__(self, parent, text, command, bg, hover):
        super().__init__(parent, text=text, bg=bg, fg="white",
                         font=("Times New Roman", 13, "bold"),
                         padx=20, pady=10, cursor="hand2")
        self.command = command
        self.default_bg = bg
        self.hover_bg = hover
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))
        self.bind("<Button-1>", lambda e: self.command())

# ================= APP =================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IUBAT Flight Reservation System- by team Megas")
        self.geometry("1000x750")
        self.configure(bg=BG)
        self.user = None
        self.user_id = None
        self.show_home()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ---------- HOME ----------
    def show_home(self):
        self.clear()
        tk.Label(self, text="IUBAT Flight Reservation System", font=("Times New Roman", 28, "bold"),
                 bg=BG, fg=TEXT).pack(pady=50)

        HoverButton(self,"👤 User Login", self.user_login, PRIMARY, PRIMARY_H).pack(pady=15)
        HoverButton(self,"🛂 Admin Login", self.admin_login, PRIMARY, PRIMARY_H).pack(pady=15)
        HoverButton(self,"📝 Register", self.register, SUCCESS, "#007F99").pack(pady=15)

    # ---------- REGISTER ----------
    def register(self):
        self.clear()
        tk.Label(self, text="📝 Register", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=30)

        tk.Label(self, text="Username:", font=FONT_MAIN, bg=BG, fg=TEXT).pack(anchor="w", padx=150)
        u = tk.Entry(self, font=FONT_MAIN, bg=INPUT_BG)
        u.pack(padx=150, pady=5, fill="x")

        tk.Label(self, text="Password:", font=FONT_MAIN, bg=BG, fg=TEXT).pack(anchor="w", padx=150)
        p = tk.Entry(self, font=FONT_MAIN, show="*", bg=INPUT_BG)
        p.pack(padx=150, pady=5, fill="x")

        role_var = tk.StringVar(value="User")
        tk.Radiobutton(self, text="User", variable=role_var, value="User", bg=BG, fg=TEXT, font=FONT_MAIN).pack()
        tk.Radiobutton(self, text="Admin", variable=role_var, value="Admin", bg=BG, fg=TEXT, font=FONT_MAIN).pack()

        def save():
            db = sqlite3.connect("FRS.db")
            cur = db.cursor()
            try:
                cur.execute("INSERT INTO Users VALUES(NULL,?,?,?)",
                            (u.get(), hashlib.sha256(p.get().encode()).hexdigest(), role_var.get()))
                db.commit()
                messagebox.showinfo("✅ Success","Registered successfully!")
                self.show_home()
            except:
                messagebox.showerror("❌ Error","Username already exists!")
        HoverButton(self,"Register", save, SUCCESS, "#007F99").pack(pady=20)
        HoverButton(self,"← Back", self.show_home, DANGER, "#AA1E2D").pack()

    # ---------- LOGIN ----------
    def user_login(self): self.login("User")
    def admin_login(self): self.login("Admin")

    def login(self, role):
        self.clear()
        tk.Label(self, text=f"🔑 {role} Login", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=30)

        tk.Label(self, text="Username:", font=FONT_MAIN, bg=BG, fg=TEXT).pack(anchor="w", padx=150)
        u = tk.Entry(self, font=FONT_MAIN, bg=INPUT_BG)
        u.pack(padx=150, pady=5, fill="x")

        tk.Label(self, text="Password:", font=FONT_MAIN, bg=BG, fg=TEXT).pack(anchor="w", padx=150)
        p = tk.Entry(self, font=FONT_MAIN, show="*", bg=INPUT_BG)
        p.pack(padx=150, pady=5, fill="x")

        def go():
            db = sqlite3.connect("FRS.db"); cur = db.cursor()
            cur.execute("SELECT UserID,Role FROM Users WHERE Username=? AND Password=?",
                        (u.get(), hashlib.sha256(p.get().encode()).hexdigest()))
            r = cur.fetchone()
            if not r or r[1] != role:
                messagebox.showerror("❌ Error","Invalid username/password")
                return
            self.user = u.get()
            self.user_id = r[0]
            self.show_admin() if role=="Admin" else self.show_user()

        HoverButton(self,"Login", go, PRIMARY, PRIMARY_H).pack(pady=20)
        HoverButton(self,"← Back", self.show_home, DANGER, "#AA1E2D").pack()

    # ---------- USER PANEL ----------
    def show_user(self):
        self.clear()
        tk.Label(self, text=f"👋 Welcome, {self.user}", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)

        HoverButton(self,"🔍 Search Flights", self.user_search_flights, PRIMARY, PRIMARY_H).pack(pady=10)
        HoverButton(self,"🚪 Logout", self.logout, DANGER, "#AA1E2D").pack(pady=20)

    # ---------- USER SEARCH/BOOK/PAY/CANCEL ----------
    def user_search_flights(self):
        self.clear()
        tk.Label(self, text="🔍 Search Flights", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)

        db = sqlite3.connect("FRS.db"); cur = db.cursor()
        cur.execute("SELECT PlaceName FROM Places"); places = [r[0] for r in cur.fetchall()]

        tk.Label(self, text="Source:", font=FONT_MAIN, bg=BG, fg=TEXT).pack()
        source_cb = ttk.Combobox(self, values=places, font=FONT_MAIN)
        source_cb.pack(pady=5)

        tk.Label(self, text="Destination:", font=FONT_MAIN, bg=BG, fg=TEXT).pack()
        dest_cb = ttk.Combobox(self, values=places, font=FONT_MAIN)
        dest_cb.pack(pady=5)

        tk.Label(self, text="Day:", font=FONT_MAIN, bg=BG, fg=TEXT).pack()
        days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        day_cb = ttk.Combobox(self, values=days, font=FONT_MAIN)
        day_cb.pack(pady=5)

        flight_list = tk.Listbox(self, font=FONT_MAIN, width=100)
        flight_list.pack(pady=10)

        # ---------- SEARCH ----------
        def search():
            flight_list.delete(0, tk.END)
            cur.execute("""SELECT FlightID, FlightName, Departure, Arrival, SeatsAvailable, Date 
                           FROM Flights 
                           WHERE Source=? AND Destination=? AND Day=? AND SeatsAvailable>0""",
                        (source_cb.get(), dest_cb.get(), day_cb.get()))
            rows = cur.fetchall()
            if not rows:
                messagebox.showinfo("❌ No Flights","No flights found. Showing at least 3 available demo flights.")
                # Show first 3 flights as fallback
                cur.execute("SELECT FlightID, FlightName, Departure, Arrival, SeatsAvailable, Date FROM Flights LIMIT 3")
                rows = cur.fetchall()
            for r in rows:
                flight_list.insert(tk.END, f"{r[0]} | {r[1]} | {r[2]} → {r[3]} | Seats:{r[4]} | Date:{r[5]}")

        HoverButton(self,"Search", search, PRIMARY, PRIMARY_H).pack(pady=10)

        # ---------- BOOK ----------
        def book_flight():
            try:
                sel = flight_list.get(flight_list.curselection())
                flight_id = int(sel.split("|")[0].strip())
            except:
                messagebox.showerror("❌ Error","Select a flight first")
                return
            booking_id = str(uuid.uuid4())[:8]
            try:
                cur.execute("INSERT INTO PassengerBookings (BookingID, UserID, FlightID) VALUES (?,?,?)",
                            (booking_id, self.user_id, flight_id))
                cur.execute("UPDATE Flights SET SeatsAvailable=SeatsAvailable-1 WHERE FlightID=?",(flight_id,))
                db.commit()
                messagebox.showinfo("✅ Booked", f"Booking ID: {booking_id}\nProceed to payment.")
            except Exception as e:
                messagebox.showerror("❌ Error",str(e))
        HoverButton(self,"✈ Book Selected Flight", book_flight, SUCCESS, "#007F99").pack(pady=10)

        # ---------- PAYMENT ----------
        def pay_booking():
            try:
                sel = flight_list.get(flight_list.curselection())
                flight_id = int(sel.split("|")[0].strip())
            except:
                messagebox.showerror("❌ Error","Select a flight first")
                return
            cur.execute("SELECT BookingID, PaymentStatus FROM PassengerBookings WHERE UserID=? AND FlightID=?",
                        (self.user_id, flight_id))
            booking = cur.fetchone()
            if not booking:
                messagebox.showerror("❌ Error","No booking found for payment")
                return
            if booking[1]=="Paid":
                messagebox.showinfo("ℹ Already Paid","Booking is already paid")
                return

            def pay_demo(method):
                trans_id = str(uuid.uuid4())[:10]
                cur.execute("UPDATE PassengerBookings SET PaymentStatus='Paid', TransactionID=?, PaymentMethod=? WHERE BookingID=?",
                            (trans_id, method, booking[0]))
                db.commit()
                messagebox.showinfo("✅ Payment Confirmed", f"Transaction ID: {trans_id}\nMethod: {method}")

            pay_win = tk.Toplevel(self)
            pay_win.title("💳 Payment")
            pay_win.configure(bg=BG)
            tk.Label(pay_win, text="Select Payment Method", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
            HoverButton(pay_win,"💳 Card", lambda: pay_demo("Card"), PRIMARY, PRIMARY_H).pack(pady=10)
            HoverButton(pay_win,"📱 bKash", lambda: pay_demo("bKash"), SUCCESS, "#007F99").pack(pady=10)
            HoverButton(pay_win,"📱 Nagad", lambda: pay_demo("Nagad"), "#FFA500", "#CC8400").pack(pady=10)
            HoverButton(pay_win,"📱 Rocket", lambda: pay_demo("Rocket"), "#FF4500", "#CC3300").pack(pady=10)

        HoverButton(self,"💳 Pay Selected Booking", pay_booking, PRIMARY, PRIMARY_H).pack(pady=10)

        # ---------- CANCEL ----------
        def cancel_booking():
            try:
                sel = flight_list.get(flight_list.curselection())
                flight_id = int(sel.split("|")[0].strip())
            except:
                messagebox.showerror("❌ Error","Select a flight first")
                return
            cur.execute("SELECT BookingID, Status FROM PassengerBookings WHERE UserID=? AND FlightID=?",
                        (self.user_id, flight_id))
            booking = cur.fetchone()
            if not booking:
                messagebox.showerror("❌ Error","No booking found")
                return
            if booking[1]=="Cancelled":
                messagebox.showinfo("ℹ Already Cancelled","Booking is already cancelled")
                return
            cur.execute("UPDATE PassengerBookings SET Status='Cancelled' WHERE BookingID=?",(booking[0],))
            cur.execute("UPDATE Flights SET SeatsAvailable=SeatsAvailable+1 WHERE FlightID=?",(flight_id,))
            db.commit()
            messagebox.showinfo("✅ Cancelled","Booking has been cancelled")
        HoverButton(self,"❌ Cancel Selected Booking", cancel_booking, DANGER, "#AA1E2D").pack(pady=10)

        HoverButton(self,"← Back", self.show_user, DANGER, "#AA1E2D").pack(pady=20)

    # ---------- ADMIN PANEL ----------
    def show_admin(self):
        self.clear()
        tk.Label(self, text=f"👑 Admin Panel: {self.user}", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
        db = sqlite3.connect("FRS.db"); cur = db.cursor()

        HoverButton(self,"📋 View Bookings", self.admin_view_bookings, PRIMARY, PRIMARY_H).pack(pady=10)
        HoverButton(self,"➕ Add Flight", self.admin_add_flight, SUCCESS, "#007F99").pack(pady=10)
        HoverButton(self,"✏ Update Flight", self.admin_update_flight, "#FFA500", "#CC8400").pack(pady=10)
        HoverButton(self,"❌ Cancel Passenger Booking", self.admin_cancel_booking, DANGER, "#AA1E2D").pack(pady=10)
        HoverButton(self,"✅ Approve Payment", self.admin_approve_payment, SUCCESS, "#00BFFF").pack(pady=10)
        HoverButton(self,"🚫 Deny Payment", self.admin_deny_payment, DANGER, "#AA1E2D").pack(pady=10)
        HoverButton(self,"🚪 Logout", self.logout, DANGER, "#AA1E2D").pack(pady=20)

    # ================= ADMIN FUNCTIONALITIES =================
    # View all bookings
    def admin_view_bookings(self):
        self.clear()
        tk.Label(self, text="📋 All Bookings", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
        db = sqlite3.connect("FRS.db"); cur = db.cursor()
        box = tk.Text(self, width=110, height=25, font=FONT_MAIN)
        box.pack(padx=10, pady=10)
        cur.execute("""
            SELECT PB.BookingID, U.Username, F.FlightName, F.Source, F.Destination, F.Date,
                   PB.Status, PB.PaymentStatus, PB.PaymentMethod, PB.TransactionID
            FROM PassengerBookings PB
            JOIN Users U ON PB.UserID=U.UserID
            JOIN Flights F ON PB.FlightID=F.FlightID
        """)
        rows = cur.fetchall()
        for r in rows:
            box.insert(tk.END, f"{r}\n")
        HoverButton(self,"← Back", self.show_admin, DANGER, "#AA1E2D").pack(pady=10)

    # Add Flight
    def admin_add_flight(self):
        self.clear()
        tk.Label(self, text="➕ Add Flight", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
        db = sqlite3.connect("FRS.db"); cur = db.cursor()
        cur.execute("SELECT PlaceName FROM Places"); places = [r[0] for r in cur.fetchall()]

        entries = {}
        labels = ["Flight Name","Source","Destination","Departure","Arrival","Seats Available","Day","Date(YYYY-MM-DD)"]
        for lab in labels:
            tk.Label(self, text=lab, font=FONT_MAIN, bg=BG, fg=TEXT).pack()
            e = tk.Entry(self, font=FONT_MAIN, bg=INPUT_BG)
            e.pack(pady=3)
            entries[lab] = e

        # Combobox for Source and Destination
        src_cb = ttk.Combobox(self, values=places, font=FONT_MAIN); src_cb.pack()
        dst_cb = ttk.Combobox(self, values=places, font=FONT_MAIN); dst_cb.pack()
        entries["Source"] = src_cb; entries["Destination"] = dst_cb

        def save_flight():
            try:
                cur.execute("""
                    INSERT INTO Flights(FlightName,Source,Destination,Departure,Arrival,SeatsAvailable,Day,Date)
                    VALUES(?,?,?,?,?,?,?,?)
                """,(entries["Flight Name"].get(),entries["Source"].get(),entries["Destination"].get(),
                     entries["Departure"].get(),entries["Arrival"].get(),int(entries["Seats Available"].get()),
                     entries["Day"].get(),entries["Date(YYYY-MM-DD)"].get()))
                db.commit()
                messagebox.showinfo("✅ Added","Flight added successfully")
            except Exception as e:
                messagebox.showerror("❌ Error",str(e))
        HoverButton(self,"Save Flight", save_flight, SUCCESS, "#007F99").pack(pady=10)
        HoverButton(self,"← Back", self.show_admin, DANGER, "#AA1E2D").pack(pady=10)

    # Update Flight
    def admin_update_flight(self):
        self.clear()
        tk.Label(self, text="✏ Update Flight", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
        db = sqlite3.connect("FRS.db"); cur = db.cursor()
        cur.execute("SELECT FlightID, FlightName FROM Flights")
        flights = cur.fetchall()
        flight_cb = ttk.Combobox(self, values=[f"{f[0]}-{f[1]}" for f in flights], font=FONT_MAIN); flight_cb.pack(pady=5)

        entries = {}
        labels = ["Flight Name","Source","Destination","Departure","Arrival","Seats Available","Day","Date(YYYY-MM-DD)"]
        for lab in labels:
            tk.Label(self, text=lab, font=FONT_MAIN, bg=BG, fg=TEXT).pack()
            e = tk.Entry(self, font=FONT_MAIN, bg=INPUT_BG)
            e.pack(pady=3)
            entries[lab] = e

        def update_flight():
            try:
                flight_id = int(flight_cb.get().split("-")[0])
                cur.execute("""
                    UPDATE Flights SET FlightName=?, Source=?, Destination=?, Departure=?, Arrival=?, SeatsAvailable=?, Day=?, Date=? 
                    WHERE FlightID=?
                """,(entries["Flight Name"].get(),entries["Source"].get(),entries["Destination"].get(),
                    entries["Departure"].get(),entries["Arrival"].get(),int(entries["Seats Available"].get()),
                    entries["Day"].get(),entries["Date(YYYY-MM-DD)"].get(),flight_id))
                db.commit()
                messagebox.showinfo("✅ Updated","Flight updated successfully")
            except Exception as e:
                messagebox.showerror("❌ Error",str(e))
        HoverButton(self,"Update Flight", update_flight, "#FFA500", "#CC8400").pack(pady=10)
        HoverButton(self,"← Back", self.show_admin, DANGER, "#AA1E2D").pack(pady=10)

    # Cancel Passenger Booking
    def admin_cancel_booking(self):
        self.clear()
        tk.Label(self, text="❌ Cancel Passenger Booking", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
        db = sqlite3.connect("FRS.db"); cur = db.cursor()
        cur.execute("""SELECT PB.BookingID, U.Username, F.FlightName FROM PassengerBookings PB
                       JOIN Users U ON PB.UserID=U.UserID
                       JOIN Flights F ON PB.FlightID=F.FlightID""")
        bookings = cur.fetchall()
        book_cb = ttk.Combobox(self, values=[f"{b[0]}-{b[1]}-{b[2]}" for b in bookings], font=FONT_MAIN); book_cb.pack(pady=5)

        def cancel():
            try:
                booking_id = book_cb.get().split("-")[0]
                cur.execute("UPDATE PassengerBookings SET Status='Cancelled' WHERE BookingID=?",(booking_id,))
                # Increase seat
                cur.execute("SELECT FlightID FROM PassengerBookings WHERE BookingID=?",(booking_id,))
                flight_id = cur.fetchone()[0]
                cur.execute("UPDATE Flights SET SeatsAvailable=SeatsAvailable+1 WHERE FlightID=?",(flight_id,))
                db.commit()
                messagebox.showinfo("✅ Cancelled","Booking cancelled successfully")
            except Exception as e:
                messagebox.showerror("❌ Error",str(e))
        HoverButton(self,"Cancel Booking", cancel, DANGER, "#AA1E2D").pack(pady=10)
        HoverButton(self,"← Back", self.show_admin, DANGER, "#AA1E2D").pack(pady=10)

    # Approve Payment
    def admin_approve_payment(self):
        self.clear()
        tk.Label(self, text="✅ Approve Payment", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
        db = sqlite3.connect("FRS.db"); cur = db.cursor()
        cur.execute("""SELECT BookingID, UserID FROM PassengerBookings WHERE PaymentStatus='Pending'""")
        pending = cur.fetchall()
        if not pending: messagebox.showinfo("ℹ Info","No pending payments"); self.show_admin(); return
        book_cb = ttk.Combobox(self, values=[b[0] for b in pending], font=FONT_MAIN); book_cb.pack(pady=5)

        def approve():
            try:
                booking_id = book_cb.get()
                cur.execute("UPDATE PassengerBookings SET PaymentStatus='Paid', TransactionID=? WHERE BookingID=?",
                            (str(uuid.uuid4())[:10], booking_id))
                db.commit()
                messagebox.showinfo("✅ Approved","Payment approved")
            except Exception as e:
                messagebox.showerror("❌ Error",str(e))
        HoverButton(self,"Approve Payment", approve, SUCCESS, "#00BFFF").pack(pady=10)
        HoverButton(self,"← Back", self.show_admin, DANGER, "#AA1E2D").pack(pady=10)

    # Deny Payment
    def admin_deny_payment(self):
        self.clear()
        tk.Label(self, text="🚫 Deny Payment", font=FONT_HEADER, bg=BG, fg=TEXT).pack(pady=20)
        db = sqlite3.connect("FRS.db"); cur = db.cursor()
        cur.execute("""SELECT BookingID, UserID FROM PassengerBookings WHERE PaymentStatus='Pending'""")
        pending = cur.fetchall()
        if not pending: messagebox.showinfo("ℹ Info","No pending payments"); self.show_admin(); return
        book_cb = ttk.Combobox(self, values=[b[0] for b in pending], font=FONT_MAIN); book_cb.pack(pady=5)

        def deny():
            try:
                booking_id = book_cb.get()
                cur.execute("UPDATE PassengerBookings SET PaymentStatus='Denied' WHERE BookingID=?",(booking_id,))
                db.commit()
                messagebox.showinfo("✅ Denied","Payment denied")
            except Exception as e:
                messagebox.showerror("❌ Error",str(e))
        HoverButton(self,"Deny Payment", deny, DANGER, "#AA1E2D").pack(pady=10)
        HoverButton(self,"← Back", self.show_admin, DANGER, "#AA1E2D").pack(pady=10)

    # ---------- LOGOUT ----------
    def logout(self):
        self.user = None
        self.user_id = None
        self.show_home()


# ================= RUN =================
if __name__=="__main__":
    App().mainloop()
