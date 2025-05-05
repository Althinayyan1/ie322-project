import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import random
import datetime

# Room prices per night
room_prices = {
    "Standard": 100,
    "Deluxe": 150,
    "Suite": 200
}

def calculate_total_price(nights, room_type, discount_percent=0):
    price_per_night = room_prices.get(room_type, 0)
    total_before_discount = nights * price_per_night
    discount_amount = total_before_discount * (discount_percent / 100)
    total_after_discount = total_before_discount - discount_amount
    return total_before_discount, discount_amount, total_after_discount

def reserve_room():
    guest_name = entry_name.get().strip()
    room_type = room_var.get()
    check_in_date = check_in.get_date()
    check_out_date = check_out.get_date()
    entered_code = entry_discount.get().strip()

    if not guest_name or room_type == "Select a room":
        messagebox.showwarning("Warning", "Please enter your name and select a room type.")
        return

    if check_out_date <= check_in_date:
        messagebox.showerror("Error", "Check-out date must be after Check-in date.")
        return

    nights = (check_out_date - check_in_date).days
    valid_discount = 20 if entered_code.startswith("UHOTEL-") else 0
    new_discount_code = f"UHOTEL-{random.randint(1000, 9999)}"

    total_before, discount_amount, final_price = calculate_total_price(nights, room_type, valid_discount)

    message = f"""
Reservation Successful!
Guest Name: {guest_name}
Room Type: {room_type}
Check-in: {check_in_date.strftime('%Y-%m-%d')}
Check-out: {check_out_date.strftime('%Y-%m-%d')}
Nights: {nights}
Total Before Discount: ${total_before:.2f}
Discount Applied: {valid_discount}% (${discount_amount:.2f})
Final Price: ${final_price:.2f}

🎁 Your Discount Code for Next Time: {new_discount_code}
"""

    messagebox.showinfo("Reservation Confirmed", message)

    with open("reservations.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {guest_name} - {room_type} - {nights} nights - {check_in_date} to {check_out_date} - ${final_price:.2f} - Used: {entered_code or 'None'} - New Code: {new_discount_code}\n")

# Function to clear inputs
def clear_fields():
    entry_name.delete(0, tk.END)
    room_var.set("Select a room")
    check_in.set_date(datetime.date.today())
    check_out.set_date(datetime.date.today())
    entry_discount.delete(0, tk.END)

# Create main window
window = tk.Tk()
window.title("U Hotel - Room Reservation")
window.geometry("450x600")
window.resizable(False, False)

# Title
tk.Label(window, text="U Hotel Reservation", font=("Segoe UI", 18, "bold")).pack(pady=10)

# Guest Name
tk.Label(window, text="Guest Name:", font=("Segoe UI", 12)).pack()
entry_name = tk.Entry(window, font=("Segoe UI", 12), width=30)
entry_name.pack(pady=5)

# Room Type
tk.Label(window, text="Room Type:", font=("Segoe UI", 12)).pack()
room_var = tk.StringVar(value="Select a room")
room_options = ["Standard", "Deluxe", "Suite"]
room_menu = tk.OptionMenu(window, room_var, *room_options)
room_menu.config(font=("Segoe UI", 12))
room_menu.pack(pady=5)

# Check-in Date
tk.Label(window, text="Check-in Date:", font=("Segoe UI", 12)).pack()
check_in = DateEntry(window, font=("Segoe UI", 12), width=20, background='darkblue', foreground='white', borderwidth=2)
check_in.pack(pady=5)

# Check-out Date
tk.Label(window, text="Check-out Date:", font=("Segoe UI", 12)).pack()
check_out = DateEntry(window, font=("Segoe UI", 12), width=20, background='darkblue', foreground='white', borderwidth=2)
check_out.pack(pady=5)

# Discount Code
tk.Label(window, text="Enter Discount Code (Optional):", font=("Segoe UI", 12)).pack(pady=5)
entry_discount = tk.Entry(window, font=("Segoe UI", 12), width=30)
entry_discount.pack(pady=5)

# Reserve Button
tk.Button(window, text="Reserve", font=("Segoe UI", 12, "bold"), command=reserve_room, width=20).pack(pady=10)

# Clear All Inputs Button
tk.Button(window, text="Clear All Inputs", font=("Segoe UI", 12), command=clear_fields, width=20).pack(pady=5)

# Exit Button (NEW)
tk.Button(window, text="Exit", font=("Segoe UI", 12), command=window.quit, width=20).pack(pady=5)

# Footer
tk.Label(window, text="Thank you for choosing U Hotel!", font=("Segoe UI", 10), fg="gray").pack(side="bottom", pady=10)

# Run the app
window.mainloop()


