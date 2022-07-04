import secrets

class User:
    def __init__(self, name, pw, perm, token):
        self.name = name
        self.pw = pw
        # about permission
        # 777: full permission admin, 
        # 
        # 
        self.permission = perm
        self.token = token

class UserTable:
    def __init__():
        # {token: User}
        user_table = {}


def user_check(auth_head) -> bool:
    print('user_check header:', auth_head)
    try:
        u_token = auth_head.get('Authorization').split()[1]
    except:
        return False

    global user_token_list
    if u_token in user_token_list:
        return True
    else:
        return False

def admin_check(auth_head) -> bool:
    print('user_check header:', auth_head)
    try:
        u_token = auth_head.get('Authorization').split()[1]
    except:
        return False

    global user_token_list
    if u_token not in user_token_list:
        return False

    global user_dict
    for uid in user_dict:
        if user_dict[uid].permission == 0:
            return True

    return False

def add_user(u_name, u_pw, u_perm):
    global user_dict
    if u_name in user_dict:
        return False, None

    global user_token_list
    u_token = secrets.token_hex()
    user_dict[u_name] = User(u_name, u_pw, u_perm, u_token)
    user_token_list.append(u_token)

    return True, u_token
    
def del_user(u_name, u_pw, u_token):
    global user_dict
    if u_name not in user_dict:
        return False

    global user_token_list
    if u_token not in user_token_list:
        return False

    if user_dict[u_name].pw != u_pw:
        return False

    if user_dict[u_name].name != u_name:
        return False

    if user_dict[u_name].token != u_token:
        return False

    user_dict.pop(u_name)
    user_token_list.remove(u_token)

    return True

def show_users():
    global user_dict
    list_users = []
    for u_id in user_dict:
        list_users.append(
            {
                'u_name': user_dict[u_id].name, 
                'u_pw': user_dict[u_id].pw, 
                'u_token': user_dict[u_id].token, 
                'u_permission': ('admin') if (user_dict[u_id].permission == 0) else ('visitor')
            }
        )

    return list_users

def token_reset(u_name, u_pw):
    global user_dict
    if u_name not in user_dict:
        return False, None

    if user_dict[u_name].pw != u_pw:
        return False, None

    if user_dict[u_name].name != u_name:
        return False, None

    global user_token_list
    user_token_list.remove(user_dict[u_name].token)
    n_token = secrets.token_hex()
    user_dict[u_name].token = n_token

    return True, n_token