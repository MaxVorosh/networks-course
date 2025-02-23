from flask import Flask, request, send_file
from http import HTTPStatus


class Product:
    def __init__(self, id, name, description, icon=""):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description, "icon": self.icon}


app = Flask(__name__)
storage = {}
next_id = 0


@app.route("/products")
def get_list():
    return list(map(lambda x: x.to_dict(), storage.values())), HTTPStatus.OK


@app.route("/product", methods=["POST"])
def add_product():
    global next_id, storage
    json_data = request.json
    if "name" not in json_data or "description" not in json_data:
        return "Not enough info", HTTPStatus.BAD_REQUEST
    storage[next_id] = Product(next_id, json_data["name"], json_data["description"])
    next_id += 1
    return storage[next_id - 1].to_dict(), HTTPStatus.CREATED


@app.route("/product/<int:product_id>")
def get_product(product_id):
    if product_id not in storage:
        return "No product", HTTPStatus.BAD_REQUEST
    return storage[product_id].to_dict(), HTTPStatus.OK


@app.route("/product/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    if product_id not in storage:
        return "No product", HTTPStatus.BAD_REQUEST
    json_data = request.json
    product = storage[product_id]
    if "id" in json_data:
        try:
            product.id = int(json_data["id"])
        except:
            return "Id not a number", HTTPStatus.BAD_REQUEST
    if "name" in json_data:
        product.name = json_data["name"]
    if "description" in json_data:
        product.description = json_data["description"]
    storage.pop(product_id)
    storage[product.id] = product
    return product.to_dict(), HTTPStatus.OK


@app.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    if product_id not in storage:
        return "No product", HTTPStatus.BAD_REQUEST
    product = storage[product_id]
    storage.pop(product_id)
    return product.to_dict(), HTTPStatus.OK


@app.route("/product/<int:product_id>/image")
def get_icon(product_id):
    if product_id not in storage:
        return "No product", HTTPStatus.BAD_REQUEST
    product = storage[product_id]
    if product.icon == "":
        return "", HTTPStatus.NO_CONTENT
    return send_file(storage[product_id].icon), HTTPStatus.OK


@app.route("/product/<int:product_id>/image", methods=["POST"])
def set_icon(product_id):
    if product_id not in storage:
        return "No product", HTTPStatus.BAD_REQUEST
    request_data = request.files
    if "icon" not in request_data:
        return "Invalid json", HTTPStatus.BAD_REQUEST
    filename = f"icons/{product_id}.png"
    img_data = request_data["icon"]
    img_data.save(filename)
    storage[product_id].icon = filename
    return "", HTTPStatus.OK


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)