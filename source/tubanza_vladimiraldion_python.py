import sqlite3

def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect('pens_inventory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            ink_color TEXT NOT NULL,
            pen_type TEXT NOT NULL,
            cost REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def view_pens():
    """Retrieves and displays all pens."""
    conn = sqlite3.connect('pens_inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pens')
    records = cursor.fetchall()
    
    print("\n<== Current Pen Inventory ==>")
    if not records:
        print("The inventory is empty.")
    else:
        for record in records:
            print(f"ID: {record[0]} | Brand: {record[1]} | Ink: {record[2]} | Type: {record[3]} | Cost: P{record[4]:.2f}")
    print("<===========================>\n")
    conn.close()

def main():
    init_db()
    
    while True:
        print("=== Pen Inventory Menu ===")
        print("1. Add a new pen")
        print("2. View inventory")
        print("3. Edit a pen")
        print("4. Remove a pen")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1': # ADD
            brand = input("Enter brand: ")
            ink_color = input("Enter ink color (e.g. Red, Blue, ...): ")
            pen_type = input("Enter pen type (Ball, Nib, or Brush): ")
            try:
                cost = float(input("Enter cost (in PHP): "))
                conn = sqlite3.connect('pens_inventory.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Pens (brand, ink_color, pen_type, cost)
                    VALUES (?, ?, ?, ?)
                ''', (brand, ink_color, pen_type, cost))
                conn.commit()
                conn.close()
                print("Pen added successfully!\n")
            except ValueError:
                print("Invalid cost. Must be a number.\n")
                
        elif choice == '2': # CHECK
            view_pens()
            
        elif choice == '3': # EDIT
            view_pens()
            try:
                pen_id = int(input("Enter the ID of the pen to edit: "))
                brand = input("Enter new brand: ")
                ink_color = input("Enter new ink color: ")
                pen_type = input("Enter new pen type: ")
                cost = float(input("Enter new cost: "))
                
                conn = sqlite3.connect('pens_inventory.db')
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE Pens 
                    SET brand = ?, ink_color = ?, pen_type = ?, cost = ?
                    WHERE id = ?
                ''', (brand, ink_color, pen_type, cost, pen_id))
                
                if cursor.rowcount == 0:
                    print("No pen found with that ID.\n")
                else:
                    print("Pen updated successfully!\n")
                conn.commit()
                conn.close()
            except ValueError:
                print("Invalid input for ID or Cost. Must be a number.\n")
                
        elif choice == '4': # REMOVE
            view_pens()
            try:
                pen_id = int(input("Enter the ID of the pen to remove: "))
                conn = sqlite3.connect('pens_inventory.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Pens WHERE id = ?', (pen_id,))
                
                if cursor.rowcount == 0:
                    print("No pen found with that ID.\n")
                else:
                    print("Pen removed successfully!\n")
                conn.commit()
                conn.close()
            except ValueError:
                print("Invalid ID. Must be a number.\n")
                
        elif choice == '5': # EXIT
            print("Exiting program.")
            break
            
        else:
            print("Invalid choice. Please select a number from 1 to 5.\n")

if __name__ == '__main__':
    main()