#!/usr/bin/python3
"""
Flask states Blueprint
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app.teardown_appcontext
def app_close(exception=None):
    """ Teardown method """
    storage.close()


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def get_states_cities(state_id):
    """get create delete update any states"""
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        state = storage.get(State, state_id)
        if not state:
            abort(404)

        new = request.get_json()
        if not new:
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        if "name" not in new.keys():
            return make_response(jsonify({"error": "Missing name"}), 400)
        inst = City(**new)
        inst.state_id = state_id
        city = storage.new(inst)
        storage.save()
        return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def change_cities(city_id):
    """get create delete update any states"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({"status code": 200})

    if request.method == 'PUT':
        city = storage.get(State, city_id)
        if not city:
            abort(404)
        update = request.get_json()
        if not update:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

        for key, value in update.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
