import sqlite3

DB_PATH = "ims.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def add_employee(name, email, gender, contact, dob, doj, password, utype, address, salary):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO employee (name, email, gender, contact, dob, doj, pass, utype, address, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, email, gender, contact, dob, doj, password, utype, address, salary)
        )
        con.commit()
    finally:
        con.close()

def get_employees():
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM employee")
        return cur.fetchall()
    finally:
        con.close()

def update_employee(eid, name, email, gender, contact, dob, doj, password, utype, address, salary):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE employee SET name=?, email=?, gender=?, contact=?, dob=?, doj=?, pass=?, utype=?, address=?, salary=? WHERE eid=?",
            (name, email, gender, contact, dob, doj, password, utype, address, salary, eid)
        )
        con.commit()
    finally:
        con.close()

def delete_employee(eid):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM employee WHERE eid=?", (eid,))
        con.commit()
    finally:
        con.close()

def search_employee(by, value):
    con = get_connection()
    cur = con.cursor()
    try:
        query = f"SELECT * FROM employee WHERE {by} LIKE ?"
        cur.execute(query, (f"%{value}%",))
        return cur.fetchall()
    finally:
        con.close()

# Supplier CRUD

def add_supplier(name, contact, desc):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO supplier (name, contact, desc) VALUES (?, ?, ?)", (name, contact, desc))
        con.commit()
    finally:
        con.close()

def get_suppliers():
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM supplier")
        return cur.fetchall()
    finally:
        con.close()

def update_supplier(invoice, name, contact, desc):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE supplier SET name=?, contact=?, desc=? WHERE invoice=?",
            (name, contact, desc, invoice)
        )
        con.commit()
    finally:
        con.close()

def delete_supplier(invoice):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM supplier WHERE invoice=?", (invoice,))
        con.commit()
    finally:
        con.close()

def search_supplier(by, value):
    con = get_connection()
    cur = con.cursor()
    try:
        query = f"SELECT * FROM supplier WHERE {by} LIKE ?"
        cur.execute(query, (f"%{value}%",))
        return cur.fetchall()
    finally:
        con.close()

# Category CRUD

def add_category(name):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO category (name) VALUES (?)", (name,))
        con.commit()
    finally:
        con.close()

def get_categories():
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM category")
        return cur.fetchall()
    finally:
        con.close()

def update_category(cid, name):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE category SET name=? WHERE cid=?",
            (name, cid)
        )
        con.commit()
    finally:
        con.close()

def delete_category(cid):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM category WHERE cid=?", (cid,))
        con.commit()
    finally:
        con.close()

def search_category(by, value):
    con = get_connection()
    cur = con.cursor()
    try:
        query = f"SELECT * FROM category WHERE {by} LIKE ?"
        cur.execute(query, (f"%{value}%",))
        return cur.fetchall()
    finally:
        con.close()

# Product CRUD

def add_product(category, supplier, name, price, qty, status):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO product (Category, Supplier, name, price, qty, status)VALUES (?, ?, ?, ?, ?, ?) ", (category, supplier, name, price, qty, status))
        con.commit()
    finally:
        con.close()

def get_products():
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM product")
        return cur.fetchall()
    finally:
        con.close()

def update_product(pid, category, supplier, name, price, qty, status):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "UPDATE product SET Category=?, Supplier=?, name=?, price=?, qty=?, status=? WHERE pid=?",
            (category, supplier, name, price, qty, status, pid)
        )
        con.commit()
    finally:
        con.close()

def delete_product(pid):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM product WHERE pid=?", (pid,))
        con.commit()
    finally:
        con.close()

def search_product(by, value):
    con = get_connection()
    cur = con.cursor()
    try:
        query = f"SELECT * FROM product WHERE {by} LIKE ?"
        cur.execute(query, (f"%{value}%",))
        return cur.fetchall()
    finally:
        con.close()