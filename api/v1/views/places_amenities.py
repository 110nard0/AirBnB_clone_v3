#!/usr/bin/python3
""" View for Place and Amenity objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place, place_amenity
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(get_amenities(place))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenities(place_id, amenity_id):
    """ Deletes an Amenity object of a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenities = get_amenities(place)
    if amenity.to_dict() not in amenities and amenity_id not in amenities:
        abort(404)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenities(place_id, amenity_id):
    """ Links an Amenity object linked to a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    amenities = get_amenities(place)
    if amenity.to_dict() in amenities or amenity_id in amenities:
        return make_response(jsonify(amenity.to_dict()), 200)

    if type(storage).__name__ == 'DBStorage':
        # amenity.place_amenities.append(place)
        place.amenities.append(amenity)
        # place_amenity(place_id, amenity_id)
    else:
        place.amenity_id.append(amenity_id)
    return make_response(jsonify(amenity.to_dict()), 201)


def get_amenities(place):
    """ Set storage and retrieve Amenities stored in Place object """
    if type(storage).__name__ == 'DBStorage':
        amenity_list = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenity_list = [amenity_id for amenity_id in place.amenity_ids]
    return amenity_list
