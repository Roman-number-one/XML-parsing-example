from xml.etree import ElementTree

from xml_source import PurchaseResponsibleBuilder


NAMESPACES = {
    'default': 'http://zakupki.gov.ru/oos/types/1',
    'ns2': 'http://zakupki.gov.ru/oos/export/1',
}


if __name__ == '__main__':
    root_element = ElementTree.parse('test.xml').getroot()
    purchase_responsible_root = root_element.find(
        'ns2:fcsNotificationEF/default:purchaseResponsible',
        namespaces=NAMESPACES,
    )
    purchase_responsible_builder = PurchaseResponsibleBuilder(namespaces=NAMESPACES)
    purchase_responsible = purchase_responsible_builder.build(purchase_responsible_root)
    print(purchase_responsible)
