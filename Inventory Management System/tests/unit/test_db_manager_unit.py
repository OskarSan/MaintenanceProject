from pathlib import Path
from unittest.mock import MagicMock
import sys

PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import db_manager


def _mock_connection(monkeypatch, fetch_rows=None):
    con = MagicMock()
    cur = MagicMock()
    con.cursor.return_value = cur
    if fetch_rows is not None:
        cur.fetchall.return_value = fetch_rows

    monkeypatch.setattr(db_manager, "get_connection", lambda: con)
    return con, cur


def test_add_employee_executes_insert_and_commits(monkeypatch):
    con, cur = _mock_connection(monkeypatch)

    db_manager.add_employee(
        name="johndoe",
        email="johndoe@example.com",
        gender="F",
        contact="12345",
        dob="2000-01-01",
        doj="2024-01-01",
        password="secret",
        utype="admin",
        address="Main street",
        salary="1000",
    )

    cur.execute.assert_called_once()
    sql, params = cur.execute.call_args.args
    assert "INSERT INTO employee" in sql
    assert params[0] == "johndoe"
    assert params[1] == "johndoe@example.com"
    con.commit.assert_called_once()
    con.close.assert_called_once()


def test_get_products_returns_rows_from_fetchall(monkeypatch):
    expected_rows = [
        (1, "Stationery", "Acme", "Pen", "10", "5", "Active"),
        (2, "Books", "Acme", "Notebook", "20", "8", "Active"),
    ]
    con, cur = _mock_connection(monkeypatch, fetch_rows=expected_rows)

    rows = db_manager.get_products()

    cur.execute.assert_called_once_with("SELECT * FROM product")
    assert rows == expected_rows
    con.close.assert_called_once()


def test_search_product_uses_like_pattern(monkeypatch):
    expected_rows = [(1, "Stationery", "Acme", "Pen", "10", "5", "Active")]
    con, cur = _mock_connection(monkeypatch, fetch_rows=expected_rows)

    rows = db_manager.search_product("name", "Pe")

    cur.execute.assert_called_once()
    sql, params = cur.execute.call_args.args
    assert sql == "SELECT * FROM product WHERE name LIKE ?"
    assert params == ("%Pe%",)
    assert rows == expected_rows
    con.close.assert_called_once()


def test_delete_product_executes_delete_by_id(monkeypatch):
    con, cur = _mock_connection(monkeypatch)

    db_manager.delete_product(9)

    cur.execute.assert_called_once_with("DELETE FROM product WHERE pid=?", (9,))
    con.commit.assert_called_once()
    con.close.assert_called_once()
