from lxml import etree


def pretty_xml(data: bytes) -> str:
    """
    Formatea los datos xml de un objeto de este tipo

    :param data: Datos que se desean formatear
    :type data: bytearray
    :return: Datos formateados
    :rtype: str
    """

    if data is None:
        return ''

    xml = etree.fromstring(data)
    response = etree.tostring(xml, pretty_print=True).decode()

    return response
