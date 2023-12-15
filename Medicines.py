import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to the MySQL database (replace with your database details)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pharmacy"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create a table for medicines if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        quantity INT,
        price DECIMAL(10, 2)
    )
""")

# Function to add a new medicine to the inventory
def add_medicine():
    name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if name and quantity and price:
        cursor.execute("INSERT INTO medicines (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        db.commit()
        messagebox.showinfo("Success", f"{quantity} units of {name} added to the Pharmacy.")
        clear_entries()
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

# Function to view the inventory
def view_inventory():
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    if not medicines:
        result_text.set("Inventory is empty.")
    else:
        result_text.set("\nMedicine Inventory:\n\nID  | Medicine Name | Quantity | Price\n--------------------------------------")
        for medicine in medicines:
            result_text.set(result_text.get() + f"\n{medicine[0]:<3} | {medicine[1]:<14} | {medicine[2]:<8} | Rs.{medicine[3]:.2f}")

# Function to sell a medicine
def sell_medicine():
    medicine_id = entry_sell_id.get()
    quantity_sold = entry_sell_quantity.get()

    if medicine_id and quantity_sold:
        cursor.execute("SELECT * FROM medicines WHERE id = %s", (medicine_id,))
        medicine = cursor.fetchone()

        if medicine:
            if medicine[2] >= int(quantity_sold):
                total_price = int(quantity_sold) * medicine[3]
                result_text.set(f"\nSold {quantity_sold} units of {medicine[1]} for Rs.{total_price:.2f}")
                cursor.execute("UPDATE medicines SET quantity = quantity - %s WHERE id = %s", (quantity_sold, medicine_id))
                db.commit()
                clear_entries()
            else:
                messagebox.showwarning("Warning", "Insufficient quantity in stock.")
        else:
            messagebox.showwarning("Warning", "Medicine not found in Pharmacy.")
    else:
        messagebox.showwarning("Warning", "Please enter both ID and quantity.")

# Function to clear entry fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_sell_id.delete(0, tk.END)
    entry_sell_quantity.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Pharmacy Management System")

# Create and place labels and entry widgets
label_name = tk.Label(root, text="Medicine Name:")
label_name.grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)

label_quantity = tk.Label(root, text="Quantity:")
label_quantity.grid(row=1, column=0, padx=10, pady=10)
entry_quantity = tk.Entry(root)
entry_quantity.grid(row=1, column=1, padx=10, pady=10)

label_price = tk.Label(root, text="Price:")
label_price.grid(row=2, column=0, padx=10, pady=10)
entry_price = tk.Entry(root)
entry_price.grid(row=2, column=1, padx=10, pady=10)

# Sell section
label_sell_id = tk.Label(root, text="Medicine ID:")
label_sell_id.grid(row=0, column=2, padx=10, pady=10)
entry_sell_id = tk.Entry(root)
entry_sell_id.grid(row=0, column=3, padx=10, pady=10)

label_sell_quantity = tk.Label(root, text="Quantity to Sell:")
label_sell_quantity.grid(row=1, column=2, padx=10, pady=10)
entry_sell_quantity = tk.Entry(root)
entry_sell_quantity.grid(row=1, column=3, padx=10, pady=10)

# Create and place buttons
add_button = tk.Button(root, text="Add Medicine", command=add_medicine)
add_button.grid(row=3, column=0, pady=10)

view_button = tk.Button(root, text="View Inventory", command=view_inventory)
view_button.grid(row=3, column=1, pady=10)

sell_button = tk.Button(root, text="Sell Medicine", command=sell_medicine)
sell_button.grid(row=3, column=2, pady=10)

clear_button = tk.Button(root, text="Clear Entries", command=clear_entries)
clear_button.grid(row=3, column=3, pady=10)

# Create and place result text
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT)
result_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

# Run the GUI application
root.mainloop()

# Close the cursor and database connection
cursor.close()
db.close()