import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk, ImageSequence


class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Database")
        self.root.configure(bg="#0f1a2b")

        # Database
        self.conn = sqlite3.connect('pharmacy.db')
        self.cur = self.conn.cursor()
        self.create_tables()

        # Add pseudo data
        self.add_pseudo_data()

        # GUI
        self.create_gui()

        # Display GIF
        self.display_gif()

    # Existing methods...

    def display_gif(self):
        # Load the GIF
        gif_path = "1.gif"
        gif = Image.open(gif_path)

        # Convert GIF frames to Tkinter PhotoImage objects
        self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

        # Create a label to display the GIF
        self.gif_label = tk.Label(self.root)
        self.gif_label.pack()

        # Start the animation loop
        self.update_image(0)
    def update_image(self, index):
        frame = self.frames[index]
        self.gif_label.configure(image=frame)
        self.root.after(100, self.update_image, (index + 1) % len(self.frames))


    def create_tables(self):
        self.cur.executescript('''
            -- SQL queries for table creation
            CREATE TABLE IF NOT EXISTS Doctor (
                Doc_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                Pharmacy_name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Medicine (
                med_name TEXT PRIMARY KEY,
                price INTEGER NOT NULL,
                expired_date DATE NOT NULL,
                count INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Patient (
                Patient_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact_number TEXT NOT NULL,
                address TEXT NOT NULL,
                insurance_info TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Employee (
            Emp_id INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Contact TEXT NOT NULL,
            Shift TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Receipts (
            receipt_id INTEGER PRIMARY KEY,
            medicines TEXT NOT NULL,
            total_price INTEGER NOT NULL
            );
        ''')
        self.conn.commit()

    def add_pseudo_data(self):
        # Delete existing data from tables
        self.cur.execute("DELETE FROM Medicine")
        self.cur.execute("DELETE FROM Doctor")
        self.cur.execute("DELETE FROM Patient")

        # Add pseudo data to Medicine table

        self.cur.executemany("INSERT INTO Medicine VALUES (?, ?, ?, ?)", [
            ("Medicine A", 10, "2024-12-31", 50),
            ("Medicine B", 15, "2025-06-30", 30),
            ("Medicine C", 20, "2023-09-15", 25),
        ])

        # Add pseudo data to Doctor table
        self.cur.executemany("INSERT INTO Doctor VALUES (?, ?, ?, ?)", [
            (1, "Dr. Smith", "1234567890", "Pharmacy 1"),
            (2, "Dr. Johnson", "9876543210", "Pharmacy 2"),
            (3, "Dr. Brown", "5555555555", "Pharmacy 3"),
        ])

        # Add pseudo data to Patient table
        self.cur.executemany("INSERT INTO Patient VALUES (?, ?, ?, ?, ?)", [
            (1, "John Doe", "1112223333", "123 Main St", "Insurance 1"),
            (2, "Jane Smith", "4445556666", "456 Elm St", "Insurance 2"),
            (3, "Mike Johnson", "7778889999", "789 Oak St", "Insurance 3"),
        ])

        self.conn.commit()
    def create_employees_gui(self):
        # Employees Treeview
        self.employees_tree = ttk.Treeview(self.employees_tab, columns=("Name", "Age", "Contact", "Shift"))
        self.employees_tree.heading("#0", text="ID")
        self.employees_tree.heading("Name", text="Name")
        self.employees_tree.heading("Age", text="Age")
        self.employees_tree.heading("Contact", text="Contact")
        self.employees_tree.heading("Shift", text="Shift")
        self.employees_tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_employees_table()

        # Insert Employee button
        self.employee_insert_button = tk.Button(self.employees_tab, font=20, text="Add Employee", background="cadetblue", foreground="white", command=self.open_insert_employee_window)
        self.employee_insert_button.place(x=200, y=150)

    def show_all_data(self):
        self.refresh_medicine_table()
        self.refresh_doctors_table()
        self.refresh_patients_table()

    def create_medicine_gui(self):
        # Medicine Treeview
        self.medicine_tree = ttk.Treeview(self.medicine_tab, columns=("Price", "Expired Date", "Count"))
        self.medicine_tree.heading("#0", text="Name")
        self.medicine_tree.heading("Price", text="Price")
        self.medicine_tree.heading("Expired Date", text="Expired Date")
        self.medicine_tree.heading("Count", text="Count")
        self.medicine_tree.pack(fill=tk.BOTH, expand=True)
        self.medicine_tree.bind("<ButtonRelease-1>", self.select_medicine)
        self.refresh_medicine_table()

        # Insert Medicine button
        self.medicine_insert_button = tk.Button(self.medicine_tab,font=20 ,text="Insert Medicine",background="cadetblue",foreground="white", command=self.open_insert_medicine_window)
        self.medicine_insert_button.place(x=200,y=150)

        # Delete Medicine button
        self.medicine_delete_button = tk.Button(self.medicine_tab, font=20,text="Delete Medicine",background="cadetblue",foreground="white", command=self.delete_selected_medicine)
        self.medicine_delete_button.place(x=350,y=150)

        # Edit Medicine button
        self.medicine_edit_button = Button(self.medicine_tab,font=20, text="Edit Medicine",background="cadetblue",foreground="white", command=self.open_edit_medicine_window)
        self.medicine_edit_button.place(x=500,y=150)

        # Selected medicine variable
        self.selected_medicine = None

    def select_medicine(self, event):
        item = self.medicine_tree.selection()[0]
        self.selected_medicine = self.medicine_tree.item(item, "text")

    def open_insert_medicine_window(self):
        # Open a new window for inserting medicine
        insert_window = tk.Toplevel(self.root)
        insert_window.title("Insert Medicine")

        # Labels and entry fields for medicine details
        name_label = tk.Label(insert_window, text="Medicine Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(insert_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        price_label = tk.Label(insert_window, text="Price:")
        price_label.grid(row=1, column=0, padx=5, pady=5)
        price_entry = tk.Entry(insert_window)
        price_entry.grid(row=1, column=1, padx=5, pady=5)

        expiry_label = tk.Label(insert_window, text="Expiry Date:")
        expiry_label.grid(row=2, column=0, padx=5, pady=5)
        expiry_entry = tk.Entry(insert_window)
        expiry_entry.grid(row=2, column=1, padx=5, pady=5)

        count_label = tk.Label(insert_window, text="Count:")
        count_label.grid(row=3, column=0, padx=5, pady=5)
        count_entry = tk.Entry(insert_window)
        count_entry.grid(row=3, column=1, padx=5, pady=5)

        # Function to handle insertion
        def confirm_insertion():
            name = name_entry.get()
            price = int(price_entry.get())
            expiry = expiry_entry.get()
            count = int(count_entry.get())
            self.cur.execute("INSERT INTO Medicine VALUES (?, ?, ?, ?)", (name, price, expiry, count))
            self.conn.commit()
            self.refresh_medicine_table()
            insert_window.destroy()

        # Button to confirm insertion
        confirm_button = tk.Button(insert_window, text="Submit", command=confirm_insertion)
        confirm_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def create_gui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root, style='My.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        #***********************
        self.employees_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.employees_tab, text="Employees")
        self.create_employees_gui()

        self.create_receipt_tab()
        # Medicine tab
        self.medicine_tab = tk.Frame(self.notebook, bg="cadetblue")
        self.notebook.add(self.medicine_tab, text="Medicine")
        self.create_medicine_gui()

        # Doctors tab
        self.doctors_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.doctors_tab, text="Doctors")
        self.create_doctors_gui()

        # Patients tab
        self.patients_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.patients_tab, text="Patients")
        self.create_patients_gui()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        # Show all data button

        self.sell_button = tk.Button(self.medicine_tab, font=20, text="Sell", background="cadetblue", foreground="white", command=self.open_sell_window)
        self.sell_button.place(x=650, y=150)

        # Insert Patient button
        self.patient_insert_button = tk.Button(self.root, font=20, text="Add patient", background="cadetblue", foreground="white", command=self.open_insert_patient_window)
        self.patient_insert_button.place(x=780, y=200)
    def on_tab_selected(self, event):
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        if current_tab == "Patients":
            self.patient_insert_button = tk.Button(self.root, font=20, text="Add patient", background="cadetblue", foreground="white", command=self.open_insert_patient_window)
            self.patient_insert_button.place(x=780, y=200)
        else:
            if hasattr(self, 'patient_insert_button'):
                self.patient_insert_button.destroy()

    def sell_medicine(self):
        if self.selected_medicine:
            confirm = messagebox.askyesno("Confirm Sale", f"Are you sure you want to sell {self.selected_medicine}?")
            if confirm:
                # Update the count of the selected medicine
                self.cur.execute("UPDATE Medicine SET count = count - 1 WHERE med_name=?", (self.selected_medicine,))
                self.conn.commit()
                self.refresh_medicine_table()
    def open_sell_window(self):
        # Create a new window for selling medicine
        sell_window = tk.Toplevel(self.root)
        sell_window.title("Sell Medicine")

        # Create a listbox to display available medicines
        self.medicine_listbox = tk.Listbox(sell_window, selectmode=tk.MULTIPLE,width=30,height=15,font=20)
        self.medicine_listbox.pack(padx=10, pady=10)

        # Populate the listbox with available medicines
        self.cur.execute("SELECT med_name FROM Medicine")
        medicines = self.cur.fetchall()
        for medicine in medicines:
            self.medicine_listbox.insert(tk.END, medicine[0])

        # Declare total_price outside of the function
        total_price = 0

        # Function to handle the sale process
        def confirm_sale():
            nonlocal total_price  # Use nonlocal to access the total_price variable
            selected_indices = self.medicine_listbox.curselection()
            if len(selected_indices) == 0:
                messagebox.showwarning("No Selection", "Please select at least one medicine to sell.")
                return
            confirm = messagebox.askyesno("Confirm Sale", "Are you sure you want to sell the selected medicine(s)?")
            if confirm:
                # Iterate through selected medicines and update their counts in the database
                for index in selected_indices:
                    selected_medicine = self.medicine_listbox.get(index)
                    self.cur.execute("UPDATE Medicine SET count = count - 1 WHERE med_name=?", (selected_medicine,))
                    self.conn.commit()
                    self.refresh_medicine_table()
                    # Retrieve the price of the sold medicine and add it to the total price
                    self.cur.execute("SELECT price FROM Medicine WHERE med_name=?", (selected_medicine,))
                    price = self.cur.fetchone()[0]
                    total_price += price

                medicines_str = ", ".join(self.medicine_listbox.get(index) for index in selected_indices)
                self.cur.execute("INSERT INTO Receipts (medicines, total_price) VALUES (?, ?)", (medicines_str, total_price))
                self.conn.commit()
                # Show the total price
                messagebox.showinfo("Total Price", f"The total price is: ${total_price}")

                # Show the receipt
                show_receipt(selected_indices, total_price)

                # Close the sell window
                sell_window.destroy()

        # Button to confirm the sale
        confirm_button = tk.Button(sell_window, text="Sell", command=confirm_sale)
        confirm_button.pack(pady=10)



        # Function to show the receipt
        def show_receipt(selected_indices, total_price):
            receipt_window = tk.Toplevel(self.root)
            receipt_window.title("Receipt")

            receipt_text = "Receipt\n\n"
            for index in selected_indices:
                selected_medicine = self.medicine_listbox.get(index)
                # Retrieve the price of each selected medicine
                self.cur.execute("SELECT price FROM Medicine WHERE med_name=?", (selected_medicine,))
                price = self.cur.fetchone()[0]
                # Append each medicine with its individual price
                receipt_text += f"{selected_medicine}: ${price}\n"

            # Add the total price at the end
            receipt_text += f"\nTotal Price: ${total_price}"

            receipt_label = tk.Label(receipt_window, text=receipt_text,font=20,width=20,height=20)
            receipt_label.pack()

        # Button to calculate the total price and show the receipt
        receipt_button = tk.Button(sell_window, text="Show Receipt", command=lambda: show_receipt(self.medicine_listbox.curselection(), total_price))
        receipt_button.pack(pady=10)

    def create_receipt_tab(self):
        # Receipt tab
        self.receipt_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.receipt_tab, text="Receipt")

        # Create a text widget to display the receipt
        self.receipt_text = tk.Text(self.receipt_tab, wrap="word", width=40, height=20)
        self.receipt_text.pack(padx=10, pady=10)

        # Button to show all receipts
        self.show_all_receipts_button = tk.Button(self.receipt_tab, text="Show All Receipts", command=self.show_all_receipts)
        self.show_all_receipts_button.pack(pady=10)

    def show_all_receipts(self):
        self.receipt_text.delete("1.0", tk.END)  # Clear previous receipts
        self.cur.execute("SELECT * FROM Receipts")
        receipts = self.cur.fetchall()
        for receipt in receipts:
            receipt_text = f"Receipt ID: {receipt[0]}\n"
            receipt_text += f"Medicines: {receipt[1]}\n"
            receipt_text += f"Total Price: ${receipt[2]}\n\n"
            self.receipt_text.insert(tk.END, receipt_text)
    def open_insert_patient_window(self):
        # Open a new window for inserting patient details
        insert_window = tk.Toplevel(self.root)
        insert_window.title("Insert Patient")

        # Labels and entry fields for patient details
        name_label = tk.Label(insert_window, text="Patient Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(insert_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        contact_label = tk.Label(insert_window, text="Contact Number:")
        contact_label.grid(row=1, column=0, padx=5, pady=5)
        contact_entry = tk.Entry(insert_window)
        contact_entry.grid(row=1, column=1, padx=5, pady=5)

        address_label = tk.Label(insert_window, text="Address:")
        address_label.grid(row=2, column=0, padx=5, pady=5)
        address_entry = tk.Entry(insert_window)
        address_entry.grid(row=2, column=1, padx=5, pady=5)

        insurance_label = tk.Label(insert_window, text="Insurance Info:")
        insurance_label.grid(row=3, column=0, padx=5, pady=5)
        insurance_entry = tk.Entry(insert_window)
        insurance_entry.grid(row=3, column=1, padx=5, pady=5)

        # Function to handle insertion
        def confirm_insertion():
            name = name_entry.get()
            contact_number = contact_entry.get()
            address = address_entry.get()
            insurance_info = insurance_entry.get()
            self.cur.execute("INSERT INTO Patient (name, contact_number, address, insurance_info) VALUES (?, ?, ?, ?)", (name, contact_number, address, insurance_info))
            self.conn.commit()
            self.refresh_patients_table()
            insert_window.destroy()

        # Button to confirm insertion
        confirm_button = tk.Button(insert_window, text="Submit", command=confirm_insertion)
        confirm_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def refresh_medicine_table(self):
        self.medicine_tree.delete(*self.medicine_tree.get_children())
        self.cur.execute("SELECT * FROM Medicine")
        medicines = self.cur.fetchall()
        for medicine in medicines:
            self.medicine_tree.insert("", "end", text=medicine[0], values=(medicine[1], medicine[2],medicine[3]))

    def delete_selected_medicine(self):
        if self.selected_medicine:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {self.selected_medicine}?")
            if confirm:
                self.cur.execute("DELETE FROM Medicine WHERE med_name=?", (self.selected_medicine,))
                self.conn.commit()
                self.refresh_medicine_table()
                self.selected_medicine = None
    def open_insert_employee_window(self):
        # Open a new window for inserting employee details
        insert_window = tk.Toplevel(self.root)
        insert_window.title("Add Employee")

        # Labels and entry fields for employee details
        name_label = tk.Label(insert_window, text="Employee Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(insert_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        age_label = tk.Label(insert_window, text="Age:")
        age_label.grid(row=1, column=0, padx=5, pady=5)
        age_entry = tk.Entry(insert_window)
        age_entry.grid(row=1, column=1, padx=5, pady=5)

        contact_label = tk.Label(insert_window, text="Contact Number:")
        contact_label.grid(row=2, column=0, padx=5, pady=5)
        contact_entry = tk.Entry(insert_window)
        contact_entry.grid(row=2, column=1, padx=5, pady=5)

        shift_label = tk.Label(insert_window, text="Shift Time:")
        shift_label.grid(row=3, column=0, padx=5, pady=5)
        shift_entry = tk.Entry(insert_window)
        shift_entry.grid(row=3, column=1, padx=5, pady=5)
        def confirm_insertion():
            name = name_entry.get()
            age = int(age_entry.get())
            contact = contact_entry.get()
            shift = shift_entry.get()
            self.cur.execute("INSERT INTO Employee (Name, Age, Contact, Shift) VALUES (?, ?, ?, ?)", (name, age, contact, shift))
            self.conn.commit()
            self.refresh_employees_table()
            insert_window.destroy()
        # Button to confirm insertion
        confirm_button = tk.Button(insert_window, text="Submit", command=confirm_insertion)
        confirm_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def refresh_employees_table(self):
        self.employees_tree.delete(*self.employees_tree.get_children())
        self.cur.execute("SELECT * FROM Employee")
        employees = self.cur.fetchall()
        for employee in employees:
            self.employees_tree.insert("", "end", text=employee[0], values=(employee[1], employee[2], employee[3], employee[4]))
    def open_edit_medicine_window(self):
        if self.selected_medicine:
            # Open a new window for editing medicine
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Medicine")

            # Labels and entry fields for medicine details
            name_label = tk.Label(edit_window, text="Medicine Name:")
            name_label.grid(row=0, column=0, padx=5, pady=5)
            name_entry = tk.Entry(edit_window)
            name_entry.grid(row=0, column=1, padx=5, pady=5)
            name_entry.insert(0, self.selected_medicine)

            price_label = tk.Label(edit_window, text="Price:")
            price_label.grid(row=1, column=0, padx=5, pady=5)
            price_entry = tk.Entry(edit_window)
            price_entry.grid(row=1, column=1, padx=5, pady=5)

            expiry_label = tk.Label(edit_window, text="Expiry Date:")
            expiry_label.grid(row=2, column=0, padx=5, pady=5)
            expiry_entry = tk.Entry(edit_window)
            expiry_entry.grid(row=2, column=1, padx=5, pady=5)

            count_label = tk.Label(edit_window, text="Count:")
            count_label.grid(row=3, column=0, padx=5, pady=5)
            count_entry = tk.Entry(edit_window)
            count_entry.grid(row=3, column=1, padx=5, pady=5)

            # Function to handle editing
            def confirm_edit():
                price = int(price_entry.get())
                expiry = expiry_entry.get()
                count = int(count_entry.get())
                self.cur.execute("UPDATE Medicine SET price=?, expired_date=?, count=? WHERE med_name=?", (price, expiry, count, self.selected_medicine))
                self.conn.commit()
                self.refresh_medicine_table()
                edit_window.destroy()

            # Button to confirm editing
            confirm_button = tk.Button(edit_window, text="Submit", command=confirm_edit)
            confirm_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def create_doctors_gui(self):
        self.doctors_tree = ttk.Treeview(self.doctors_tab, columns=("Name", "Phone", "Pharmacy"))
        self.doctors_tree.heading("#0", text="ID")
        self.doctors_tree.heading("Name", text="Name")
        self.doctors_tree.heading("Phone", text="Phone")
        self.doctors_tree.heading("Pharmacy", text="Pharmacy")
        self.doctors_tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_doctors_table()

    def refresh_doctors_table(self):
        self.doctors_tree.delete(*self.doctors_tree.get_children())
        self.cur.execute("SELECT * FROM Doctor")
        doctors = self.cur.fetchall()
        for doctor in doctors:
            self.doctors_tree.insert("", "end", text=doctor[0], values=(doctor[1], doctor[2], doctor[3]))

    def create_patients_gui(self):
        self.patients_tree = ttk.Treeview(self.patients_tab, columns=("Name", "Contact Number", "Address", "Insurance Info"))
        self.patients_tree.heading("#0", text="ID")
        self.patients_tree.heading("Name", text="Name")
        self.patients_tree.heading("Contact Number", text="Contact Number")
        self.patients_tree.heading("Address", text="Address")
        self.patients_tree.heading("Insurance Info", text="Insurance Info")
        self.patients_tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_patients_table()

    def refresh_patients_table(self):
        self.patients_tree.delete(*self.patients_tree.get_children())
        self.cur.execute("SELECT * FROM Patient")
        patients = self.cur.fetchall()
        for patient in patients:
            self.patients_tree.insert("", "end", text=patient[0], values=(patient[1], patient[2], patient[3], patient[4]))

    def run(self):
        self.root.mainloop()

# Instantiate the PharmacyApp class and run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    app.run()
