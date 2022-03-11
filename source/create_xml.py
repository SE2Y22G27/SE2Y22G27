import xml.etree.ElementTree as ET
from source.database import data as database
from source.helpers_auth import check_valid_token, decode_token

# https://docs.python.org/3.8/library/xml.etree.elementtree.html
# contains all the library functions

def create_invoice_v1(token):
    '''

    Arguments:
        token (string) : Username thats encrypted into JWT token

    Exceptions:
        - invalid token

    Returns:
        {}
    
    '''
    data_info = database.get_data()

    # ----- Error handling -----
    # check whether the token is valid 
    check_valid_token(token)
    user_id = decode_token(token)

    invoice_dict = {}
    # Find the user
    for user in data_info['users']:
        if user["user_id"] == user_id:
            # Takes the first user invoice
            invoice_dict = user['user_invoices'][0]
            break

    cID = "AUD"
    cbc = "cbc:"
    cac = "cac:"

    root = ET.Element("Invoice")

    # Section 3. LegalMonetaryTotal
    legal_monetary_total = ET.SubElement(root, f"{cac}LegalMonetaryTotal")
    ET.SubElement(legal_monetary_total, f"{cbc}LineExtensionAmount", currencyID=f"{cID}").text = f"{invoice_dict["lineExtensionAmount"]}"
    ET.SubElement(legal_monetary_total, f"{cbc}TaxExclusiveAmount", currencyID=f"{cID}").text = f"{invoice_dict["taxExclusiveAmount"]}"
    ET.SubElement(legal_monetary_total, f"{cbc}TaxInclusiveAmount", currencyID=f"{cID}").text = f"{invoice_dict["taxInclusiveAmount"]}"
    ET.SubElement(legal_monetary_total, f"{cbc}ChargeTotalAmount", currencyID=f"{cID}").text = f"{invoice_dict["chargeTotalAmount"]}"
    ET.SubElement(legal_monetary_total, f"{cbc}PayableAmount", currencyID=f"{cID}").text = f"{invoice_dict["payableAmount"]}"

    tree = ET.ElementTree(root)

    # print(ET.tostring(root))
    # Doesn't work but this function should indent the tree and make the tree more readable.
    #ET.indent(tree, space="\t", level=0)

    tree.write(f"{user_id}_e_invoice.xml")
