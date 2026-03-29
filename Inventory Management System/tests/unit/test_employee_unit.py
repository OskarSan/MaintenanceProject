from pathlib import Path
from unittest.mock import MagicMock
import sys

PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import employee
from employee import employeeClass


class FakeVar:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class FakeText:
    def __init__(self, value=""):
        self.value = value

    def get(self, _start, _end):
        return self.value

    def delete(self, _start, _end):
        self.value = ""

    def insert(self, _where, value):
        self.value = value


class FakeTable:
    def __init__(self):
        self.rows = []

    def get_children(self):
        return ["item-1", "item-2"] if self.rows else []

    def delete(self, *_items):
        self.rows = []

    def insert(self, _parent, _where, values):
        self.rows.append(values)


def _make_employee_obj():
    obj = employeeClass.__new__(employeeClass)
    obj.root = object()

    obj.var_searchby = FakeVar("Select")
    obj.var_searchtxt = FakeVar("")
    obj.var_emp_id = FakeVar("")
    obj.var_gender = FakeVar("Select")
    obj.var_contact = FakeVar("")
    obj.var_name = FakeVar("")
    obj.var_dob = FakeVar("")
    obj.var_doj = FakeVar("")
    obj.var_email = FakeVar("")
    obj.var_pass = FakeVar("")
    obj.var_utype = FakeVar("Admin")
    obj.var_salary = FakeVar("")
    obj.txt_address = FakeText("")
    obj.EmployeeTable = FakeTable()
    return obj


def test_add_shows_error_when_emp_id_missing(monkeypatch):
    obj = _make_employee_obj()
    showerror = MagicMock()

    monkeypatch.setattr(employee.messagebox, "showerror", showerror)
    monkeypatch.setattr(employee.db_manager, "search_employee", MagicMock())
    monkeypatch.setattr(employee.db_manager, "add_employee", MagicMock())

    obj.add()

    showerror.assert_called_once()
    assert "Employee ID must be required" in showerror.call_args.args[1]
    employee.db_manager.search_employee.assert_not_called()
    employee.db_manager.add_employee.assert_not_called()


def test_add_calls_db_and_success_message(monkeypatch):
    obj = _make_employee_obj()
    obj.var_emp_id.set("101")
    obj.var_name.set("John")
    obj.var_email.set("john@example.com")
    obj.var_gender.set("Male")
    obj.var_contact.set("999")
    obj.var_dob.set("2000-01-01")
    obj.var_doj.set("2024-01-01")
    obj.var_pass.set("secret")
    obj.var_utype.set("Admin")
    obj.var_salary.set("2500")
    obj.txt_address = FakeText("Some address")
    obj.clear = MagicMock()
    obj.show = MagicMock()

    showinfo = MagicMock()
    monkeypatch.setattr(employee.messagebox, "showinfo", showinfo)
    monkeypatch.setattr(employee.messagebox, "showerror", MagicMock())
    monkeypatch.setattr(employee.db_manager, "search_employee", MagicMock(return_value=[]))
    monkeypatch.setattr(employee.db_manager, "add_employee", MagicMock())

    obj.add()

    employee.db_manager.add_employee.assert_called_once_with(
        "John",
        "john@example.com",
        "Male",
        "999",
        "2000-01-01",
        "2024-01-01",
        "secret",
        "Admin",
        "Some address",
        "2500",
    )
    showinfo.assert_called_once()
    obj.clear.assert_called_once()
    obj.show.assert_called_once()


def test_update_shows_invalid_id_error(monkeypatch):
    obj = _make_employee_obj()
    obj.var_emp_id.set("404")
    showerror = MagicMock()

    monkeypatch.setattr(employee.messagebox, "showerror", showerror)
    monkeypatch.setattr(employee.db_manager, "search_employee", MagicMock(return_value=[]))
    monkeypatch.setattr(employee.db_manager, "update_employee", MagicMock())

    obj.update()

    showerror.assert_called_once()
    assert "Invalid Employee ID" in showerror.call_args.args[1]
    employee.db_manager.update_employee.assert_not_called()


def test_delete_calls_db_when_confirmed(monkeypatch):
    obj = _make_employee_obj()
    obj.var_emp_id.set("10")
    obj.clear = MagicMock()

    monkeypatch.setattr(employee.db_manager, "search_employee", MagicMock(return_value=[("10",)]))
    monkeypatch.setattr(employee.db_manager, "delete_employee", MagicMock())
    monkeypatch.setattr(employee.messagebox, "askyesno", MagicMock(return_value=True))
    monkeypatch.setattr(employee.messagebox, "showinfo", MagicMock())
    monkeypatch.setattr(employee.messagebox, "showerror", MagicMock())

    obj.delete()

    employee.db_manager.delete_employee.assert_called_once_with("10")
    employee.messagebox.showinfo.assert_called_once()
    obj.clear.assert_called_once()


def test_search_populates_table_when_rows_exist(monkeypatch):
    obj = _make_employee_obj()
    obj.var_searchby.set("Name")
    obj.var_searchtxt.set("john")
    rows = [
        (1, "John", "john@example.com", "Male", "123", "2000-01-01", "2024-01-01", "x", "Admin", "Addr", "1000")
    ]

    monkeypatch.setattr(employee.db_manager, "search_employee", MagicMock(return_value=rows))
    monkeypatch.setattr(employee.messagebox, "showerror", MagicMock())

    obj.search()

    employee.db_manager.search_employee.assert_called_once_with("name", "john")
    assert obj.EmployeeTable.rows == rows


def test_clear_resets_fields_and_calls_show(monkeypatch):
    obj = _make_employee_obj()
    obj.var_emp_id.set("99")
    obj.var_name.set("N")
    obj.var_email.set("e@x")
    obj.var_gender.set("Male")
    obj.var_contact.set("1")
    obj.var_dob.set("d")
    obj.var_doj.set("d")
    obj.var_pass.set("p")
    obj.var_utype.set("Employee")
    obj.var_salary.set("100")
    obj.var_searchby.set("Name")
    obj.var_searchtxt.set("abc")
    obj.txt_address = FakeText("Filled")

    obj.show = MagicMock()
    obj.clear()

    assert obj.var_emp_id.get() == ""
    assert obj.var_name.get() == ""
    assert obj.var_email.get() == ""
    assert obj.var_gender.get() == "Select"
    assert obj.var_utype.get() == "Admin"
    assert obj.var_searchby.get() == "Select"
    assert obj.var_searchtxt.get() == ""
    assert obj.txt_address.get("1.0", employee.END) == ""
    obj.show.assert_called_once()
