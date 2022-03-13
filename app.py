import sys
from json import dumps, loads
from flask import Flask, request, response_class
from source.data_read import data_read_v1
from source.data_list import data_list_v1
from source.login import login
from source.logout import logout
from source.register import register
from source.create_xml import create_invoice_v1

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

''' DATA FUNCTION '''
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

''' CONVERT TO XML FUNCTION '''
@app.route("/invoice/create/v1", methods = ['POST'])
def create_xml_route():
    info = request.get_json()
    return app.response_class(create_invoice_v1(info['token']), mimetype = 'application/xml')

if __name__ == "__main__":
    app.run()