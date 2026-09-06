from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

products = [
    {"id": 1, "name": "Keyboard", "price": 49.99},
    {"id": 2, "name": "Mouse", "price": 29.99}
]


# --------------------------------
# HOME PAGE
# --------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------
# GET - Get all products
# --------------------------------
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# --------------------------------
# SEARCH PRODUCTS
# --------------------------------
@app.route("/api/search", methods=["GET"])
def search():

    # Get search value from URL
    query = request.args.get("q", "").strip().lower()

    results = []

    for product in products:

        if query in product["name"].lower():
            results.append(product)

    return jsonify(results)


# --------------------------------
# POST - Add a new product
# --------------------------------
@app.route("/products", methods=["POST"])
def add_product():

    data = request.get_json()

    new_product = {
        "id": len(products) + 1,
        "name": data.get("name"),
        "price": data.get("price")
    }

    products.append(new_product)

    return jsonify({
        "message": "Product added",
        "product": new_product
    }), 201


# --------------------------------
# PUT - Update complete product
# --------------------------------
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    for product in products:

        if product["id"] == id:

            data = request.get_json()

            product["name"] = data["name"]
            product["price"] = data["price"]

            return jsonify(product), 200

    return jsonify({
        "message": "Product not found"
    }), 404


# --------------------------------
# PATCH - Update part of product
# --------------------------------
@app.route("/products/<int:id>", methods=["PATCH"])
def patch_product(id):

    data = request.get_json()

    for product in products:

        if product["id"] == id:

            if "name" in data:
                product["name"] = data["name"]

            if "price" in data:
                product["price"] = data["price"]

            return jsonify({
                "message": "Product updated successfully",
                "product": product
            }), 200

    return jsonify({
        "message": "Product not found"
    }), 404


# --------------------------------
# DELETE - Delete product
# --------------------------------
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):

    for product in products:

        if product["id"] == id:

            products.remove(product)

            return jsonify({
                "message": "Product deleted successfully",
                "product": product
            }), 200

    return jsonify({
        "message": "Product not found"
    }), 404


# --------------------------------
# HEAD
# --------------------------------
@app.route("/products/<int:id>", methods=["HEAD"])
def head_product(id):

    for product in products:

        if product["id"] == id:
            return "", 200

    return "", 404


# --------------------------------
# OPTIONS
# --------------------------------
@app.route("/products", methods=["OPTIONS"])
def options_products():

    response = jsonify({
        "message": "Supported methods are GET, POST, PUT, PATCH, DELETE, HEAD and OPTIONS"
    })

    response.headers["Allow"] = (
        "GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS"
    )

    return response, 200


# --------------------------------
# RUN SERVER
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)
