import json


def convert_bytes_to_json(data: bytes) -> dict:
    """
    Transforma una respuesta json que esta como bytes a json

    :param data: Datos que se desean transformar
    :type data: bytes
    :return: Los datos en formato json
    :rtype: dict
    """

    data_json = data.decode('utf8').replace("'", ' ')
    response_json: dict = json.loads(data_json)

    return response_json
