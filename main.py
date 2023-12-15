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
    name = input("Enter the name of the medicine: ")
    quantity = int(input("Enter the quantity: "))
    price = float(input("Enter the price: "))

    cursor.execute("INSERT INTO medicines (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    db.commit()
    print(f"{quantity} units of {name} added to the pharmacy.")

# Function to view the inventory
def view_inventory():
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    if not medicines:
        print("Inventory is empty.")
    else:
        print("\nMedicine Inventory:")
        print("ID  | Medicine Name | Quantity | Price")
        print("--------------------------------------")
        for medicine in medicines:
            print(f"{medicine[0]:<3} | {medicine[1]:<14} | {medicine[2]:<8} | ${medicine[3]:.2f}")

# Function to sell a medicine
def sell_medicine():
    view_inventory()
    medicine_id = int(input("Enter the ID of the medicine you want to sell: "))
    quantity_sold = int(input("Enter the quantity sold: "))

    cursor.execute("SELECT * FROM medicines WHERE id = %s", (medicine_id,))
    medicine = cursor.fetchone()

    if medicine:
        if medicine[2] >= quantity_sold:
            total_price = quantity_sold * medicine[3]
            print(f"\nSold {quantity_sold} units of {medicine[1]} for Rs.{total_price:.2f}")
            cursor.execute("UPDATE medicines SET quantity = quantity - %s WHERE id = %s", (quantity_sold, medicine_id))
            db.commit()
        else:
            print("Insufficient quantity in stock.")
    else:
        print("Medicine not found in inventory.")

# Menu-driven interface
while True:
    print("\nPharmacy Management System Menu:")
    print("1. Add Medicine to Inventory")
    print("2. View Inventory")
    print("3. Sell Medicine")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_medicine()
    elif choice == '2':
        view_inventory()
    elif choice == '3':
        sell_medicine()
    elif choice == '4':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")

# Close the cursor and database connection
cursor.close()
db.close()