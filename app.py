from importlib.metadata import files
import sys
import requests
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

@app.route("/create/invoice", methods=['POST'])
def create_invoice_page():
    return render_template('invoice_creator.html', token=request.form['JWTToken'])

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
    
    


    invoice_dict = { 
        'InvoiceTypeCode' : 380,
        'InvoiceID' : request.form['InvoiceID'],
        'IssueDate' : request.form['IssueDate'],
        'AccountingSupplierParty' : {
            'Party' : 
                    {
                        'PartyIdentification': {'ID':  request.form['RegistrationID']},
                        'PartyName' : {'Name':  request.form['Name']},
                        'PostalAddress' : {
                                'StreetName' :  request.form['Street'],
                                'CityName':  request.form['City'],
                                'PostalZone' :  request.form['PostalZone'],
                                'Country' : {'IdentificationCode': 'AU'}
                        },
                        'PartyLegalEntity' : {
                            'RegistrationName' :  request.form['Name'],
                            'CompanyID' :  request.form['RegistrationID'],
                        }
                    }

                                     },
        'AccountingCustomerParty' : {
            'Party' : 
                    {
                        'PartyName' : {'Name':  request.form['Name1']},
                        'PostalAddress' : {
                                'StreetName' :  request.form['Street1'],
                                'CityName':  request.form['CityName'],
                                'PostalZone' : request.form['PostalZone'],
                                'Country' : {'IdentificationCode': 'AU'}
                        },
                        'PartyLegalEntity' : {
                            'RegistrationName' :  request.form['Name1'],
                        }
                    }

                                     },
        'PaymentMeans': {
            'PaymentMeansCode' : 1,
            'PaymentID' :  request.form['InvoiceID'],
                        },
        'PaymentTerms': {
            'Note' : 'As agreed'
                        },

        'TaxTotal' : {
            'TaxAmount' :  request.form['TaxAmount'],
            'TaxSubtotal' : {
                'TaxableAmount' :  request.form['TaxableAmount'],
                'TaxAmount' :  request.form['SubTaxAmount'],
                'TaxCategory' : {  
                     'ID' :  request.form['TaxCategoryID'],
                'Percent' :  request.form['TaxCategoryPercent'],
                'TaxScheme' : { 
                    'ID' :  request.form['TaxSchemeID']
                             }
                                },
                    },

                    },
            

        'LegalMonetaryTotal' : {'LineExtensionAmount' :  request.form['LineExtensionAmount'],
                                'TaxExclusiveAmount' : request.form['TaxExclusiveAmount'],
                                'TaxInclusiveAmount' : request.form['TaxInclusiveAmount'],
                                'PayableRoundingAmount' : request.form['PayableRoundingAmount'],
                                'PayableAmount' : request.form['PayableAmount'],
                                },

        'InvoiceLine' : [],
                    }
    
    if 'AdditionalStreet' in request.form:
        invoice_dict['AccountingSupplierParty']['Party']['PostalAddress']['AdditionalStreetName'] = request.form["AdditionalStreet"]
    if 'AdditionalStreet1' in request.form:
        invoice_dict['AccountingCustomerParty']['Party']['PostalAddress']['AdditionalStreetName'] = request.form["AdditionalStreet1"]

    digit = 0

    while 'ID'+f"{digit}" in request.form:
        invoice_line_dict = {
                'ID' :  request.form['ID'+f"{digit}"],
                'InvoiceQuantity' : request.form['InvoiceQuantity'+f"{digit}"],
                'LineExtensionAmount' : request.form['LineExtensionAmount'+f"{digit}"],
                'Item' : {
                    'Name' : request.form['ItemName'+f"{digit}"],
                    'ClassifiedTaxCategory': {
                        'ID':request.form['ClassifiedTaxCategoryID'+f"{digit}"],
                        'Percent': request.form['ClassifiedTaxCategoryPercent'+f"{digit}"],
                        'TaxScheme': {'ID' :request.form['ClassifiedTaxCategoryTaxSchemeID'+f"{digit}"]},
                    },
                },
                'Price' : {
                    'PriceAmount' : request.form['PriceAmount'+f"{digit}"],
                    'BaseQuantity' : request.form['BaseQuantity'+f"{digit}"],
                        },
            }
        invoice_dict['InvoiceLine'].append(invoice_line_dict)
        digit = digit + 1

    data_read_v1(token, invoice_dict)
    create_invoice_v1(token)
    
    validation_endpoint = "http://invoicevalidation.services:8080/verify_invoice"
    user_id = decode_token(token)
    files = {'invoice': open(f"{user_id}"+"_invoice.xml",'rb')}
    data_dict = {
        'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJncm91cF9pZCI6NX0.GoDgfC3GzSjjOgKhntzyd37euX0ec-v5G4P-rKG7V3A',
        'rules' : 3,
        'output_type' : 'json'
    }
    response = requests.post(url = validation_endpoint, files= files, data = data_dict)
    data = response.json()
    
    if response.status_code != 200:
        print("server is out!!!")
    if data['message']['valid'] == True:
        rendering_endpoint = "https://www.invoicerendering.com/einvoices/v2"
        param = {
            'renderType' : "html",
            'lang' : "en"
        }
        files = {
            'xml' : open(f"{user_id}"+"_invoice.xml","rb")
        }
        response = requests.post(url= rendering_endpoint, params= param, files= files)
        if response.status_code == 200:
            f = open(f"{user_id}"+"render.html", "w")
            f.write(response.text)
        print(response.text)

    return render_template('display_invoice.html', token=token)
    

@app.route("/invoice/send/v1", methods = ['POST'])
def send_invoice():
    
    return render_template('success.html', email=request.form['email'], token=request.form['JWTToken'])
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=0)