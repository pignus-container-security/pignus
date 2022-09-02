"""Controller Model - Base

"""
from flask import make_response, request, jsonify


def get_model(model, entity_id: int = None) -> dict:
    """Base GET operation for a model.
    :unit-test: TestCtrlModelsBase::test__get_model
    """
    entity = model()

    data = {
        "status": "Error",
        "message": "",
        "object": {},
        "object_type": entity.model_name
    }
    if not entity_id:
        data["message"] = "Missing entity ID"
        return make_response(jsonify(data), 401)

    if not entity.get_by_id(entity_id):
        data["message"] = "Could not find Entity"
        return make_response(jsonify(data), 404)

    data["status"] = "Success"
    data["object"] = entity.json()
    return data


def post_model(model, entity_id: int = None):
    """Base POST operation for a model. Create or modify a entity."""
    data = {
        "status": "Error"
    }
    request_data = request.get_json()

    # print("\n\n")
    # print(request_data)
    # print("\n\n")

    entity = model()

    # Search for the entity by it's ID.
    entity_id_field = "%s_id" % entity.model_name
    if entity_id or entity_id_field in request_data:
        search_id = None
        if entity_id:
            search_id = entity_id
        elif entity_id_field in request_data:
            search_id = request_data[entity_id_field]

        if not entity.get_by_id(search_id):
            data["status"] = "Error"
            data["message"] = "Could not find %s ID: %s" % (entity.model_name, entity_id)
            return jsonify(data), 404

    data["object"] = entity.json()
    data["object_type"] = entity.model_name

    # if "name" in request_data:
    #     user.name = request_data["name"]

    # if "role_id" in request_data:
    #     user.role_id = request_data["role_id"]

    # user.save()
    # resp_data["object"] = user.json()
    return data


def delete_model(model, entity_id: int):
    """Base DELETE a model."""
    entity = model()
    data = {
        "status": "Success",
        "object_type": entity.model_name
    }
    if not entity.get_by_id(entity_id):
        data["status"] = "Error"
        data["message"] = "Entity not found"
        return make_response(jsonify(data), 404)
    entity.delete()
    data["message"] = "User deleted successfully"
    data["object"] = entity.json()
    return data


# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_base.py
