import sys
from json import dumps, loads
from tabnanny import check
from flask import Flask, request, Response, render_template
from source.data_read import data_read_v1
from source.data_list import data_list_v1
from source.login import login
from source.logout import logout
from source.register import register
from source.create_xml import create_invoice_v1
from source.helpers_auth import check_valid_token, decode_token
from source.database import data

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/register")
def register_page():
    return render_template('register.html')

#''' AUTH FUNCTIONS '''
@app.route("/user/register", methods=['POST'])
def user_register():
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    return_register = register(email, password, first_name, last_name)
    data = dumps({
        'auth_user_id': return_register['auth_user_id'],
        'token': return_register['token'],  
    })
    return render_template('invoice_creator.html', data=data)

@app.route("/user/login", methods=['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']

    return_login = login(email, password)
    data = dumps({
        'auth_user_id': return_login['auth_user_id'],
        'token': return_login['token']
    })
    
    return render_template('invoice_creator.html', data=data)
    

# @app.route("/user/logout", methods=['POST'])
# def user_logout():
#    # No option to logout

# #''' DATA FUNCTION '''
# @app.route("/data/read/v1", methods = ['POST'])
# def data_read_route():
#     # merged
   

# @app.route("/data/list/v1", methods = ['GET'])
# def data_list_route():
#     # merged

#''' CONVERT TO XML FUNCTION '''
@app.route("/invoice/create/v1", methods = ['POST'])
def create_xml_route():
    
    return render_template('display_invoice.html')

# @app.route("/invoice/xml/v1", methods = ['GET'])
# def create_xml_v1():
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=0)