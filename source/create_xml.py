import xml.etree.ElementTree as ET
# https://docs.python.org/3.8/library/xml.etree.elementtree.html for more information

from source.database import data as database
from source.helpers_auth import check_valid_token, decode_token
from source.data_read_helper import decode_user_invoice

def create_invoice_v1(token):
    '''
    Creates an xml file containing the invoice information of a specific user found from (token).
    
    Arguments:
        token (string) : Username thats encrypted into JWT token

    Exceptions:
        - 

    Returns:
        {}
    
    '''
    data_info = database.get_data()

    # ----- Error handling -----
    # check whether the token is valid 
    check_valid_token(token)
    user_id = decode_token(token)

    # Finds the invoice data for a specific user_id
    invoice_dict = {}
    # Find the user
    for user in data_info['users']:
        if user["user_id"] == user_id:
            # Takes the first user invoice
            invoice_dict = user['user_invoice']
            break
    invoice_dict = decode_user_invoice(invoice_dict)
    
    cID = "AUD"
    cbc = "cbc:"
    cac = "cac:"

    root = ET.Element("Invoice")

    # Section 1. Invoice Type Code
    ET.SubElement(root, f"{cbc}InvoiceTypeCode").text = f"{invoice_dict['InvoiceTypeCode']}"

    # Section 2. Allowance Charge
    allowance_charge = ET.SubElement(root, f"{cac}AllowanceCharge")
    allowance_charge_dict = invoice_dict["AllowanceCharge"]
    ET.SubElement(allowance_charge, f"{cbc}ChargeIndicator").text = f"{allowance_charge_dict['ChargeIndicator']}"
    ET.SubElement(allowance_charge, f"{cbc}AllowanceChargeReason").text = f"{allowance_charge_dict['AllowanceChargeReason']}"
    ET.SubElement(allowance_charge, f"{cbc}Amount", currencyID=f"{cID}").text = f"{allowance_charge_dict['Amount']}"

    tax_category = ET.SubElement(allowance_charge, f"{cac}TaxCategory")
    tax_category_dict = invoice_dict["AllowanceCharge"]["TaxCategory"]
    ET.SubElement(tax_category, f"{cbc}ID").text = f"{tax_category_dict['ID']}"
    ET.SubElement(tax_category, f"{cbc}Percent").text =  f"{tax_category_dict['Percent']}"

    tax_scheme = ET.SubElement(tax_category, f"{cac}TaxScheme")
    tax_scheme_dict = invoice_dict["AllowanceCharge"]["TaxCategory"]["TaxScheme"]
    ET.SubElement(tax_scheme, f"{cbc}ID").text = f"{tax_scheme_dict['ID']}"

    # Section 3. LegalMonetaryTotal
    legal_monetary_total = ET.SubElement(root, f"{cac}LegalMonetaryTotal")
    legal_monetary_total_dict = invoice_dict["LegalMonetaryTotal"]
    for key, value in legal_monetary_total_dict.items():
        ET.SubElement(legal_monetary_total, f"{cbc}{key}", currencyID=f"{cID}").text = f"{value}"
        
    # Section 4 / 5. InvoiceLines.
    # Just repeates it twice for completeness.
    invoice_line_list = invoice_dict["InvoiceLine"]
    for invoice_line_dict in invoice_line_list:
        invoice_line = ET.SubElement(root, f"{cac}InvoiceLine")
        ET.SubElement(invoice_line, f"{cbc}ID").text = f"{invoice_line_dict['ID']}"
        ET.SubElement(invoice_line, f"{cbc}InvoiceQuantity", unitCode="DAY").text = f"{invoice_line_dict['InvoiceQuantity']}"
        ET.SubElement(invoice_line, f"{cbc}LineExtensionAmount", currencyID=f"{cID}").text =  f"{invoice_line_dict['LineExtensionAmount']}"

        price = ET.SubElement(invoice_line, f"{cac}Price")
        ET.SubElement(price, f"{cbc}PriceAmount", currencyID=f"{cID}").text = f"{invoice_line_dict['Price']['PriceAmount']}"

    tree = ET.ElementTree(root)

    # Indents the xml output and makes it more readable
    ET.indent(tree, space="\t", level=0)

    tree.write(f"{user_id}_e_invoice.xml")
    
    for user in data_info['users']:
        if user['user_id'] == user_id:
            user['xmlroot'] = root
    return {}
