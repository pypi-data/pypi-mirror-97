import json
from datetime import datetime
from typing import Optional, List
from xml.etree import ElementTree

import requests
from log_helper import LogHelper
from requests import Response
from requests.auth import HTTPBasicAuth

from spectrum_api_service.helpers import convert_bytes_to_json, pretty_xml
from spectrum_api_service.constants import MODEL_HANDLE_ATTR, MODEL_NAME_ATTR, ALARM_TITLE_ATTR, \
    TROUBLE_TICKET_ID_ATTR, CREATION_DATE_ATTR, ALARM_MODIFIED_TIME_ATTR, CAUSE_CODE_ATTR, LANDSCAPE_NAME_ATTR, \
    CREATED_BY_ATTR, EVENT_ATTR, EVENT_TYPE_ATTR, SEVERITY_ATTR
from spectrum_api_service.models.host_spectrum_model import HostSpectrumModel
from spectrum_api_service.models import SpectrumAlarmModel
from spectrum_api_service.models import SpectrumEventModel


class SpectrumApiService(LogHelper):
    """
    Clase con las funcionalidades requeridas para interactuar con la api de SPECTRUM
    """

    def __init__(self, hostsSpectrum: List[HostSpectrumModel]):
        """
        Constructor

        :param hostsSpectrum: Datos del host de spectrum y sus respaldos si los tuviera
        :type hostsSpectrum: List[HostSpectrumModel]
        """

        super().__init__()
        if hostsSpectrum is None or hostsSpectrum.__len__() <= 0:
            raise Exception('Debe especificar los datos de o los hosts de spectrum a los que se le va consultar')

        self.hosts: List[HostSpectrumModel] = hostsSpectrum
        self.__current_host: HostSpectrumModel = hostsSpectrum[0]
        self.__response_type_json = False

    def get_alarms(self, attr: list = None, last_hours: int = 0, items_per_page: int = 100000) \
            -> List[SpectrumAlarmModel]:
        """
        Obtiene las alarmas activas en SPECTRUM, ya sea la totalidad o las presentadas en un lapso de tiempo

        :param attr: Atributos que se desean obtener de cada alarma
        :type attr: list
        :param last_hours: Se usa para indicar las alarmas mas que se desean obtener en un determinado numero de horas
        a partir de la hora actual hacia atrás
        :type last_hours: int
        :param items_per_page: Cantidad de alarmas que se desean obtener por consulta
        :type items_per_page: int
        :return: La cantidad de alarmas encontradas, si no existen, se retorna None
        :rtype: list
        """

        response: list[SpectrumAlarmModel] = []
        data: list

        if last_hours > 0:
            data = self.__get_all_alarms_in_last_hours(last_hours, attr, items_per_page)
        else:
            data = self.__get_all_alarms(attr, items_per_page)

        if data is None or data.__len__() == 0:
            return response

        # self.logger.debug(json.dumps(data, indent=4, sort_keys=False))
        response = self.__map_to_spectrum_alarm_model(data)
        return response

    def get_events(self, model_handle: list, start_time: datetime, end_time: datetime, attrs: list) \
            -> Optional[List[SpectrumEventModel]]:
        """
        Obtiene los eventos en SPECTRUM en un intervalo de tiempo determinado

        :param model_handle: Lista de Model handle de los que se desea obtener los eventos
        :type model_handle: list
        :param start_time: Fecha inicial del intervalo de búsqueda
        :type start_time: datetime
        :param end_time: Fecha final del intervalo de búsqueda
        :type end_time: datetime
        :param attrs: Atributos que se desean obtener de los eventos
        :type attrs: list
        :return: La cantidad de eventos encontrados, si no existen, se retorna None
        :rtype: list
        """

        action = 'events/getEvents'
        start_timestamp: float = start_time.timestamp().__round__() * 1000
        end_timestamp: float = end_time.timestamp().__round__() * 1000

        count: int = 0
        landscape: str = self.__current_host.landscape[count]
        response: List[SpectrumEventModel] = []

        while landscape is not None:
            self.debug(f'Se inicia el proceso para obtener los eventos del model handle {model_handle} en el '
                       f'landscape [{landscape}] presentados entre '
                       f'{start_time.strftime("%d/%m/%Y %H:%M:%S")} y '
                       f'{end_time.strftime("%d/%m/%Y %H:%M:%S")}')

            # Construyo el request en xml que se va a enviar a spectrum
            payload: ElementTree.ElementTree = \
                self.__build_payload_xml_get_events(model_handle, start_timestamp, end_timestamp, attrs, landscape)

            # Obtengo el root del elemento xml
            root = payload.getroot()

            # Convierto el xml en string para ser enviado a spectrum
            data_xml: bytes = ElementTree.tostring(root, encoding='utf8', method='xml')

            # Este header indica al servidor que retorne la respuesta en formato json
            headers = {
                'Content-Type': 'application/xml',
                'Accept': 'application/json'
            }

            self.debug(f"Se solicitan los eventos a SPECTRUM:\n{pretty_xml(data_xml)}")
            # Hago la solicitud a la API de SPECTRUM
            response: Response = self.__query(action=action, method='post', headers=headers, data_xml=data_xml)
            response_json: dict = convert_bytes_to_json(response.content)
            self.debug(response_json)

            events: list = self.__process_response_get_events_action(response)
            count += 1

            if events is None:
                self.debug(f'No existen datos del model handle {model_handle} en el landscape [{landscape}]')
                if count < self.__current_host.landscape.__len__():
                    landscape = self.__current_host.landscape[count]
                else:
                    landscape = None
                    response = None
            else:
                response = self.__map_to_spectrum_event_model(events)
                landscape = None

        return response

    def update_alarm(self, alarm_id: str, attributes: list, values: list) -> bool:
        """
        Actualiza los atributos especificados de una alarma en específico

        :param alarm_id: Identificador de la a alarma
        :type alarm_id: int
        :param attributes: Lista de atributos que se desean actualizar de la alarma
        :type attributes: list
        :param values: Valores de los atributos que se van actualizar
        :type values: list
        :return: Lista con la respuesta dada por la API
        :rtype bool
        """

        action = f'alarms/{alarm_id}?'
        if attributes.__len__() != values.__len__():
            self.error('La cantidad de valores no concuerda con la cantidad de atributos que se desean actualizar')
            return False

        counter: int = 0
        for value in attributes:
            action += f'attr={value}&val={values[counter]}'
            counter += 1

            # Si existen más atributos por especificar agrego el & al final para garantizar que el endpoint esté
            # bien construido
            if counter < attributes.__len__():
                action += '&'

        self.debug(f'Se inicia el proceso para actualizar la alarma con id [{alarm_id}]')
        response: Response = self.__query(action=action, method='put')
        return self.__process_response_update_alarms_action(response)

    def add_event(self, model: str, event_type: str, data: dict) -> bool:
        """
        Registra un evento en spectrum

        :param model: Identificador del modelo en el que se va a registrar el evento
        :type model: str
        :param event_type: Identificador de tipo de evento
        :type event_type: str
        :param data: Datos que se van a registrar en spectrum
        :type data: dict
        :return: Verdadero si el evento se registro correctamente en SPECTRUM
        :rtype: bool
        """

        self.debug('Se inicia el proceso que permite agregar eventos a SPECTRUM')
        # Construyo la url de la acción que se va a usar de la API de SPECTRUM
        action = "events"
        # Convierto los datos que se desean registrar en elementos xml
        payload: ElementTree.ElementTree = self.__build_payload_xml_add_event(model, event_type, data)
        # Obtengo el root del elemento xml
        root = payload.getroot()
        # Convierto el xml en string para ser enviado a spectrum
        data_xml: bytes = ElementTree.tostring(root, encoding='utf8', method='xml')

        headers = {'Content-Type': 'application/xml'}
        self.debug(f"Se envían los datos a SPECTRUM:\n{pretty_xml(data_xml)}")
        response: Response = self.__query(action=action, method='post', headers=headers, data_xml=data_xml)

        return self.__is_success_response(response, response_type_json=self.__response_type_json)

    def __get_all_alarms(self, attr: list = None, items_per_page: int = 100000) -> Optional[list]:
        """
        Obtiene todas las alarmas presentadas en SPECTRUM

        :param attr: Atributos que se desean obtener de cada alarma
        :type attr: dict
        :param items_per_page: Cantidad de alarmas que se desean obtener por consulta
        :type items_per_page: int
        :return: La cantidad de alarmas encontradas, si no existen, se retorna None
        :rtype: dict
        """

        action = f"alarms?symptoms=yes&throttlesize={items_per_page}"
        self.debug('Se inicia el proceso para obtener todas las alarmas')

        # Agrego los atributos que se desean obtener a la url
        if attr is not None:
            for value in attr:
                action += f'&attr={value}'

        response: Response = self.__query(action=action, method='get')
        return self.__process_response_get_alarms_action(response)

    def __get_all_alarms_in_last_hours(self, last_hours: int = 1, attr: list = None, items_per_page: int = 100000) \
            -> Optional[list]:
        """
        Obtiene todas las alarmas activas en SPECTRUM en un lapso de tiempo determinado

        :param last_hours: Se usa para indicar las alarmas mas que se desean obtener en un determinado numero de horas
        a partir de la hora actual hacia atrás
        :type last_hours: int
        :param attr: Atributos que se desean obtener de cada alarma
        :type attr: list
        :param items_per_page: Cantidad de alarmas que se desean obtener por consulta
        :type items_per_page: int
        :return: La cantidad de alarmas encontradas, si no existen, se retorna None
        :rtype: dict
        """

        action = f"alarms?lasthour={last_hours}"
        self.debug(f'Se inicia el proceso para obtener las alarmas presentadas en las ultimas {last_hours} horas')

        # Construyo el request en xml que se va a enviar a spectrum
        payload: ElementTree.ElementTree = self.__build_payload_xml_get_alarms(attr, items_per_page)
        # Obtengo el root del elemento xml
        root = payload.getroot()
        # Convierto el xml en string para ser enviado a spectrum
        data_xml: bytes = ElementTree.tostring(root)

        # Este header indica al servidor que retorne la respuesta en formato json
        headers: dict = {
            'Content-Type': 'application/xml',
            'Accept': 'application/json'
        }

        self.debug(f"Se solicitan las alarmas a SPECTRUM:\n{pretty_xml(data_xml)}")
        # Hago la solicitud a la API de SPECTRUM
        response: Response = self.__query(action=action, method='post', headers=headers, data_xml=data_xml)

        return self.__process_response_get_alarms_action(response)

    def __query(self, action: str, method: str, headers: dict = None, data_xml: bytes = None) -> Optional[Response]:
        """
        Realiza una consulta a la API de spectrum

        :param action: Acción de la API que se va a ejecutar
        :type action: str
        :param method: Método que debe usarse para realizar la consulta a la API POST, GET, PUT, DELETE
        :type method: str
        :param headers: Cabeceras del request
        :type headers: dict
        :param data_xml: Body de la consulta
        :type data_xml: bytes
        :return: La respuesta de la API
        :rtype: Optional[Response]
        """

        if headers is None:
            headers = {'Accept': 'application/json'}

        self.__response_type_json = False
        if headers.get('Accept') is not None and headers.get('Accept') == 'application/json':
            self.__response_type_json = True

        response: Response = None
        host_counter: int = 0
        next_host: bool = True

        while next_host:
            try:
                # Actualizo el host de consulta al que está respondiendo para evitar las consultas a los hosts
                # que no responden
                self.__current_host = self.hosts[host_counter]

                url: str = \
                    f'{self.hosts[host_counter].http_protocol}://{self.hosts[host_counter].host}:' \
                    f'{self.hosts[host_counter].port}/spectrum/restful/{action}'

                auth: HTTPBasicAuth = \
                    HTTPBasicAuth(self.hosts[host_counter].user, self.hosts[host_counter].password)

                self.debug(f'Se consume la API: {url}')
                method = method.lower()
                if method == 'post':
                    response = requests.post(url=url, auth=auth, headers=headers, data=data_xml)
                elif method == 'get':
                    response = requests.get(url=url, auth=auth, headers=headers)
                elif method == 'put':
                    response = requests.put(url=url, auth=auth, headers=headers)

                next_host = False
                return response
            except requests.exceptions.RequestException as ex:
                self.error(str(ex))
                host_counter += 1
                if host_counter >= self.hosts.__len__():
                    next_host = False
                    self.error('Se realizó la consulta a todos los host especificados y todos arrojan '
                               'error al realizar la consulta')

    def __process_response_update_alarms_action(self, response: Response) -> bool:
        """
        Procesa las respuestas de la acción alarm-update que permite actualizar las alarmas

        :param response: Respuesta obtenida del servidor después de consultar las alarmas
        :type response: Response
        :return: La cantidad de alarmas encontradas, si no existen, se retorna None
        :rtype: dict
        """

        updated: bool = False
        if response is None:
            self.debug("La respuesta de la API es nula")
            return updated

        # Si la respuesta es válida, retorno el resultado en formato JSON.
        # Sino, imprimo el error y retorno un None
        if response.status_code == 200:
            response_json: dict = convert_bytes_to_json(response.content)
            data: dict = response_json.get('alarm-update-response-list')
            response: dict = data.get('alarm-responses').get('alarm')
            updated = response.get('@error') == 'Success'

            if not updated:
                self.error(f'Se presentó un error realizando la actualización')
                self.debug(response)

            return updated

        self.error(f'Consultando la API de SPECTRUM: {response.status_code}')
        return updated

    def __process_response_get_alarms_action(self, response: Response) -> Optional[list]:
        """
        Procesa las respuestas de la acción get_alarms en sus variadas presentaciones

        :param response: Respuesta obtenida del servidor después de consultar las alarmas
        :type response: Response
        :return: La cantidad de alarmas encontradas, si no existen, se retorna None
        :rtype: dict
        """

        if response is None:
            self.error("La respuesta de la API es nula")
            return None

        # Si la respuesta es válida, retorno el resultado en formato JSON.
        # Sino, imprimo el error y retorno un None
        if response.status_code == 200:
            response_json: dict = convert_bytes_to_json(response.content)
            data: dict = response_json.get('alarm-response-list')
            total_alarms: int = data.get('@total-alarms')

            if total_alarms == 0:
                self.info('No existen alarmas activas en SPECTRUM')
                return None

            alarm_response: dict = data.get('alarm-responses')
            alarms: list = alarm_response.get('alarm')

            # self.info(f'Existen {total_alarms} alarmas activas en SPECTRUM')
            # self.debug(json.dumps(alarms, indent=4))

            return alarms

        self.error(f'Consultando la API de SPECTRUM: {response.status_code}')
        return None

    def __process_response_get_events_action(self, response: Response) -> Optional[list]:
        """
        Procesa las respuestas de la acción get_events en sus variadas presentaciones

        :param response: Respuesta obtenida del servidor después de consultar los eventos
        :type response: Response
        :return: La cantidad de eventos encontradas, si no existen, se retorna None
        :rtype: dict
        """

        if response is None:
            self.error("La respuesta de la API es nula")
            return None

        # Si la respuesta es válida, retorno el resultado en formato JSON.
        # Sino, imprimo el error y retorno un None
        if response.status_code == 200:
            response_json: dict = convert_bytes_to_json(response.content)
            data: dict = response_json.get('get-event-response-list')
            total_events: int = data.get('@total-events')

            self.debug(f'TOTAL EVENTOS: {total_events}')
            if total_events == 0:
                error_message: str = data.get('@error-message')
                if error_message is not None and error_message.__len__() > 0:
                    self.warning(f'Mensaje de error en el response: {error_message}')

                return None

            events_response: dict = data.get('get-event-responses')
            events: list = events_response.get('event')

            return events

        self.error(f'Consultando la API de SPECTRUM: {response.status_code}')
        return None

    def __build_payload_xml_add_event(self, model: str, event_type: str, data: dict, items_per_page: int = 100000) \
            -> ElementTree.ElementTree:
        """
        Construye el xml requerido para registrar eventos en SPECTRUM

        :param model: Identificador del modelo en el que se va a registrar el evento
        :type model: str
        :param event_type: Identificador de tipo de evento
        :type event_type: str
        :param data: Datos que se van a registrar en spectrum
        :type data: dict
        :return: Objeto con la estructura xml requerida para registrar eventos en SPECTRUM
        :rtype: ElementTree.ElementTree
        """

        self.debug("Se inicia el proceso de construcción del XML para SPECTRUM")
        # Especifico el root o raíz del documento xml a construir
        root: ElementTree.Element = ElementTree.Element('rs:event-request', {
            'throttlesize': items_per_page,
            'xmlns:rs': 'http://www.ca.com/spectrum/restful/schema/request'
        })
        # Agrego el elemento event
        event: ElementTree.Element = ElementTree.SubElement(root, 'rs:event')
        # Agrego el elemento target_model al evento anterior
        target_model: ElementTree.Element = ElementTree.SubElement(event, 'rs:target-models')
        # Agrego el elemento model al target_model con sus respectivos datos
        ElementTree.SubElement(target_model, 'rs:model', {'mh': model})
        # Agrego el elemento event-type al event con sus respectivos datos
        ElementTree.SubElement(event, 'rs:event-type', {'id': event_type})

        # Registro los varbind acorde a lo enviado por parámetro
        for key, value in data.items():
            ElementTree.SubElement(event, 'rs:varbind', {'id': key}).text = value

        # retorno el xml construido
        return ElementTree.ElementTree(root)

    def __build_payload_xml_get_alarms(self, attr: list, items_per_page: int = 100000) -> ElementTree.ElementTree:
        """
        Construye el xml requerido para obtener las alarmas activas de SPECTRUM en un determinado lapso de tiempo

        :param attr: Atributos que se desean obtener de cada alarma
        :type attr: list
        :param items_per_page: Cantidad de alarmas que se desean obtener por consulta
        :type items_per_page: int
        :return: Objeto con la estructura xml requerida para registrar eventos en SPECTRUM
        :rtype: ElementTree.ElementTree
        """

        self.debug("Se inicia el proceso de construcción del XML para SPECTRUM")
        # Especifico el root o raíz del documento xml a construir
        root = ElementTree.Element('rs:alarm-request', {
            'throttlesize': items_per_page.__str__(),
            'xmlns:rs': 'http://www.ca.com/spectrum/restful/schema/request',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.ca.com/spectrum/restful/schema/request../../../xsd/Request.xsd'
        })
        # Agrego los atributos que se desean obtener de las alarmas
        for attribute in attr:
            ElementTree.SubElement(root, 'rs:requested-attribute', {'id': attribute})

        # retorno el xml construido
        return ElementTree.ElementTree(root)

    def __build_payload_xml_get_events(self, model_handle: list, start_date: float, end_date: float, attrs: list,
                                       landscape: str, items_per_page: int = 100000) -> ElementTree.ElementTree:
        """
        Construye el xml requerido para obtener los eventos de SPECTRUM asociados a uno o varios model handle en un
        determinado intervalo de tiempo

        :param model_handle: Lista de Model handle de los que se desea obtener los eventos
        :type model_handle: list
        :param start_date: Fecha inicial en timestamp en milisegundos de la búsqueda
        :type start_date: float
        :param end_date: Fecha final en timestamp en milisegundos de la búsqueda
        :type end_date: float
        :param attrs: Atributos que se desean obtener de los eventos
        :type attrs: list
        :param landscape: Landscape donde se debe buscar los model handle
        :type landscape: str
        :param items_per_page: Cantidad de eventos que se desean obtener por consulta
        :type items_per_page: int
        :return: Objeto con la estructura xml requerida para registrar eventos en SPECTRUM
        :rtype: ElementTree.ElementTree
        """

        self.debug("Se inicia el proceso de construcción del XML para SPECTRUM")
        # Especifico el root o raíz del documento xml a construir
        root: ElementTree.Element = ElementTree.Element('rs:get-event-request', {
            'throttlesize': items_per_page.__str__(),
            'xmlns:rs': 'http://www.ca.com/spectrum/restful/schema/request',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:schemaLocation': 'http://www.ca.com/spectrum/restful/schema/request../../../xsd/Request.xsd'
        })

        # Agrego los filtros de búsqueda inicial
        ElementTree.SubElement(root, 'rs:get-events-filter', {
            'start-time': start_date.__str__(),
            'end-time': end_date.__str__(),
            'subcomponents-events': 'true',
            'exclude-events': '0x10005,0x10219,0x10706'
        })

        # Agrego los atributos que se desean obtener de los eventos
        for attribute in attrs:
            ElementTree.SubElement(root, 'rs:requested-attribute', {'id': f'{attribute}'})

        # Especifico los model handel de los que deseo obtener los eventos
        models: ElementTree.Element = ElementTree.SubElement(root, 'rs:target-models')
        for mh in model_handle:
            ElementTree.SubElement(models, 'rs:model', {'mh': f'{mh}'})

        ElementTree.SubElement(root, 'rs:landscape', {'id': f'{landscape}'})

        # retorno el xml construido
        return ElementTree.ElementTree(root)

    @staticmethod
    def __map_to_spectrum_alarm_model(data: list) -> List[SpectrumAlarmModel]:
        response: List[SpectrumAlarmModel] = []
        for item in data:
            attributes: list = item.get('attribute')

            alarm = SpectrumAlarmModel()
            alarm.id = item.get('@id')
            alarm.model_handle = SpectrumApiService.__get_data_by_attribute_id(attributes, MODEL_HANDLE_ATTR)
            alarm.model_name = SpectrumApiService.__get_data_by_attribute_id(attributes, MODEL_NAME_ATTR)
            alarm.title = SpectrumApiService.__get_data_by_attribute_id(attributes, ALARM_TITLE_ATTR)
            alarm.trouble_ticket_id = SpectrumApiService.__get_data_by_attribute_id(attributes, TROUBLE_TICKET_ID_ATTR)
            alarm.creation_date_timestamp = SpectrumApiService.__get_data_by_attribute_id(attributes,
                                                                                          CREATION_DATE_ATTR)
            alarm.last_modified_date_timestamp = \
                SpectrumApiService.__get_data_by_attribute_id(attributes, ALARM_MODIFIED_TIME_ATTR)
            alarm.cause_code = SpectrumApiService.__get_data_by_attribute_id(attributes, CAUSE_CODE_ATTR)
            alarm.landscape_name = SpectrumApiService.__get_data_by_attribute_id(attributes, LANDSCAPE_NAME_ATTR)

            response.append(alarm)

        return response

    @staticmethod
    def __map_to_spectrum_event_model(data: list) -> List[SpectrumEventModel]:
        response: List[SpectrumEventModel] = []
        for item in data:
            attributes: list = item.get('attribute')

            event = SpectrumEventModel()
            event.id = item.get('@id')
            event.created_by = SpectrumApiService.__get_data_by_attribute_id(attributes, CREATED_BY_ATTR)
            event.event_description = SpectrumApiService.__get_data_by_attribute_id(attributes, EVENT_ATTR)
            event.event_type = SpectrumApiService.__get_data_by_attribute_id(attributes, EVENT_TYPE_ATTR)
            event.creation_date_timestamp = SpectrumApiService.__get_data_by_attribute_id(attributes,
                                                                                          CREATION_DATE_ATTR)
            event.severity = SpectrumApiService.__get_data_by_attribute_id(attributes, SEVERITY_ATTR)
            event.landscape_name = SpectrumApiService.__get_data_by_attribute_id(attributes, LANDSCAPE_NAME_ATTR)

            response.append(event)

        return response

    @staticmethod
    def __get_data_by_attribute_id(attributes: list, attribute_id: str) -> Optional[str]:
        data = next((x for x in attributes if x.get('@id') == attribute_id), None)
        if data is None:
            return data

        return data.get('$')

    @staticmethod
    def __is_success_response(response: Response, response_type_json: bool = False) -> bool:
        """
        Valida que la respuesta de la API de spectrum sea exitosa

        :return: Verdadero si la respuesta específica es success
        :rtype: bool
        """

        error_data: str = ''
        if response.status_code == 200:
            if response_type_json is False:
                content_response: ElementTree.Element = ElementTree.fromstring(response.content)
                for node in content_response.iter():
                    if node.attrib.__len__() > 0:
                        error_data = node.attrib['error']
            else:
                json_data = response.content.decode('utf8').replace("\\", '')
                print(json_data)
                data: dict = json.loads(json_data)
                # TODO: CORREGIR YA QUE NO TODOS TIENEN EL MISMO NODO INICIAL Y BUSCAR EL VALOR @error-message
                error_data: str = data.get('alarm-response-list').get('@error')

        return error_data == 'Success' or error_data == 'EndOfResults'
