import sys
from json import dumps, loads
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
    return render_template('invoice_creator.html', token=return_register['token'])

@app.route("/user/login", methods=['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']

    return_login = login(email, password)
    data = dumps({
        'auth_user_id': return_login['auth_user_id'],
        'token': return_login['token']
    })
    
    return render_template('invoice_creator.html', token=return_login['token'])
    
#''' CONVERT TO XML FUNCTION '''
@app.route("/invoice/create/v1", methods = ['POST'])
def create_xml_route():
    #info = request.get_json()
    token = request.form['JWTToken']
    
    invoice_dict = { 'InvoiceTypeCode' : 380,
        'AllowanceCharge' : {
            'ChargeIndicator' : request.form['ChargeIndicator'],
            'AllowanceChargeReason' : request.form['AllowanceChargeReason'],
            'Amount' : request.form['Amount'],
            'TaxCategory' : {   'ID' : request.form['TaxCategoryID'],
                'Percent' : request.form['Percent'],
                'TaxScheme' : { 'ID' : request.form['TaxSchemeID']},
                            },
                    },

        'LegalMonetaryTotal' : {'LineExtensionAmount' : request.form['LineExtensionAmount'],
                                'TaxExclusiveAmount' : request.form['TaxExclusiveAmount'],
                                'TaxInclusiveAmount' : request.form['TaxInclusiveAmount'],
                                'ChargedTotalAmount' : request.form['ChargedTotalAmount'],
                                'PayableAmount' : request.form['PayableAmount'],
                                },

        'InvoiceLine' : [
            {
                'ID' : request.form['InvoiceLineID'],
                'InvoiceQuantity' : request.form['InvoicedQuantity'],
                'LineExtensionAmount' : request.form['LineExtensionAmount'],
                'Price' : {
                    'PriceAmount' : request.form['PriceAmount'],
                        }
            }
                        ],
                    }
    
    
    data_read_v1(token, invoice_dict)
    create_invoice_v1(token)
    
    return render_template('display_invoice.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=0)