#!/usr/bin/python3
"""
Flask states Blueprint
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.routes('/states', methods=['GET'])
def get_states():
    """list all states"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.routes('/states/<str:id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
def get_states(id):
    """list all states"""
    state = storage.get(State, id)
    if request.method == 'GET':
        if not state:
            abort(404)
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        state = storage.get(State, id)
        if not state:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({"status code": 200})

    if request.method == 'POST':
        new = request.get_json()
        if not new:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in new.keys():
            return make_response(jsonify({"error": "Missing name"}), 400)
        inst = State(**new)
        state = storage.new(inst)
        storage.save()
        return make_response(jsonify(inst.to_dict()), 201)

    if request.method == 'PUT':
        state = storage.get(State, id)
        if not state:
            abort(404)
        update = request.get_json()
        if not update:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        for key, value in update.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
