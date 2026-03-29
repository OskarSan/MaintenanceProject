from pathlib import Path
import sqlite3
import sys

PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import db_manager


SCHEMA = [
    "CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)",
    "CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)",
    "CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)",
    "CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,name text,price text,qty text,status text)",
]


def _setup_temp_db(db_file):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    for statement in SCHEMA:
        cur.execute(statement)
    con.commit()
    con.close()


def test_employee_crud_integration(tmp_path, monkeypatch):
    db_file = tmp_path / "ims_integration.db"
    _setup_temp_db(db_file)
    monkeypatch.setattr(db_manager, "DB_PATH", str(db_file))

    db_manager.add_employee(
        name="Alice",
        email="alice@example.com",
        gender="F",
        contact="555001",
        dob="2000-01-01",
        doj="2024-01-01",
        password="secret",
        utype="admin",
        address="Street 1",
        salary="1500",
    )

    rows = db_manager.get_employees()
    assert len(rows) == 1
    eid = rows[0][0]

    db_manager.update_employee(
        eid=eid,
        name="Alice Updated",
        email="alice@example.com",
        gender="F",
        contact="555002",
        dob="2000-01-01",
        doj="2024-01-01",
        password="secret2",
        utype="admin",
        address="Street 1",
        salary="1700",
    )

    updated = db_manager.search_employee("name", "Updated")
    assert len(updated) == 1
    assert updated[0][1] == "Alice Updated"
    assert updated[0][4] == "555002"

    db_manager.delete_employee(eid)
    assert db_manager.get_employees() == []


def test_category_and_supplier_crud_integration(tmp_path, monkeypatch):
    db_file = tmp_path / "ims_integration.db"
    _setup_temp_db(db_file)
    monkeypatch.setattr(db_manager, "DB_PATH", str(db_file))

    db_manager.add_category("Stationery")
    categories = db_manager.search_category("name", "Stat")
    assert len(categories) == 1
    cid = categories[0][0]

    db_manager.update_category(cid, "Office Stationery")
    categories = db_manager.search_category("name", "Office")
    assert len(categories) == 1

    db_manager.add_supplier("Acme", "12345", "Primary supplier")
    suppliers = db_manager.search_supplier("name", "Acm")
    assert len(suppliers) == 1
    invoice = suppliers[0][0]

    db_manager.update_supplier(invoice, "Acme Updated", "67890", "Backup supplier")
    suppliers = db_manager.search_supplier("name", "Updated")
    assert len(suppliers) == 1
    assert suppliers[0][2] == "67890"

    db_manager.delete_category(cid)
    db_manager.delete_supplier(invoice)
    assert db_manager.get_categories() == []
    assert db_manager.get_suppliers() == []


def test_product_crud_integration(tmp_path, monkeypatch):
    db_file = tmp_path / "ims_integration.db"
    _setup_temp_db(db_file)
    monkeypatch.setattr(db_manager, "DB_PATH", str(db_file))

    db_manager.add_product("Stationery", "Acme", "Pen", "10", "50", "Active")

    products = db_manager.search_product("name", "Pe")
    assert len(products) == 1
    pid = products[0][0]

    db_manager.update_product(pid, "Stationery", "Acme", "Pen Blue", "12", "40", "Active")

    updated = db_manager.search_product("name", "Blue")
    assert len(updated) == 1
    assert updated[0][3] == "Pen Blue"
    assert updated[0][5] == "40"

    db_manager.delete_product(pid)
    assert db_manager.get_products() == []
