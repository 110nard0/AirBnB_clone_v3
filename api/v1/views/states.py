#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    data_state = storage.all(state)
    return jsonify([obj.to_dict() for obj in data_state.value()])


@app_views.route('/api/v1/states/<int: state_id>', methods=['GET'])
def state_by_id(state_id):
    """Retrieves a State object"""
    state = storage.get("state: ", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<int: state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete state object"""
    state = storage.get("states", state_id)
    if not state:
        abort(404)
        state.delete()
        storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/api/v1/states', methods=['POST'])
def create_post():
    """Post new state oblect"""
    state_n = request.get_json(state)
    if not state_n:
        abort(404, "Not a JSON")
    if "name" not in state_n:
        abort(404, "Missing name")
    state = State(**state_n)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)
