from flask import Flask
from flask import request
# from flask import Response
from flask_cors import CORS

import json
import re
import copy


class Device:
    def __init__(self, dev_id) -> None:
        self.id = dev_id
        self.info = {}
        self.props = {}
        self.dd = {}

    def __str__(self):
        return {
            'id': self.id,
            'info': self.info,
            'properties': self.props,
        }

    def __format__(self):
        pass


app = Flask(__name__)
CORS(app)

device_dict = {}


# get all device info
# /elapi/v1/devices?offset=123&limit=123
@app.route('/elapi/v1/devices', methods=['GET'], strict_slashes=False)
def testAPI_devices():

    global device_dict

    return_list = []

    offset = request.args.get('offset', default = 0, type = int)
    limit = request.args.get('limit', default = 0, type = int)

    offect_count = 0
    limit_count = 0

    for d_name in device_dict:
        if offset != 0 and offect_count < offset:
            offect_count += 1
            continue

        if limit == 0 or (limit != 0 and limit_count < limit):
            return_list.append(device_dict[d_name].info)
            limit_count += 1
        
        else:
            break
    

    if limit != 0:
        has_more = False
        if len(device_dict) > offset + limit:
            has_more = True

        return {
            'devices': return_list,
            'hasMore': has_more,
            'limit': limit,
            'offset': offset
        }
    else:
        return {
            'devices': return_list,
            'hasMore': False,
            'limit': None,
            'offset': None
        }


# get one device dd
@app.route('/elapi/v1/devices/<device_id>', methods = ['GET'], strict_slashes=False)
def testAPI_get_device(device_id):
    
    global device_dict

    if device_id not in device_dict:
        return {'error': 'deivce id not exist'}, 404

    return device_dict[device_id].dd, 200

    

# create one deivce
# {info:{} , props:{}}
@app.route('/elapi/v1/devices/<device_id>', methods=['POST'], strict_slashes=False)
def testAPI_create(device_id):

    global device_dict

    if device_id in device_dict:
        return {'error': 'deivce id existed'}, 400

    request_data = request.get_json()
    d = Device(device_id)

    if 'info' not in request_data:
        return {'error': 'info part not in request body'}, 400

    if 'properties' not in request_data:
        return {'error': 'properties part not in request body'}, 400

    if 'dd' not in request_data:
        return {'error': 'dd part not in request body'}, 400

    device_dict[device_id] = Device(device_id)
    device_dict[device_id].info = request_data['info']
    device_dict[device_id].props = request_data['properties']
    device_dict[device_id].dd = request_data['dd']

    return {device_id: 'created'}, 200



# delete one device
@app.route('/elapi/v1/devices/<device_id>', methods = ['DELETE'], strict_slashes=False)
def testAPI_del_device(device_id):
    
    global device_dict

    if device_id not in device_dict:
        return {'error': 'deivce id not exist'}, 404

    request_data = request.get_json()
    if 'device_id' not in request_data:
        return {'error': 'device id not in request body'}, 400

    if device_id != request_data['device_id']:
        return {'error': 'device id not not correct'}, 400

    del device_dict[device_id]

    return {device_id: 'deleted'}, 200



# get one device properties
@app.route('/elapi/v1/devices/<device_id>/properties', methods=['GET'], strict_slashes=False)
def testAPI_search(device_id):

    global device_dict

    if device_id in device_dict:
        return device_dict[device_id].props, 200

    else:
        return {'error': 'device id not exist'}, 404



# get one deivce one peroperty
@app.route('/elapi/v1/devices/<device_id>/properties/<prop_name>', methods=['GET'], strict_slashes=False)
def testAPI_search_one(device_id, prop_name):

    global device_dict

    if device_id not in device_dict:
        return {'error': 'deivce not exist'}, 404

    if prop_name not in device_dict[device_id].props:
        return {'error': 'property name not exist'}, 404

    return {prop_name: device_dict[device_id].props[prop_name]}



# change one device one property value
# {prop_name: new_value}
@app.route('/elapi/v1/devices/<device_id>/properties/<prop_name>', methods=['PUT'], strict_slashes=False)
def testAPI_update_one(device_id, prop_name):

    global device_dict
    
    request_data = request.get_json()

    global device_dict

    if device_id not in device_dict:
        return {'error': 'device id not exist'}, 404

    if prop_name not in request_data:
        return {'error': 'bad request format, no property name in body'}, 400

    if prop_name not in device_dict[device_id].props:
        return {'error': 'property name not exist'}, 404

    if type(request_data[prop_name]) != type(device_dict[device_id].props[prop_name]):
        return {'error': 'bad request, property value type wrong'}, 400

    device_dict[device_id].props[prop_name] = request_data[prop_name]

    return {prop_name: device_dict[device_id].props[prop_name]}



def main():
    print('start server')
    app.run(host='0.0.0.0', port='5000', debug=True)


if __name__ == '__main__':
    main()
