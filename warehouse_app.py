import tkinter as tk
from math import expm1
from tkinter import ttk, messagebox, simpledialog
from database import get_connection

from dml_statements import (
    INSERT_CLIENT, INSERT_AGREEMENT,
    DELETE_AGREEMENT, DELETE_MOVEMENT,
    UPDATE_PRODUCT, UPDATE_FACILITY
)

from query import (
    QUERY_1_MAX_INDUSTRY,
    QUERY_2_NO_ACTIVITY,
    QUERY_3_MAX_STAFF_MOVEMENTS,
    QUERY_4_MANUFACTURERS_NO_STORAGE,
    QUERY_5_PRODUCTS_PER_FACILITY,
    QUERY_6_CLIENT_TOTAL_QUANTITY
)


class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smartwarehouse")
        self.root.geometry("900x600")

        self.root.call('source', 'forest-dark.tcl')

        self.connection = get_connection()

        self.setup_ui()

    def setup_ui(self):
        # main left frame for buttons
        left_frame = ttk.Frame(self.root, width=250, padding=10)
        left_frame.pack(side='left', fill='y')

        # Right side for the results
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.pack(side='right', fill='both', expand=True)

        # Treeview for SELECT results
        self.tree = ttk.Treeview(right_frame, show='headings')
        self.tree.pack(fill='both', expand=True)

        # Scrollbar for the tree
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        ttk.Style().theme_use('forest-dark')

        # Now add buttons in left_frame
        self.create_buttons(left_frame)

        pass

    def create_buttons(self, frame):

        ttk.Label(frame, text="DML Operations", font=('Arial', 12, 'bold')).pack(pady=5)

        ttk.Button(frame, text="Add Client", command=self.add_client).pack(fill='x', pady=2)
        ttk.Button(frame, text="Add Agreement", command=self.add_agreement).pack(fill='x', pady=2)
        ttk.Button(frame, text="Delete Agreement", command=self.delete_agreement).pack(fill='x', pady=2)
        ttk.Button(frame, text="Delete Movement", command=self.delete_movement).pack(fill='x', pady=2)
        ttk.Button(frame, text="Update Product", command=self.update_product).pack(fill='x', pady=2)
        ttk.Button(frame, text="Update Facility", command=self.update_facility).pack(fill='x', pady=2)

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

        ttk.Label(frame, text="Business Reports", font=('Arial', 12, 'bold')).pack(pady=5, anchor='s')

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=0)

        ttk.Label(frame, text="Select:", font=('Arial', 12)).pack(pady=5,anchor='w', fill='x')

        ttk.Button(frame, text="Q1: Max Agreements Industry",
                   command=lambda: self.run_select(QUERY_1_MAX_INDUSTRY)).pack(fill='x', pady=2)
        ttk.Button(frame, text="Q2: Inactive Product",
                   command=lambda: self.run_select(QUERY_2_NO_ACTIVITY)).pack(fill='x', pady=2)
        ttk.Button(frame, text="Q3: Top Staff",
                   command=lambda: self.run_select(QUERY_3_MAX_STAFF_MOVEMENTS)).pack(fill='x', pady=2)
        ttk.Button(frame, text="Q4: Manufacturers w/o Storage",
                   command=lambda: self.run_select(QUERY_4_MANUFACTURERS_NO_STORAGE)).pack(fill='x', pady=2)
        ttk.Button(frame, text="Q5: Products per Facility",
                   command=lambda: self.run_select(QUERY_5_PRODUCTS_PER_FACILITY)).pack(fill='x', pady=2)
        ttk.Button(frame, text="Q6: Client Stock",
                   command=lambda: self.run_select(QUERY_6_CLIENT_TOTAL_QUANTITY)).pack(fill='x', pady=2)
        pass

    def execute_dml(self,query,parameters):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
            self.connection.commit()

            messagebox.showinfo("DML Operations", "DML operation executed successfully")
        except Exception as e:
            messagebox.showerror("DML Error", str(e))
            self.connection.rollback()

        pass

    def add_client(self):

        win = tk.Toplevel(self.root)
        win.title("Add Client")
        win.geometry("300x200")

        ttk.Label(win, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(win)
        name_entry.pack()

        ttk.Label(win, text="Phone:").pack(pady=5)
        phone_entry = ttk.Entry(win)
        phone_entry.pack()

        ttk.Label(win, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(win)
        email_entry.pack()

        def submit():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            if not name or not phone:
                messagebox.showwarning("Missing Data", "Name and phone required.")
                return
            self.execute_dml(INSERT_CLIENT, (name, phone, email))
            win.destroy()
            self.run_select("SELECT * FROM Client" , True)

        ttk.Button(win, text="Submit", command=submit).pack(pady=10)

        pass

    def add_agreement(self):
        win = tk.Toplevel(self.root)
        win.title("Add Agreement")
        win.geometry("300x350")

        ttk.Label(win, text="FacilityID:").pack(pady=5)
        facilityid_entry = ttk.Entry(win)
        facilityid_entry.pack()

        ttk.Label(win, text="ClientID:").pack(pady=5)
        clientid_entry = ttk.Entry(win)
        clientid_entry.pack()

        ttk.Label(win, text="Quantity:").pack(pady=5)
        quantity_entry = ttk.Entry(win)
        quantity_entry.pack()

        ttk.Label(win, text="Startdate:").pack(pady=5)
        startdate_entry = ttk.Entry(win)
        startdate_entry.pack()

        ttk.Label(win, text="Enddate:").pack(pady=5)
        enddate_entry = ttk.Entry(win)
        enddate_entry.pack()

        def submit():
            facility = facilityid_entry.get()
            client = clientid_entry.get()
            quantity = quantity_entry.get()
            startdate = startdate_entry.get()
            enddate = enddate_entry.get()
            self.execute_dml(INSERT_AGREEMENT, (facility, client, quantity, startdate, enddate))
            win.destroy()
            self.run_select("SELECT * FROM Storage_Agreement", adding=True)

        ttk.Button(win, text="Submit", command=submit).pack(pady=10)

        pass

    def delete_agreement(self):
        try:
            self.run_select("SELECT * FROM Storage_Agreement")
            agreement_id = simpledialog.askinteger("Delete Agreement", "Enter agreement ID:")
            if agreement_id is not None:
                self.execute_dml(DELETE_AGREEMENT, (agreement_id,))
        except Exception as e:
            messagebox.showerror("DML Error", str(e))

        self.run_select("SELECT * FROM Storage_Agreement")

        pass

    def delete_movement(self):
        try:
            self.run_select("SELECT * FROM INVENTORY_MOVEMENT")

            movement_id = simpledialog.askinteger("Delete Movement", "Enter Movement ID:")
            if movement_id is not None:
                self.execute_dml(DELETE_MOVEMENT, (movement_id,))
        except Exception as e:
            messagebox.showerror("DML Error", str(e))

        self.run_select("SELECT * FROM INVENTORY_MOVEMENT")

        pass

    def update_product(self):
        self.run_select("SELECT * FROM Product")

        win = tk.Toplevel(self.root)
        win.title("Update Product Weight")
        win.geometry("300x150")

        ttk.Label(win, text="Product ID:").pack()
        pid_entry = ttk.Entry(win)
        pid_entry.pack()

        ttk.Label(win, text="New Weight:").pack()
        weight_entry = ttk.Entry(win)
        weight_entry.pack()

        def submit():
            pid = pid_entry.get()
            weight = weight_entry.get()
            self.execute_dml(UPDATE_PRODUCT, (weight, pid))
            win.destroy()
            self.run_select("SELECT * FROM Product",updatingId=pid)


        ttk.Button(win, text="Submit", command=submit).pack()

        pass
    def update_facility(self):
        self.run_select("SELECT * FROM Facility")

        win = tk.Toplevel(self.root)
        win.title("Update Facility Capacity")
        win.geometry("300x150")

        ttk.Label(win, text="Facility ID:").pack()
        fid_entry = ttk.Entry(win)
        fid_entry.pack()

        ttk.Label(win, text="New Capacity:").pack()
        capacity_entry = ttk.Entry(win)
        capacity_entry.pack()

        def submit():
            fid = fid_entry.get()
            capacity = capacity_entry.get()
            self.execute_dml(UPDATE_FACILITY, (capacity, fid))
            win.destroy()
            self.run_select("SELECT * FROM Facility", updatingId=fid)

        ttk.Button(win, text="Submit", command=submit).pack()

        pass


    def run_select(self, query, adding=False , updatingId=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            style = ttk.Style(self.root)
            style.configure("Treeview.Heading", font=("Arial", 12, "bold"))


            # clear the current tree
            self.tree.delete(*self.tree.get_children())

            self.tree.tag_configure('highlight', background='green', font=('Arial', 9, 'bold'))

            columns = [desc[0] for desc in cursor.description]
            self.tree["columns"] = columns

            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor='center')

            # insert rows
            if adding == True:
                for i, row in enumerate(rows):
                    if i == len(rows)-1:
                        self.tree.insert("", "end", values=list(row), tags=('highlight',))
                    else:
                        self.tree.insert("", "end", values=list(row))
            elif updatingId is not None:
                for row in rows:

                    if int(row[0]) == int(updatingId):
                        self.tree.insert("", "end", values=list(row), tags=('highlight',))
                    else:
                        self.tree.insert("", "end", values=list(row))

            elif adding == False :
                if updatingId is None:
                    for row in rows:
                        self.tree.insert("", "end", values=list(row))


        except Exception as e:
            messagebox.showerror("Query Error", str(e))

        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
