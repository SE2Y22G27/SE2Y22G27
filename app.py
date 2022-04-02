# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# import sys
from json import dumps # loads
# from tabnanny import check
from flask import Flask, request, Response
from source.data_read import data_read_v1
from source.data_list import data_list_v1
from source.login import login
from source.logout import logout
from source.register import register
from source.create_xml import create_invoice_v1
from source.helpers_auth import check_valid_token, decode_token
from source.database import data

app = Flask(__name__)

''' AUTH FUNCTIONS '''
@app.route("/user/register", methods=['POST'])
def user_register():
    info = request.get_json()
    email = info['email']
    password = info['password']
    first_name = info['first_name']
    last_name = info['last_name']

    return_register = register(email, password, first_name, last_name)
    return dumps({
        'auth_user_id': return_register['auth_user_id'],
        'token': return_register['token'],
    })

@app.route("/user/login", methods=['POST'])
def user_login():
    info = request.get_json()
    email = info['email']
    password = info['password']

    return_login = login(email, password)
    return dumps({
        'auth_user_id': return_login['auth_user_id'],
        'token': return_login['token']
    })

@app.route("/user/logout", methods=['POST'])
def user_logout():
    info = request.get_json()
    token = info['token']
    logout(token)
    return dumps({})

# DATA FUNCTION
@app.route("/data/read/v1", methods = ['POST'])
def data_read_route():
    info = request.get_json()
    data_read_v1(info['token'], info['invoice'])
    return dumps({})

@app.route("/data/list/v1", methods = ['GET'])
def data_list_route():
    token = request.args.get('token')
    invoice_dict = data_list_v1(token)
    return dumps(invoice_dict)

# CONVERT TO XML FUNCTION
@app.route("/invoice/create/v1", methods = ['POST'])
def create_xml_route():
    info = request.get_json()
    create_invoice_v1(info['token'])
    return dumps({})

@app.route("/invoice/xml/v1", methods = ['GET'])
def return_xml_rout():
    token = request.args.get('token')
    data_info = data.get_data()
    check_valid_token(token)
    user_id = decode_token(token)
    for user in data_info['users']:
        if user['user_id'] == user_id:
            root = user['xmlroot']
    return Response(root,mimetype='txt/xml')

@app.route("/data/xml/v1", methods=['POST'])
def data_xml_route():
    info = request.get_json()
    data_read_v1(info['token'], info['invoice'])
    create_invoice_v1(info['token'])
    return dumps({})

if __name__ == "__main__":
    app.run()
