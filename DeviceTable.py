class Device:
    def __init__(self, id, desc, p_list) -> None:
        self.id = id
        self.desc = p_list
        self.prop_list = desc

        self.info = {
            'id': id,
            'deviceType': desc['deviceType'],
            "protocol": {"type": "ECHONET_Lite v1.1","version": "Rel.A"},
            'manufacturer': p_list['manufacturer']
        }

    def print_me(self):
        return self.prop_list

class DeviceTable:
    def __init__(self):
        # {id: Device}
        self.device_table = {}
    
    # C
    def add_device():
        return


    # R
    def get_device():
        return

    def get_prop():
        return

    def get_device_props():
        return

    def get_infos():
        return

    def get_device_desc():
        return
    

    # U
    def update_prop():
        return
    
    def update_device_props():
        return


    # D
    def del_device():
        return