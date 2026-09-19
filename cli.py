import json
import requests

BASE_URL = "http://127.0.0.1:5000/inventory"


def print_json(data):
  """Helper to cleanly print JSON responses."""
  print(json.dumps(data, indent=4))


def view_all_inventory():
  print("\n--- Fetching All Local Inventory ---")
  try:
    response = requests.get(BASE_URL)
    if response.status_code == 200:
      print_json(response.json())
    else:
      print(f"Error {response.status_code}: Unexpected response.")
  except requests.exceptions.ConnectionError:
    print(  
        "Connection Error: Could not connect to the server. Is app.py running?"
    )


def view_single_item():
  code = input("Enter the product barcode (code) to search locally: ").strip()
  if not code:
    print("Error: Code cannot be empty.")
    return

  try:
    response = requests.get(f"{BASE_URL}/{code}")
    if response.status_code == 200:
      print("\n--- Product Found Locally ---")
      print_json(response.json())
    elif response.status_code == 404:
      print(
          "\nProduct not found locally. You can use the API Fetch option to"
          " pull it from OpenFoodFacts."
      )
    else:
      print(f"Error {response.status_code}: {response.json().get('message')}")
  except requests.exceptions.ConnectionError:
    print(
        "Connection Error: Could not connect to the server. Is app.py running?"
    )


def fetch_live_api_by_code():
  code = input(
      "Enter the barcode to fetch from OpenFoodFacts and save locally: "
  ).strip()
  if not code:
    print("Error: Code cannot be empty.")
    return

  try:
    response = requests.get(f"{BASE_URL}/api/code/{code}")
    if response.status_code == 200:
      print("\n--- Successfully Fetched and Added to Local Inventory ---")
      print_json(response.json())
    elif response.status_code == 404:
      print("\nProduct not found in the OpenFoodFacts API.")
    else:
      print(f"Error {response.status_code}: {response.json().get('message')}")
  except requests.exceptions.ConnectionError:
    print(
        "Connection Error: Could not connect to the server. Is app.py running?"
    )


def search_live_api_by_name():
  name = input("Enter product name or keyword to search on OpenFoodFacts: ")
  if not name:
    print("Error: Search term cannot be empty.")
    return

  try:
    response = requests.get(f"{BASE_URL}/api/name/{name}")
    if response.status_code == 200:
      print("\n--- Search Results ---")
      print_json(response.json())
    elif response.status_code == 404:
      print("\nNo products found matching that name.")
    else:
      print(f"Error {response.status_code}: Unexpected error.")
  except requests.exceptions.ConnectionError:
    print(
        "Connection Error: Could not connect to the server. Is app.py running?"
    )


def add_inventory_item():
  print("\n--- Add New Inventory Item ---")
  code = input("Enter barcode (code) [Required]: ").strip()
  if not code:
    print("Error: Code is required.")
    return

  brand = input("Enter brand name (optional): ").strip()
  product_name = input("Enter product name (optional): ").strip()
  categories_input = input(
      "Enter categories separated by commas (optional): "
  ).strip()

  categories = (
      [c.strip() for c in categories_input.split(",")]
      if categories_input
      else []
  )

  payload = {
      "code": code,
      "brand": brand if brand else None,
      "product_name": product_name if product_name else None,
      "categories": categories,
  }

  try:
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 201:
      print("\n--- Product Added Successfully ---")
      print_json(response.json())
    else:
      print(f"Error {response.status_code}: {response.json().get('message')}")
  except requests.exceptions.ConnectionError:
    print(
        "Connection Error: Could not connect to the server. Is app.py running?"
    )


def update_inventory_item():
  code = input(
      "Enter the barcode (code) of the item you want to update: "
  ).strip()
  if not code:
    print("Error: Code cannot be empty.")
    return

  print("\nEnter the new details (leave blank to skip updating a field):")
  brand = input("New brand: ").strip()
  product_name = input("New product name: ").strip()

  payload = {}
  if brand:
    payload["brand"] = brand
  if product_name:
    payload["product_name"] = product_name

  if not payload:
    print("No updates provided. Operation cancelled.")
    return

  try:
    response = requests.patch(f"{BASE_URL}/{code}", json=payload)
    if response.status_code == 200:
      print("\n--- Product Updated Successfully ---")
      print_json(response.json())
    elif response.status_code == 404:
      print("\nError: Product code not found in local inventory.")
    else:
      print(f"Error {response.status_code}: Unexpected error.")
  except requests.exceptions.ConnectionError:
    print(
        "Connection Error: Could not connect to the server. Is app.py running?"
    )


def delete_inventory_item():
  code = input(
      "Enter the barcode (code) of the item you want to delete: "
  ).strip()
  if not code:
    print("Error: Code cannot be empty.")
    return

  confirm = (
      input(f"Are you sure you want to delete item {code}? (y/n): ")
      .strip()
      .lower()
  )
  if confirm != "y":
    print("Deletion cancelled.")
    return

  try:
    response = requests.delete(f"{BASE_URL}/{code}")
    if response.status_code == 204:
      print(f"\nSuccess: Product {code} has been deleted.")
    elif response.status_code == 404:
      print("\nError: Product code not found in local inventory.")
    else:
      print(f"Error {response.status_code}: Unexpected error.")
  except requests.exceptions.ConnectionError:
    print(
        "Connection Error: Could not connect to the server. Is app.py running?"
    )


def main():
  while True:
    print("\n==============================")
    print("   OPENFOODFACTS INVENTORY CLI")
    print("==============================")
    print("1. View All Local Inventory")
    print("2. View Single Item (Local)")
    print("3. Fetch & Add Item from API (By Barcode)")
    print("4. Search API (By Product Name)")
    print("5. Add New Item Manually")
    print("6. Update Item Details (PATCH)")
    print("7. Delete Item")
    print("8. Exit")

    choice = input("\nSelect an option (1-8): ").strip()

    if choice == "1":
      view_all_inventory()
    elif choice == "2":
      view_single_item()
    elif choice == "3":
      fetch_live_api_by_code()
    elif choice == "4":
      search_live_api_by_name()
    elif choice == "5":
      add_inventory_item()
    elif choice == "6":
      update_inventory_item()
    elif choice == "7":
      delete_inventory_item()
    elif choice == "8":
      print("\nExiting CLI. Goodbye!")
      break
    else:
      print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
  main()