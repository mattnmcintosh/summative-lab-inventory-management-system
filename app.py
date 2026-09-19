from flask import Flask, jsonify, request
import requests
from data import products

app = Flask(__name__)

keys_to_copy = ["code", "brand", "product_name", "key_ingredients", "categories", "allergens", "nutritional_info_per_100g", "nutri_score", "nova_group"]

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(products), 200

@app.route("/inventory/<string:code>", methods=["GET"])
def get_inventory_by_code(code):
    for p in products:
        if p["code"] == code:
            return jsonify(p), 200
    return jsonify({"message": "Product not found locally. However, if you do /inventory/api/<code>, you can get your data and it will also be added to the local database."}), 404

@app.route("/inventory/api/code/<string:code>", methods=["GET"])
def get_live_inventory_by_code(code):
    url = f"https://world.openfoodfacts.net/api/v3.6/product/{code}.json?fields=code,brand,product_name,key_ingredients,categories,allergens,nutritional_info_per_100g,nutri_score,nova_group"
    response = requests.get(url, auth=("off", "off"))
    if response.status_code == 404:
        return jsonify({"message": "Product not found in the API. The local database will not be changed."}), 404
    else:
        response_data = response.json()
        product_data = response_data.get("product")
        if not product_data:
            return jsonify({"message": "Product data was missing from the API response, the local database will not be changed"}), 500
        product = parse_to_database_format(product_data)
        if product == None:
            return jsonify({"message": "Somehow, an object without an code was retrieved. There is no valid entry. The local database will not be changed"}), 500
        else:
            products.append(product)
            return jsonify(product), 200

@app.route("/inventory/api/name/<string:name>", methods=["GET"])
def search_live_inventory_by_name(name):
    url = f"https://search.openfoodfacts.org/search?q={name}&page_size=10&page=1&fields=code%2Cbrand%2Cproduct_name%2Ckey_ingredients%2Ccategories%2Callergens%2Cnutritional_info_per_100g%2Cnutri_score%2Cnova_group"
    response = requests.get(url)
    data = response.json()
    possible_products = get_likely_search_results(data)
    if possible_products == None:
        return jsonify({"message": "No possible products found"}), 404
    else:
        '''Not adding products by name since there's little guarantee a high-quality search result would be found via this method'''
        return jsonify(possible_products), 200

@app.route("/inventory", methods=["POST"])
def add_new_inventory_item():
    data = request.get_json()
    if data.get("code") == None:
        return jsonify({"message": "An object needs a code to be valid. Nothing has been changed."}), 400
    else:
        new_product = parse_to_database_format(data)
        products.append(new_product)
        return jsonify(new_product), 201


@app.route("/inventory/<string:code>", methods=["PATCH"])
def update_inventory_item_by_code(code):
    global products
    data = request.get_json()
    product = next((p for p in products if p["code"] == code), None)
    if not product:
        return jsonify({"message": "Code not found"}), 404
    else:
        filtered_updates = update_with_database_format(data)
        updated_product = {**product, **filtered_updates}
        updated_product["code"] = code
        products = [updated_product if p.get("code") == code else p for p in products]
        return jsonify(updated_product), 200

@app.route("/inventory/<string:code>", methods=["DELETE"])
def remove_inventory_item_by_code(code):
    global products
    removable_product = next((p for p in products if p["code"] == code), None)
    if not removable_product:
        return jsonify({"message": "Code not found"}), 404
    products = [p for p in products if p["code"] != code]
    return jsonify({"message": "Product deleted"}), 204

def parse_to_database_format(d: dict) -> dict:
    if d.get("code") != None:
        new_dict = {k: d.get(k) for k in keys_to_copy}
        return new_dict
    else:
        return None

def update_with_database_format(d: dict) -> dict:
    new_dict = {k: d[k] for k in keys_to_copy if k in d}
    return new_dict
          
def get_likely_search_results(res: dict) -> dict:
    products_list = res.get("products", res.get("hits", []))
    if not products_list:
        return None
    parsed_results = [parse_to_database_format(p) for p in products_list]
    valid_results = [p for p in parsed_results if p is not None]
    return valid_results if valid_results else None
    
if __name__ == "__main__":
    app.run(debug=True)
