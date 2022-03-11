from json import dumps, loads
from flask import Flask, request, send_from_directory
from error import InputError
from source.data_read import data_read_v1
from database import data
from source.login import login
from source.logout import logout
from source.register import register
from source.convertXML import convertXML

APP = Flask(__name__)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

''' AUTH FUNCTIONS '''


''' DATA READ FUNCTION '''
@APP.route("/data/read/v1", methods = ['POST'])
def data_read_route():
    info = request.get_json()
    data_read_v1(info['token'], info['invoice'])
    return {}

''' CONVERT TO XML FUNCTION '''


if __name__ == "__main__":
    APP.run()