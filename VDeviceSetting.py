from flask import Blueprint
from flask import request
from flask import abort
# from flask_cors import CORS
from GlobalVariable import d_table, u_table

vdevice = Blueprint('vdevice', __name__, url_prefix='/manage/virtualdevice/')
# CORS(vdevice)

@vdevice.errorhandler(401)
def not_found(error):
    return {"type": "referenceError","message": "Token not allowed"}, 401

@vdevice.errorhandler(404)
def not_found(error):
    return {"type": "referenceError","message": "HTTP method or path is wrong"}, 404


# add one virtual devices
# {dname: dvalue, dname: dvalue , -------}
@vdevice.route('devices/<device_id>/properties', methods=['POST'], strict_slashes = False)
def webapi_create(device_id):

    if not u_table.user_check(request.headers):
        abort(401)

    global device_dict

    if device_id in device_dict:
        abort(500)

    request_data = request.get_json()
    d = Device()
    d.id = device_id
    for name, value in request_data.items():
        # d.prop_list.append({name: value})
        d.prop_list[name] = value
    
    device_dict[device_id] = d

    return {'add Device':'success'}, 200

# 
# {prop_name: new_value}
@vdevice.route('devices/<device_id>/properties/<prop_name>', methods=['PUT'], strict_slashes = False)
def webapi_update_one(device_id, prop_name):

    if not u_table.user_check(request.headers):
        abort(401)

    global device_dict
    request_data = request.get_json()

    global device_dict

    if device_id not in device_dict:
        abort(404)

    if prop_name not in request_data:
        abort(500)

    if prop_name not in device_dict[device_id].prop_list:
        abort(500)

    if type(request_data[prop_name]) != type(device_dict[device_id].prop_list[prop_name]):
        abort(500)

    device_dict[device_id].prop_list[prop_name] = request_data[prop_name]

    return {prop_name: device_dict[device_id].prop_list[prop_name]}