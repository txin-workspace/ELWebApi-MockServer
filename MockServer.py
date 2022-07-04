from DeviceTable import DeviceTable
from UserTable import UserTable
from GlobalVariable import d_table, u_table

from flask import Flask
from flask_cors import CORS
    
app = Flask(__name__)
CORS(app)

from WebAPI import webapi
app.register_blueprint(webapi)

from VDeviceSetting import vdevice
app.register_blueprint(vdevice)

from UserManagement import usermanage
app.register_blueprint(usermanage)


def init():
    d_table = DeviceTable()
    u_table = UserTable()
    print('default admin user token: ', u_table.get_token('default'), '')

def main():
    # print('add hard code user')
    # user_dict['default'] = User('default', 'default', 0, '4ecdf33ff128e03f2be5341388f60a8f16f9e071d2014bae8b9567417c601494')
    # user_token_list.append('4ecdf33ff128e03f2be5341388f60a8f16f9e071d2014bae8b9567417c601494')
    print('init')
    init()

    print('start server')
    app.run(host='0.0.0.0', port='5000', debug=True)

if __name__ == '__main__':
    main()