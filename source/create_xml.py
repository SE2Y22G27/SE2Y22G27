'''
    import the xml tree to convert all the data dictionary invoice information
    into xml formatted trees and converts it to string
'''

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

    cbc = "cbc:"
    cac = "cac:"

    name_space = {
        "xmlns" :
        "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
        "xmlns:cac" :
        "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        "xmlns:cbc" :
        "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        "xmlns:cec" :
        "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
    }



    root = ET.Element("Invoice", name_space)


    # Section 1. Invoice Type Code
    ET.SubElement(root, f"{cbc}UBLVersionID").text = "2.1"
    text_split_1 = "urn:cen.eu:en16931:2017#conformant#urn:fdc"
    text_split_2 = ":peppol.eu:2017:poacc:billing:international:aunz:3.0"
    ET.SubElement(root,
        f"{cbc}CustomizationID").text = text_split_1 + text_split_2
    ET.SubElement(root,
        f"{cbc}ProfileID").text = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
    ET.SubElement(root, f"{cbc}ID").text = invoice_dict['InvoiceID']
    ET.SubElement(root, f"{cbc}IssueDate").text = invoice_dict['IssueDate']
    ET.SubElement(root,
        f"{cbc}InvoiceTypeCode", listAgencyID="6",
        listID="UNCL1001").text = f"{invoice_dict['InvoiceTypeCode']}"
    ET.SubElement(root,f"{cbc}DocumentCurrencyCode",
    listAgencyID="6", listID="ISO4217" ).text = 'AUD'
    ET.SubElement(root, f"{cbc}BuyerReference").text = invoice_dict['InvoiceID']
    subroot = ET.SubElement(root, f"{cac}AdditionalDocumentReference")
    ET.SubElement(subroot, f"{cbc}ID").text = invoice_dict['InvoiceID'].lower()

    # Section 2. Supply Party
    subroot = ET.SubElement(root, f"{cac}AccountingSupplierParty")
    convert_supply_party(subroot,invoice_dict['AccountingSupplierParty'])

    # Section 3. customer Party
    subroot = ET.SubElement(root, f"{cac}AccountingCustomerParty")
    convert_customer_party(subroot,invoice_dict['AccountingCustomerParty'])

    # Section 4. payment means
    subroot = ET.SubElement(root, f"{cac}PaymentMeans")
    ET.SubElement(subroot, f"{cbc}PaymentMeansCode", listAgencyID="6",
    listID="UNCL4461").text = f"{invoice_dict['PaymentMeans']['PaymentMeansCode']}"
    ET.SubElement(subroot, f"{cbc}PaymentID").text = invoice_dict['InvoiceID']

    # Section 4. payment Terms
    subroot = ET.SubElement(root, f"{cac}PaymentTerms")
    ET.SubElement(subroot, f"{cbc}Note").text = invoice_dict['PaymentTerms']['Note']

    # Section 2. TaxTotal
    convert_taxtotal_xml(root,invoice_dict)

    # Section 3. LegalMonetaryTotal
    subroot = ET.SubElement(root, f"{cac}LegalMonetaryTotal")
    for key, value in invoice_dict["LegalMonetaryTotal"].items():
        ET.SubElement(subroot, f"{cbc}{key}", currencyID="AUD").text = f"{value}"



    # Section 4 / 5. InvoiceLines.
    convert_invoiceline_xml(root, invoice_dict)

    tree = ET.ElementTree(root)

    # Indents the xml output and makes it more readable
    ET.indent(tree, space="\t", level=0)

    for user in data_info['users']:
        if user['user_id'] == user_id:
            user['xmlroot']=ET.tostring(root,xml_declaration = True, encoding='utf8', method='xml')
    tree.write(f"{user_id}_invoice.xml", encoding='utf-8', xml_declaration=True)

    return {}

