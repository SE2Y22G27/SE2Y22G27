import xml.etree.ElementTree as ET

# https://docs.python.org/3.8/library/xml.etree.elementtree.html
# contains all the library functions

value = 10
cID = "AUD"
code = 380
root = ET.Element("Invoice")

cbc = "cbc:"
cac = "cac:"

# Section 1. Invoice Type Code
ET.SubElement(root, f"{cbc}InvoiceTypeCode").text = f"{code}"

# Section 2. Allowance Charge
allowance_charge = ET.SubElement(root, f"{cac}AllowanceCharge")
ET.SubElement(allowance_charge, f"{cbc}ChargeIndicator").text = "true"
ET.SubElement(allowance_charge, f"{cbc}AllowanceChargeReason").text = "Insurance"
ET.SubElement(allowance_charge, f"{cbc}Amount", currencyID=f"{cID}").text = "-25"

tax_category = ET.SubElement(allowance_charge, f"{cac}TaxCategory")
ET.SubElement(tax_category, f"{cbc}ID").text = "S"
ET.SubElement(tax_category, f"{cbc}Percent").text = "25.0"

tax_scheme = ET.SubElement(tax_category, f"{cac}TaxScheme")
ET.SubElement(tax_scheme, f"{cbc}ID").text = "VAT"


# Section 3. LegalMonetaryTotal
legal_monetary_total = ET.SubElement(root, f"{cac}LegalMonetaryTotal")
ET.SubElement(legal_monetary_total, f"{cbc}LineExtensionAmount", currencyID=f"{cID}").text = f"{value}"
ET.SubElement(legal_monetary_total, f"{cbc}TaxExclusiveAmount", currencyID=f"{cID}").text = f"{value}"
ET.SubElement(legal_monetary_total, f"{cbc}TaxInclusiveAmount", currencyID=f"{cID}").text = f"{value}"
ET.SubElement(legal_monetary_total, f"{cbc}PayableRoundingAmount", currencyID=f"{cID}").text = f"{value}"
ET.SubElement(legal_monetary_total, f"{cbc}PayableAmount", currencyID=f"{cID}").text = f"{value}"

# Section 4 / 5. InvoiceLines.
# Just repeates it twice for completeness.
for i in range(2):
    invoice_line = ET.SubElement(root, f"{cac}InvoiceLine")
    ET.SubElement(invoice_line, f"{cbc}ID").text = f"{i}"
    ET.SubElement(invoice_line, f"{cbc}InvoicedQuantity", unitCode="DAY").text = "-7"
    ET.SubElement(invoice_line, f"{cbc}LineExtensionAmount", currencyID=f"{cID}").text = "-2800"

    price = ET.SubElement(invoice_line, f"{cac}Price")
    ET.SubElement(price, f"{cbc}PriceAmount", currencyID=f"{cID}").text = 400



print(ET.tostring(root))

tree = ET.ElementTree(root)

# Doesn't work but this function should indent the tree and make the tree more readable.
#ET.indent(tree, space="\t", level=0)

tree.write("filename.xml")
