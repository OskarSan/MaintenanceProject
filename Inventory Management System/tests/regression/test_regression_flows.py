from pathlib import Path
import sqlite3
import sys
from unittest.mock import MagicMock

PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import billing
from billing import billClass
import employee
from employee import employeeClass


class DummyText:
    def __init__(self):
        self.content = []

    def insert(self, _pos, text):
        self.content.append(text)


class FakeVar:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value



def _build_temp_product_db(db_file, name, price, qty, status="Active"):
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,name text,price text,qty text,status text)"
    )
    cur.execute(
        "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES (?,?,?,?,?,?)",
        ("Stationery", "Acme", name, price, qty, status),
    )
    con.commit()
    con.close()

def _make_employee_for_validation_tests():
    obj = employeeClass.__new__(employeeClass)
    obj.root = object()
    obj.var_searchby = FakeVar("Select")
    obj.var_searchtxt = FakeVar("")
    obj.var_emp_id = FakeVar("")
    return obj


def test_regression_bill_middle_sets_inactive_when_quantity_reaches_zero(tmp_path, monkeypatch):
    db_file = tmp_path / "ims_regression.db"
    _build_temp_product_db(db_file, name="Pen", price="10", qty="5")

    real_connect = sqlite3.connect
    monkeypatch.setattr(billing.sqlite3, "connect", lambda *_args, **_kwargs: real_connect(db_file))

    obj = billClass.__new__(billClass)
    obj.cart_list = [["1", "Pen", "10", "5", "5"]]
    obj.txt_bill_area = DummyText()
    obj.show = lambda: None

    obj.bill_middle()

    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("SELECT qty, status FROM product WHERE pid=1")
    qty, status = cur.fetchone()
    con.close()

    assert qty == "0"
    assert status == "Inactive"


def test_regression_bill_middle_keeps_active_when_stock_remains(tmp_path, monkeypatch):
    db_file = tmp_path / "ims_regression.db"
    _build_temp_product_db(db_file, name="Notebook", price="20", qty="10")

    real_connect = sqlite3.connect
    monkeypatch.setattr(billing.sqlite3, "connect", lambda *_args, **_kwargs: real_connect(db_file))

    obj = billClass.__new__(billClass)
    obj.cart_list = [["1", "Notebook", "20", "3", "10"]]
    obj.txt_bill_area = DummyText()
    obj.show = lambda: None

    obj.bill_middle()

    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("SELECT qty, status FROM product WHERE pid=1")
    qty, status = cur.fetchone()
    con.close()

    assert qty == "7"
    assert status == "Active"


def test_regression_employee_search_requires_search_by_option(monkeypatch):
    obj = _make_employee_for_validation_tests()

    monkeypatch.setattr(employee.messagebox, "showerror", MagicMock())
    monkeypatch.setattr(employee.db_manager, "search_employee", MagicMock())

    obj.search()

    employee.messagebox.showerror.assert_called_once()
    assert "Select Search By option" in employee.messagebox.showerror.call_args.args[1]
    employee.db_manager.search_employee.assert_not_called()


def test_regression_employee_delete_invalid_id_never_calls_delete(monkeypatch):
    obj = _make_employee_for_validation_tests()
    obj.var_emp_id.set("999")

    monkeypatch.setattr(employee.messagebox, "showerror", MagicMock())
    monkeypatch.setattr(employee.db_manager, "search_employee", MagicMock(return_value=[]))
    monkeypatch.setattr(employee.db_manager, "delete_employee", MagicMock())

    obj.delete()

    employee.messagebox.showerror.assert_called_once()
    assert "Invalid Employee ID" in employee.messagebox.showerror.call_args.args[1]
    employee.db_manager.delete_employee.assert_not_called()