def convert_taxtotal_xml(root, invoice_dict):
    '''
        convert taxtotal information into xml document
    '''
    c_id = "AUD"
    cbc = "cbc:"
    cac = "cac:"
    scheme_agency_id = "6"
    scheme_id = "UNCL5305"
    taxtotal = ET.SubElement(root, f"{cac}TaxTotal")
    ET.SubElement(taxtotal,
    f"{cbc}TaxAmount",
        currencyID=f"{c_id}").text = f"{invoice_dict['TaxTotal']['TaxAmount']}"

    taxsubtotal = ET.SubElement(taxtotal, f"{cac}TaxSubtotal")
    sub_dict = invoice_dict['TaxTotal']['TaxSubtotal']
    ET.SubElement(taxsubtotal, f"{cbc}TaxableAmount",
        currencyID=f"{c_id}").text =  f"{sub_dict['TaxableAmount']}"
    ET.SubElement(taxsubtotal, f"{cbc}TaxAmount",
        currencyID=f"{c_id}").text =  f"{sub_dict['TaxAmount']}"
    tax_cat = ET.SubElement(taxsubtotal, f"{cac}TaxCategory")
    tax_dict = sub_dict['TaxCategory']
    ET.SubElement(tax_cat, f"{cbc}ID",
        schemeAgencyID=f"{scheme_agency_id}" , schemeID=f"{scheme_id}").text =  f"{tax_dict['ID']}"
    ET.SubElement(tax_cat, f"{cbc}Percent").text =  f"{tax_dict['Percent']}"
    taxscheme = ET.SubElement(tax_cat, f"{cac}TaxScheme")

    tax_scheme_dict = sub_dict['TaxCategory']["TaxScheme"]
    scheme_id = "UN/ECE 5153"
    ET.SubElement(taxscheme, f"{cbc}ID", schemeAgencyID=f"{scheme_agency_id}" ,
    schemeID=f"{scheme_id}").text = f"{tax_scheme_dict['ID']}"

def convert_invoiceline_xml(root, invoice_dict):
    '''
        convert invoiceline information into xml document
    '''
    c_id = "AUD"
    cbc = "cbc:"
    cac = "cac:"
    unit_code = "C62"
    unit_codelist_id = "UNECERec20"
    # Just repeates it twice for completeness.
    for invoice_line_dict in invoice_dict["InvoiceLine"]:
        invoice_line = ET.SubElement(root, f"{cac}InvoiceLine")
        ET.SubElement(invoice_line,
        f"{cbc}ID").text = f"{invoice_line_dict['ID']}"
        ET.SubElement(invoice_line,
        f"{cbc}InvoicedQuantity", unitCode=f"{unit_code}",
        unitCodeListID=f"{unit_codelist_id}").text = f"{invoice_line_dict['InvoicedQuantity']}"
        ET.SubElement(invoice_line, f"{cbc}LineExtensionAmount",
        currencyID=f"{c_id}").text =  f"{invoice_line_dict['LineExtensionAmount']}"
        item = ET.SubElement(invoice_line, f"{cac}Item")
        ET.SubElement(item,f"{cbc}Name").text = f"{invoice_line_dict['Item']['Name']}"
        classified_tax_category = ET.SubElement(item,f"{cac}ClassifiedTaxCategory")
        classified_tax_category_id = invoice_line_dict['Item']['ClassifiedTaxCategory']['ID']
        ET.SubElement(classified_tax_category,f"{cbc}ID",
            schemeAgencyID="6" ,
            schemeID="UNCL5305").text = f"{classified_tax_category_id}"
        ET.SubElement(classified_tax_category,
        f"{cbc}Percent").text = f"{invoice_line_dict['Item']['ClassifiedTaxCategory']['Percent']}"
        taxscheme = ET.SubElement(classified_tax_category,f"{cac}TaxScheme")
        taxscheme_id = invoice_line_dict['Item']['ClassifiedTaxCategory']['TaxScheme']['ID']
        ET.SubElement(taxscheme,f"{cbc}ID",schemeAgencyID="6" ,
            schemeID="UN/ECE 5153").text = f"{taxscheme_id}"
        price = ET.SubElement(invoice_line, f"{cac}Price")
        ET.SubElement(price, f"{cbc}PriceAmount",
        currencyID=f"{c_id}").text = f"{invoice_line_dict['Price']['PriceAmount']}"
        ET.SubElement(price, f"{cbc}BaseQuantity",
        unitCode=f"{unit_code}",
        unitCodeListID=f"{unit_codelist_id}").text = f"{invoice_line_dict['Price']['BaseQuantity']}"

