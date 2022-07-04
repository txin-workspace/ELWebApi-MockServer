from flask import Blueprint
from flask import request
from flask import abort
# from flask_cors import CORS

from GlobalVariable import u_table

usermanage = Blueprint('usermanage', __name__)
# CORS(usermanage)

@usermanage.errorhandler(401)
def not_found(error):
    return {"type": "referenceError","message": "Token not allowed"}, 401

@usermanage.errorhandler(404)
def not_found(error):
    return {"type": "referenceError","message": "HTTP method or path is wrong"}, 404


# {user:'', password:''}
# response 200, token
@usermanage.route('/admin/userCreate', methods=['POST'], strict_slashes = False)
def user_create():
    if not u_table.admin_check(request.headers):
        abort(401)

    u_json = request.get_json()
    status, user_token = u_table.add_user(u_json['user'], u_json['password'], 1)

    if status == False:
        return 'add user faild', 406
    else:
        return user_token, 200

@usermanage.route('/admin/adminCreate', methods=['POST'], strict_slashes = False)
def admin_create():
    if not u_table.admin_check(request.headers):
        abort(401)

    u_json = request.get_json()
    status, user_token = u_table.add_user(u_json['user'], u_json['password'], 0)

    if status == False:
        return 'add user faild', 406
    else:
        return user_token, 200

@usermanage.route('/admin/usersShow', methods=['GET'], strict_slashes = False)
def user_show():
    if not u_table.admin_check(request.headers):
        abort(401)

    return {'users':u_table.show_users()}, 200

# {user:'', password:'', token:''}
# response 200
@usermanage.route('/admin/userDel', methods=['POST'], strict_slashes = False)
def user_del():
    if not u_table.admin_check(request.headers):
        abort(401)

    u_json = request.get_json()
    if u_table.del_user(u_json['user'], u_json['password'], u_json['token']):
        return 'success', 200
    else:
        return 406

# {user:'', password:''}
# response 200, new_token
@usermanage.route('/admin/userTokenReset', methods=['POST'], strict_slashes = False)
def user_token_reset():
    if not u_table.admin_check(request.headers):
        abort(401)

    u_json = request.get_json()
    status, n_token = u_table.token_reset(u_json['user'], u_json['password'])

    if status == False:
        return 406
    else:
        return n_token, 200