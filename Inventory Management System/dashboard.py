from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from login import LoginWindow

# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_DIR, exist_ok=True)
# ---------------------------------------------------

class IMS:
    def __init__(self, root, user_role = None):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")
        self.current_user_role = user_role
        

        # ------------- title --------------
        self.icon_title = PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
        title = Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        ).place(x=0, y=0, relwidth=1, height=70)

        # ------------ login/logout button -----------
        self.btn_login_logout = Button(
            self.root,
            font=("times new roman", 15, "bold"),
            bg="yellow", cursor="hand2"
        )
        self.btn_login_logout.place(x=1150, y=10, height=50, width=150)
        self.update_login_logout_button()

        # ------------ clock -----------------
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=("times new roman", 15),
            bg="#4d636d", fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ---------------- left menu ---------------
        self.MenuLogo = Image.open(os.path.join(IMAGE_DIR, "menu_im.png"))
        self.MenuLogo = self.MenuLogo.resize((200, 200))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(
            LeftMenu, text="Menu",
            font=("times new roman", 20),
            bg="#009688"
        ).pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file=os.path.join(IMAGE_DIR, "side.png"))


        self.btn_employee = Button(
            LeftMenu, text="Employee", command=self.employee,
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2"
        )
        self.btn_employee.pack(side=TOP, fill=X)

        self.btn_supplier = Button(
            LeftMenu, text="Supplier", command=self.supplier,
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2"
        )
        self.btn_supplier.pack(side=TOP, fill=X)

        self.btn_category = Button(
            LeftMenu, text="Category", command=self.category,
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2"
        )
        self.btn_category.pack(side=TOP, fill=X)

        self.btn_product = Button(
            LeftMenu, text="Products", command=self.product,
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2"
        )
        self.btn_product.pack(side=TOP, fill=X)

        self.btn_sales = Button(
            LeftMenu, text="Sales", command=self.sales,
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2"
        )
        self.btn_sales.pack(side=TOP, fill=X)

        self.btn_exit = Button(
            LeftMenu, text="Exit",
            image=self.icon_side, compound=LEFT,
            padx=5, anchor="w",
            font=("times new roman", 20, "bold"),
            bg="white", bd=3, cursor="hand2",
            command=self.root.destroy
        )
        self.btn_exit.pack(side=TOP, fill=X)

        # ------------------- user level check ------------------
        self.update_user_permissions()
        
    
        # ----------- content ----------------
        self.lbl_employee = Label(
            self.root, text="Total Employee\n{ 0 }",
            bd=5, relief=RIDGE, bg="#33bbf9",
            fg="white", font=("goudy old style", 20, "bold")
        )
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(
            self.root, text="Total Supplier\n{ 0 }",
            bd=5, relief=RIDGE, bg="#ff5722",
            fg="white", font=("goudy old style", 20, "bold")
        )
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(
            self.root, text="Total Category\n{ 0 }",
            bd=5, relief=RIDGE, bg="#009688",
            fg="white", font=("goudy old style", 20, "bold")
        )
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(
            self.root, text="Total Product\n{ 0 }",
            bd=5, relief=RIDGE, bg="#607d8b",
            fg="white", font=("goudy old style", 20, "bold")
        )
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(
            self.root, text="Total Sales\n{ 0 }",
            bd=5, relief=RIDGE, bg="#ffc107",
            fg="white", font=("goudy old style", 20, "bold")
        )
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # ------------ footer -----------------
        lbl_footer = Label(
            self.root,
            text="IMS-Inventory Management System",
            font=("times new roman", 12),
            bg="#4d636d", fg="white"
        ).pack(side=BOTTOM, fill=X)

        self.update_content()

    # -------------- functions ----------------
    def _close_current_dialog(self):
        if hasattr(self, 'current_dialog') and self.current_dialog is not None:
            try:
                self.current_dialog.destroy()
            except:
                pass
            self.current_dialog = None

    def employee(self):
        self._close_current_dialog()
        self.current_dialog = Toplevel(self.root)
        self.new_obj = employeeClass(self.current_dialog)

    def supplier(self):
        self._close_current_dialog()
        self.current_dialog = Toplevel(self.root)
        self.new_obj = supplierClass(self.current_dialog)

    def category(self):
        self._close_current_dialog()
        self.current_dialog = Toplevel(self.root)
        self.new_obj = categoryClass(self.current_dialog)

    def product(self):
        self._close_current_dialog()
        self.current_dialog = Toplevel(self.root)
        self.new_obj = productClass(self.current_dialog)

    def sales(self):
        self._close_current_dialog()
        self.current_dialog = Toplevel(self.root)
        self.new_obj = salesClass(self.current_dialog)

    def update_content(self):
        con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()

        try:
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[ {len(product)} ]")

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[ {len(category)} ]")

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n[ {len(employee)} ]")

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n[ {len(supplier)} ]")

            bill = len(os.listdir(BILL_DIR))
            self.lbl_sales.config(text=f"Total Sales\n[ {bill} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}"
            )

            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def update_user_permissions(self):
            # Enable all by default
            self.btn_employee.config(state=NORMAL)
            self.btn_supplier.config(state=NORMAL)
            self.btn_category.config(state=NORMAL)
            self.btn_product.config(state=NORMAL)
            self.btn_sales.config(state=NORMAL)
            # Restrict if not admin
            if self.current_user_role != 'Admin':
                self.btn_supplier.config(state=DISABLED)
                self.btn_category.config(state=DISABLED)
                self.btn_product.config(state=DISABLED)
                self.btn_sales.config(state=DISABLED)

    def update_login_logout_button(self):
        if self.current_user_role:
            self.btn_login_logout.config(text="Logout", command=self.logout)
        else:
            self.btn_login_logout.config(text="Login", command=self.login)

    def logout(self):
        self.current_user_role = None
        self.update_login_logout_button()
        self.update_user_permissions()
        login_win = Toplevel(self.root)
        login = LoginWindow(login_win, parent=self.root)
        login_win.grab_set()
        self.root.wait_window(login_win)
        if login.user_role:
            self.current_user_role = login.user_role
            self.update_login_logout_button()
            self.update_user_permissions()

    def login(self):
        login_win = Toplevel(self.root)
        login = LoginWindow(login_win, parent=self.root)
        login_win.grab_set()
        self.root.wait_window(login_win)
        if login.user_role:
            self.current_user_role = login.user_role
            self.update_login_logout_button()
            self.update_user_permissions()
if __name__ == "__main__":
    root = Tk()
    app = IMS(root)
    root.mainloop()