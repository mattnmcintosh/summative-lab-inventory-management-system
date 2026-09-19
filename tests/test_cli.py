import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from unittest.mock import patch
import pytest
import cli

@patch("cli.requests.get")
def test_cli_view_all_inventory_success(mock_get, capsys):
  mock_get.return_value.status_code = 200
  mock_get.return_value.json.return_value = [{"code": "123", "brand": "Test"}]

  cli.view_all_inventory()
  captured = capsys.readouterr()
  assert "Fetching All Local Inventory" in captured.out
  assert "123" in captured.out


@patch("cli.requests.get")
def test_cli_view_all_inventory_connection_error(mock_get, capsys):
  # Simulate server being offline
  mock_get.side_effect = cli.requests.exceptions.ConnectionError

  cli.view_all_inventory()
  captured = capsys.readouterr()
  assert "Connection Error" in captured.out


@patch("builtins.input", return_value="3017620422003")
@patch("cli.requests.get")
def test_cli_view_single_item(mock_get, mock_input, capsys):
  mock_get.return_value.status_code = 200
  mock_get.return_value.json.return_value = {
      "code": "3017620422003",
      "brand": "Nutella",
  }

  cli.view_single_item()
  captured = capsys.readouterr()
  assert "Product Found Locally" in captured.out
  assert "Nutella" in captured.out


@patch(
    "builtins.input",
    side_effect=["999", "NewBrand", "NewProduct", "Category1"],
)
@patch("cli.requests.post")
def test_cli_add_inventory_item(mock_post, mock_input, capsys):
  mock_post.return_value.status_code = 201
  mock_post.return_value.json.return_value = {
      "code": "999",
      "brand": "NewBrand",
  }

  cli.add_inventory_item()
  captured = capsys.readouterr()
  assert "Product Added Successfully" in captured.out
  mock_post.assert_called_once()


@patch("builtins.input", side_effect=["3017620422003", "y"])
@patch("cli.requests.delete")
def test_cli_delete_inventory_item(mock_delete, mock_input, capsys):
  mock_delete.return_value.status_code = 204

  cli.delete_inventory_item()
  captured = capsys.readouterr()
  assert "Success: Product 3017620422003 has been deleted" in captured.out
  mock_delete.assert_called_once()