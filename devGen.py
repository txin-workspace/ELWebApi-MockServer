import json
import random
import string
import os
import time
import json

import static

dict_comm_dd = {}
output_props_path = ''

def init():
    global dict_comm_dd
    # load common items dd
    comm_dd_file = open('./dd/commonItems.json', mode = 'r')
    dict_comm_dd = json.load(comm_dd_file)['properties']
    comm_dd_file.close()
    # make properties json files dir
    dir_path = './properties_json_{}'.format(time.time())
    os.mkdir(dir_path)
    global output_props_path
    output_props_path = dir_path + '/' + 'properties/'
    os.mkdir(output_props_path)

def dd_loader(f_path: str):
    dd_file = open(f_path, mode = 'r')
    dict_dd = json.load(dd_file)
    dd_file.close()
    return dict_dd['deviceType'], dict_dd['properties']


# input dd[properties]
# output {property: value, p: v, p:v, ... ...}
def prop_generator(dict_dd_props: dict) -> dict:
    # dict_prop_val = None
    dict_prop_val = {}

    for p in dict_dd_props:
        # print('\tprocess property: ', p)

        if p == 'manufacturer':
            m_code = random.choice(static.manufacturers_code)
            while True:
                if m_code in static.manufacturers_ja and m_code in static.manufacturers_en:
                    break
                m_code = random.choice(static.manufacturers_code)
            
            dict_prop_val['manufacturer'] = {
                "code": m_code, 
                "descriptions": {
                    "ja": static.manufacturers_ja[m_code],
                    "en": static.manufacturers_en[m_code]
                }
            }
         
        elif p == 'protocol':
            dict_prop_val['protocol'] = {
                "type": "ECHONET_Lite v1.0",
                "version": "Rel.A"
            }

        elif p == 'installationLocation':
            p_val = random.choice(static.locations)
            dict_prop_val['installationLocation'] = p_val

        else:            
            dict_prop_val[p] = schema_type_switcher(dict_dd_props[p]['schema'])

    return dict_prop_val


def schema_type_switcher(dict_schema: dict):
    if 'oneOf' in dict_schema:
        return value_random_oneOf(dict_schema['oneOf'])

    elif dict_schema['type'] == 'number':
        num_max = 100
        num_min = 0
        if 'minimum' in dict_schema:
            num_min = dict_schema['minimum']
        if 'maximum' in dict_schema:
            num_max = dict_schema['maximum']
        if num_max <= num_min:
            num_max = num_min * 2

        if 'multipleOf' in dict_schema:
            return value_random_multiple(num_min, num_max, dict_schema['multipleOf'])
        else:
            return value_random_int(num_min, num_max)

    elif dict_schema['type'] == 'boolean':
        if 'values' in dict_schema:
            return value_random_values(dict_schema['values'])
        else:
            return value_random_normal_boolean()

    elif dict_schema['type'] == 'string':
        if 'format' in dict_schema:
            if dict_schema['format'] == 'date':
                return value_random_date()
            elif dict_schema['format'] == 'time':
                return value_random_time()
            elif dict_schema['format'] == 'date-time':
                return value_random_dt()
            else:
                print('other string format', dict_schema['format'])

        elif 'enum' in dict_schema:
            return value_random_enum(dict_schema['enum'])
        else:
            return value_random_normal_str()

    elif dict_schema['type'] == 'object':
        return value_random_obj(dict_schema['properties'])

    elif dict_schema['type'] == 'array':
        return value_random_array(dict_schema)

    else:
        print('other properties type: ', dict_schema['type'])    


def value_random_normal_boolean() -> bool:
    return random.choice([True, False])


def value_random_int(min, max) -> int:
    return random.randint(min, max)


def value_random_multiple(min, max, multiple):
    if multiple == 1:
        return value_random_int(min, max)

    elif multiple < 1:
        return value_random_float(min, max, multiple)
        
    else:
        # multiple_int
        val = random.randint(min, max)
        val -= val % multiple
        if val > max or val < min:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WRONG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", min, max, multiple, val)
        return val


def value_random_float(min, max, multiple: float) -> float:
    return round(random.uniform(min, max), len(str(multiple).split('.')[1]))


def value_random_values(values: list):
    return values[random.randint(0, len(values) -1)]['value']


def value_random_dt() -> str:
    year_l2 = random.randint(0, 22)
    month = random.randint(0, 12)
    d = random.randint(1, 28)
    h = random.randint(0, 23)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return '20{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(year_l2, month, d, h, m, s)


def value_random_date() -> str:
    year_l2 = random.randint(0, 22)
    month = random.randint(0, 12)
    d = random.randint(1, 28)
    return '20{:02d}-{:02d}-{:02d}'.format(year_l2, month, d)
    

def value_random_time() -> str:
    h = random.randint(0, 23)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return '{:02d}:{:02d}:{:02d}'.format(h, m, s)


def value_random_oneOf(list_oneof: list):
    random_select = list_oneof[random.randint(0, len(list_oneof) -1)]
    # selected_hash = hashlib.md5(json.dumps(random_select).encode('utf-8')).hexdigest()
    # return {
    #     'hash': selected_hash,
    #     'value': schema_type_switcher(random_select)
    # }
    return schema_type_switcher(random_select)


def value_random_enum(list_enum: list):
    return list_enum[random.randint(0, len(list_enum) -1)]


def value_random_obj(dict_props: dict):
    value_obj = {}
    for prop in dict_props:
        value_obj[prop] = schema_type_switcher(dict_props[prop])

    return value_obj


def value_random_normal_str() -> str:
    s = string.ascii_uppercase
    return ''.join(random.choice(s) for i in range(random.randint(10, 25)))


def value_random_array(dict_schema: dict):
    # default for no min max
    array_size_min = 0
    array_size_max = 10

    if 'minItems' in dict_schema: 
        array_size_min = dict_schema['minItems']
    if 'maxItems' in dict_schema: 
        array_size_max = dict_schema['maxItems']
    if array_size_max <= array_size_min:
        array_size_max = array_size_min *2
    
    value_arr_size = random.randint(array_size_min, array_size_max)
    value_array = []
    while len(value_array) < value_arr_size:
        value_array.append(schema_type_switcher(dict_schema['items']))

    return value_array


def props_write_file(f_name: str, dict_props: dict) -> None:
    global output_props_path
    # print('write file: ', f_name, '.json')
    file_path = output_props_path + f_name + '.json'
    props_file = open(file_path, mode = ('w'))
    props_file.write(json.dumps(dict_props))
    props_file.close()
    print('write props file finish: {}.json'.format(f_name))


def main():
    global dict_comm_dd
    init()

    # load all devices dd file path
    list_dd_file = []
    for f in os.listdir('./dd/devices/'):
        if '.json' not in f: continue
        f_path = './dd/devices/{}'.format(f)
        if os.path.isfile(f_path):
            list_dd_file.append(f_path)
    
    # write test properties
    for dd_file_path in list_dd_file:
        # one_start = time.time()
        # print('start file : ', dd_file_path)
        dd_name, dd_props = dd_loader(dd_file_path)
        device_p_v = prop_generator(dd_props)
        device_p_v.update(prop_generator(dict_comm_dd))
        props_write_file(dd_name, device_p_v)
        print('finish file : ', dd_file_path)


if __name__ == '__main__':
    main()