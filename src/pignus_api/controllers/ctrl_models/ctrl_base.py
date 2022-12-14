"""Controller Model - Base

"""
from flask import make_response, request, jsonify

from pignus_shared.utils import log


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
    print("\n\n")
    print(request_data)
    print("\n\n")

    entity = model()

    if not entity.get_by_id(entity_id):
        data["status"] = "Error"
        data["message"] = "Could not find %s ID: %s" % (entity.model_name, entity_id)
        return jsonify(data), 404
    else:
        log.info("POST - Found entity: %s" % entity)

    # Check through the fields and see if they should be applied to the model.
    for field_name, field_value in request_data.items():
        print("%s\t%s" % (field_name, field_value))
        update_field = False
        # This could be optimized.
        for entity_field in entity.field_map:
            if entity_field["name"] == field_name:
                if field_name not in entity.api_writeable_fields:
                    data["status"] = "Error"
                    data["message"] = "Cant modify field: %s" % field_name
                    return jsonify(data, 400)
                else:
                    update_field = True
        if update_field:
            setattr(entity, field_name, field_value)

    entity.save()

    data["object"] = entity.json()
    data["object_type"] = entity.model_name

    # if "name" in request_data:
    #     user.name = request_data["name"]

    # if "role_id" in request_data:
    #     user.role_id = request_data["role_id"]

    # user.save()
    # resp_data["object"] = user.json()
    return data


# def search_id(entity_id_field: str, request_data: dict):
#     """
#     """
#     # Search for the entity by it's ID.
#     search_id = None
#     if entity_id_field in request_data:
#         search_id = None
#         if entity_id:
#             search_id = entity_id
#         elif entity_id_field in request_data:
#             search_id = request_data[entity_id_field]
#     return search_id


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
