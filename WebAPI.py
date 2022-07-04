from flask import Blueprint
from flask import request
from flask import abort
# from flask_cors import CORS
from GlobalVariable import u_table, d_table

webapi = Blueprint('webapi', __name__, url_prefix='/elapi/v1/')
# CORS(webapi)

@webapi.errorhandler(401)
def not_found(error):
    return {"type": "referenceError","message": "Token not allowed"}, 401

@webapi.errorhandler(404)
def not_found(error):
    return {"type": "referenceError","message": "HTTP method or path is wrong"}, 404


@webapi.route('devices', methods=['GET'], strict_slashes = False)
def webapi_devices():

    if not u_table.user_check(request.headers):
        abort(401)

    # global device_dict

    # return_list = []
    # for d_name in device_dict:
    #     if 'co2Sensor' not in d_name:
    #         return_list.append({
    #             'id': d_name,
    #             'deviceType': re.sub('\d','', d_name),
    #             "protocol": {"type": "ECHONET_Lite v1.1","version": "Rel.A"},
    #             # 'protocol':  device_dict[d_name].prop_list.protocol,
    #             'manufacturer': device_dict[d_name].prop_list['manufacturer']
    #         })
    #     else:
    #         return_list.append({
    #             'id': d_name,
    #             'deviceType': 'co2Sensor',
    #             "protocol": {"type": "ECHONET_Lite v1.1","version": "Rel.A"},
    #             'manufacturer': device_dict[d_name].prop_list['manufacturer']
    #         })

    # return {
    #     'devices': return_list, 
    #     "hasMore": False,
    #     "limit": 100,
    #     "offset": 0
    #     }


@webapi.route('devices/<device_id>/properties', methods=['GET'], strict_slashes = False)
def webapi_search(device_id):

    if not u_table.user_check(request.headers):
        abort(401)

    global device_dict
    if device_id in device_dict:
        return device_dict[device_id].print_me()
    else:
        abort(404)


@webapi.route('devices/<device_id>/properties/<prop_name>', methods=['GET'], strict_slashes = False)
def webapi_search_one(device_id, prop_name):

    if not u_table.user_check(request.headers):
        abort(401)

    global device_dict

    if device_id not in device_dict:
        abort(404)

    if prop_name not in device_dict[device_id].prop_list:
        abort(500)

    return {prop_name: device_dict[device_id].prop_list[prop_name]}


# {prop_name: new_value}
@webapi.route('devices/<device_id>/properties/<prop_name>', methods=['PUT'], strict_slashes = False)
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