def convert_supply_party(root,invoice_dict):
    '''
        convert invoiceline information into xml document
    '''
    cbc = "cbc:"
    cac = "cac:"
    list_agency_id = "6"
    list_id = "ISO3166-1:Alpha2"
    scheme_agency_id = "ZZZ"
    scheme_id = "0151"
    party_dict = invoice_dict['Party']
    supply_party = ET.SubElement(root, f"{cac}Party")
    party_identification = ET.SubElement(supply_party, f"{cac}PartyIdentification")
    ET.SubElement(party_identification, f"{cbc}ID", schemeAgencyID=f"{scheme_agency_id}" ,
        schemeID=f"{scheme_id}").text = f"{party_dict['PartyIdentification']['ID']}"

    name = ET.SubElement(supply_party, f"{cac}PartyName")
    ET.SubElement(name, f"{cbc}Name").text = party_dict['PartyName']['Name']

    address = ET.SubElement(supply_party, f"{cac}PostalAddress")
    ET.SubElement(address, f"{cbc}StreetName").text = party_dict['PostalAddress']['StreetName']
    if party_dict['PostalAddress']['AdditionalStreetName'] != {}:
        ET.SubElement(address,
        f"{cbc}AdditionalStreetName").text = party_dict['PostalAddress']['AdditionalStreetName']
    ET.SubElement(address, f"{cbc}CityName").text = party_dict['PostalAddress']['CityName']
    ET.SubElement(address, f"{cbc}PostalZone").text = f"{party_dict['PostalAddress']['PostalZone']}"
    country = ET.SubElement(address, f"{cac}Country")
    ET.SubElement(country, f"{cbc}IdentificationCode", listAgencyID=f"{list_agency_id}",
        listID= f"{list_id}").text = party_dict['PostalAddress']['Country']['IdentificationCode']

    party_entity = ET.SubElement(supply_party, f"{cac}PartyLegalEntity")
    ET.SubElement(party_entity,
    f"{cbc}RegistrationName").text = party_dict['PartyLegalEntity']['RegistrationName']
    ET.SubElement(party_entity, f"{cbc}CompanyID", schemeAgencyID=f"{scheme_agency_id}" ,
        schemeID=f"{scheme_id}").text = f"{party_dict['PartyLegalEntity']['CompanyID']}"

def convert_customer_party(root,invoice_dict):
    '''
        convert invoiceline information into xml document
    '''
    cbc = "cbc:"
    cac = "cac:"
    list_agency_id = "6"
    list_id = "ISO3166-1:Alpha2"
    party_dict = invoice_dict['Party']
    customer_party = ET.SubElement(root, f"{cac}Party")

    name = ET.SubElement(customer_party, f"{cac}PartyName")
    ET.SubElement(name, f"{cbc}Name").text = party_dict['PartyName']['Name']
    address = ET.SubElement(customer_party, f"{cac}PostalAddress")
    ET.SubElement(address, f"{cbc}StreetName").text = party_dict['PostalAddress']['StreetName']
    if party_dict['PostalAddress']['AdditionalStreetName'] != {}:
        ET.SubElement(address,
        f"{cbc}AdditionalStreetName").text = party_dict['PostalAddress']['AdditionalStreetName']
    ET.SubElement(address, f"{cbc}CityName").text = party_dict['PostalAddress']['CityName']
    ET.SubElement(address, f"{cbc}PostalZone").text = f"{party_dict['PostalAddress']['PostalZone']}"
    country = ET.SubElement(address, f"{cac}Country")
    ET.SubElement(country, f"{cbc}IdentificationCode", listAgencyID=f"{list_agency_id}",
    listID=f"{list_id}").text = party_dict['PostalAddress']['Country']['IdentificationCode']

    party_entity = ET.SubElement(customer_party, f"{cac}PartyLegalEntity")
    ET.SubElement(party_entity,
    f"{cbc}RegistrationName").text = party_dict['PartyLegalEntity']['RegistrationName']
