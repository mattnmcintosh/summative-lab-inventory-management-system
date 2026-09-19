OpenFoodFacts Inventory Management System
A full-stack Python application featuring a RESTful Flask backend, an interactive Command Line Interface (CLI) client, external API integration with OpenFoodFacts, and a comprehensive unit testing suite.

📂 Project Structure
inventory_project/
├── app.py            # Flask backend server and REST endpoints
├── cli.py            # Interactive Command Line Interface (CLI)
├── data.py           # Simulated local database array
├── requirements.txt  # Project dependencies
└── tests/            # Automated test suites
    ├── test_app.py   # Backend API & mock integration tests
    └── test_cli.py   # CLI command and user input tests
🛠️ Installation and Setup
Clone or download the project files into a local directory.

Navigate to the project root directory in your terminal:

Bash
cd inventory_project
Install dependencies using pip:

Bash
pip install -r requirements.txt
Run the Flask Backend Server in your first terminal:

Bash
python app.py
(The server will start at [http://127.0.0.1:5000](http://127.0.0.1:5000))

Run the CLI Client in a second terminal:

Bash
python cli.py
🌐 API Endpoint Details
The Flask backend exposes the following RESTful endpoints:

GET /inventory

Description: Retrieves all items currently stored in the local simulated inventory array.

Response: 200 OK with a JSON list of inventory items.

GET /inventory/<string:code>

Description: Fetches a single item by its barcode from the local database.

Response: 200 OK with the item object, or 404 Not Found if the item isn't stored locally.

GET /inventory/api/code/<string:code>

Description: Queries the live OpenFoodFacts API using a barcode, parses the filtered data format, adds it to the local inventory array, and returns it.

Response: 200 OK with the added item, or 404 Not Found / 500 Error if the product is invalid or missing.

GET /inventory/api/name/<string:name>

Description: Searches the live OpenFoodFacts API for products matching a given text query/name.

Response: 200 OK with a list of search results, or 404 Not Found.

POST /inventory

Description: Adds a new inventory item manually to the local array. Requires a JSON payload containing at least a "code".

Response: 201 Created with the new item object, or 400 Bad Request if the code is missing.

PATCH /inventory/<string:code>

Description: Updates specific fields (partial update) of an existing item matching the given barcode.

Response: 200 OK with the updated item object, or 404 Not Found if the code does not exist.

DELETE /inventory/<string:code>

Description: Removes an item from the local inventory array by its barcode.

Response: 204 No Content on success, or 404 Not Found if the code does not exist.

🖥️ Example Usage of CLI Commands
When you run python cli.py, you will be greeted by an interactive menu with options 1 through 8. Here is how example workflows look:

Example 1: Viewing Local Inventory (Option 1)
Select option 1 from the menu to fetch and display everything currently stored locally:

Plaintext
==============================
   OPENFOODFACTS INVENTORY CLI
==============================
1. View All Local Inventory
...
Select an option (1-8): 1

--- Fetching All Local Inventory ---
[
    {
        "code": "3017620422003",
        "brand": "Nutella",
        "product_name": "Hazelnut Spread",
        "categories": ["Spreads"],
        ...
    }
]
Example 2: Fetching an Item from OpenFoodFacts by Barcode (Option 3)
Select option 3 to pull data directly from the live API and save it to your local storage:

Plaintext
Select an option (1-8): 3
Enter the barcode to fetch from OpenFoodFacts and save locally: 5449000000996

--- Successfully Fetched and Added to Local Inventory ---
{
    "code": "5449000000996",
    "brand": "Coca-Cola",
    "product_name": "Coke",
    ...
}
Example 3: Updating Item Details (Option 6)
Select option 6 to patch an existing record's details:

Plaintext
Select an option (1-8): 6
Enter the barcode (code) of the item you want to update: 3017620422003

Enter the new details (leave blank to skip updating a field):
New brand: Nutella Official
New product name: Delicious Hazelnut Spread

--- Product Updated Successfully ---
{
    "code": "3017620422003",
    "brand": "Nutella Official",
    "product_name": "Delicious Hazelnut Spread",
    ...
}
Example 4: Deleting a Product (Option 7)
Select option 7 to remove a product from your local database:

Plaintext
Select an option (1-8): 7
Enter the barcode (code) of the item you want to delete: 3017620422003
Are you sure you want to delete item 3017620422003? (y/n): y

Success: Product 3017620422003 has been deleted.