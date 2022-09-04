from flask import request, Response
import base64
from functools import wraps

def check(authorization_header):
    username = "toto"
    password = "titi"
    encoded_uname_pass = authorization_header.split()[-1]
    str  = username + ":" + password
    if encoded_uname_pass == base64.b64encode(str.encode("utf-8")).decode('utf-8'):
        return True

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401
        return f(*args, **kwargs)
    return decorated            
