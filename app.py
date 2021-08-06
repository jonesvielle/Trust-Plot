from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.secret_key = "secret_key"
app.config["SECRET_KEY"] = "thisisthesecretkey"
app.config[
    "MONGO_URI"
] = "mongodb+srv://jones123:jones123@cluster0-qelfv.azure.mongodb.net/dataiot?retryWrites=true&w=majority"

mongo = PyMongo(app)


@app.route("/dashboard/")
def dashboard():
    args = request.args
    token = args["token"]
    try:
        token_decode = jwt.decode(token, app.config["SECRET_KEY"])
        return jsonify(
            {"message": "dashboard !!!!", "token": token, "decoded_token": token_decode}
        )
    except:
        return jsonify({"message": "could not decode token"})


@app.route("/add", methods=["POST"])
def add_user():
    _json = request.json
    _name = _json["name"]
    _email = _json["email"]
    _password = _json["pwd"]

    if _name and _email and _password and request.method == "POST":
        _hash_password = generate_password_hash(_password)

        id = mongo.db.user.insert(
            {"name": _name, "email": _email, "pwd": _hash_password}
        )
        if id:
            token = jwt.encode(
                {
                    "user": _name,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                },
                app.config["SECRET_KEY"],
            )
            resp = jsonify("user added successfully")
            resp.status_code = 200
            return jsonify({"token": token.decode("UTF-8")})

    else:
        return not_found()


@app.route("/login", methods=["POST"])
def login():
    _json = request.json
    _email = _json["email"]
    _password = _json["pwd"]
    user = mongo.db.user.find({"email": _email}, {"pwd": _password})
    return jsonify({"email": _email, "password": _password, "user": dumps(user)})


@app.route("/users")
def users():
    user = mongo.db.user.find()
    resp = dumps(user)
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not found" + request.url}

    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route("/users/<id>")
def user(id):
    user = mongo.db.user.find_one({"_id": ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route("/delete/<id>", methods=["DELETE"])
def delete_user(id):
    mongo.db.user.delete_one({"_id": ObjectId(id)})
    resp = jsonify("user deleted sucessfulltt")
    resp.status_code = 200
    return resp


@app.route("/update/<id>", methods=["PUT"])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json["name"]
    _email = _json["email"]
    _password = _json["pwd"]
    if _name and _email and _password and _id and request.method == "PUT":
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.update_one(
            {"_id": ObjectId(_id["$oid"]) if "$oid" in _id else ObjectId(_id)},
            {"$set": {"name": _name, "email": _email, "pwd": _password}},
        )
        resp = jsonify("user updated")
        resp.status_code = 200
        return resp
    else:
        return not_found()


if __name__ == "__main__":
    app.run(debug=True)

