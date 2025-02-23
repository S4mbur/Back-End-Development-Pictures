from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for, redirect

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """Return length of data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Returns all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Returns a single picture by its ID"""
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture is None:
        return jsonify({"error": "Picture not found"}), 404
    return jsonify(picture), 200

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Creates a new picture entry"""
    new_picture = request.get_json()
    if not new_picture or "id" not in new_picture:
        return jsonify({"error": "Invalid request data"}), 400

    # Check if 'id' already exists and return a duplicate message with a 302
    if any(pic["id"] == new_picture["id"] for pic in data):
        return jsonify({
            "Message": f"picture with id {new_picture['id']} already present"
        }), 302

    data.append(new_picture)  # Add new picture
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates an existing picture"""
    updated_picture = request.get_json()
    if not updated_picture:
        return jsonify({"error": "Invalid request data"}), 400

    for index, pic in enumerate(data):
        if pic["id"] == id:
            data[index] = updated_picture
            return jsonify(updated_picture), 200

    return jsonify({"error": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Deletes a picture by ID"""
    global data
    initial_length = len(data)
    data = [pic for pic in data if pic["id"] != id]
    if len(data) == initial_length:
        return jsonify({"error": "Picture not found"}), 404
    return make_response('', 204)
