from json import dumps, loads
from flask import Flask, request, send_from_directory
from error import InputError
from source.data_read import data_read_v1
from database import data
from source.login import login
from source.logout import logout
from source.register import register
from source.create_xml import create_invoice_v1

APP = Flask(__name__)

''' AUTH FUNCTIONS '''
@APP.route("/user/register", methods=['POST'])
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

@APP.route("/user/login", methods=['POST'])
def user_login():
    info = request.get_json()
    email = info['email']
    password = info['password']

    return_login = login(email, password)
    return dumps({
        'auth_user_id': return_login['auth_user_id'],
        'token': return_login['token']
    })

@APP.route("/user/logout", methods=['POST'])
def user_logout():
    info = request.get_json()
    token = info['token']
    logout(token)
    return dumps({})

''' DATA FUNCTION '''
@APP.route("/data/read/v1", methods = ['POST'])
def data_read_route():
    info = request.get_json()
    data_read_v1(info['token'], info['invoice'])
    return dumps({})

@APP.route("/data/list/v1", methods = ['GET'])
def data_read_route():
    info = request.get_json()
    invoice_dict = data_read_v1(info['token'])
    return dumps(invoice_dict)

''' CONVERT TO XML FUNCTION '''
@APP.route("/createXML/v1", methods = ['GET'])
def create_xml_route():
    info = request.get_json()
    create_invoice_v1(info['token'])
    return dumps({})

if __name__ == "__main__":
    APP.run()