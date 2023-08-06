from datetime import datetime
from typing import Optional


class SpectrumAlarmModel:
    # ATTRIBUTES
    __id: str
    __model_handle: str
    __model_name: str
    __title: str
    __trouble_ticket_id: str
    __creation_date_timestamp: int
    __last_modified_date_timestamp: int
    __cause_code: int
    __landscape_name: str

    @property
    def id(self) -> str:
        """
        Identificador principal de la alarma

        :return: Identificador principal de la alarma
        :rtype: str
        """
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = value

    @property
    def model_handle(self) -> str:
        """
        Model handle al que pertenece la alarma

        :return: Model handle al que pertenece la alarma
        :rtype: str
        """
        return self.__model_handle

    @model_handle.setter
    def model_handle(self, value: str):
        self.__model_handle = value

    @property
    def model_name(self) -> str:
        """
        Model name del model handle al que pertenece la alarma

        :return: Model name del model handle al que pertenece la alarma
        :rtype: str
        """
        return self.__model_name

    @model_name.setter
    def model_name(self, value: str):
        self.__model_name = value

    @property
    def title(self) -> str:
        """
        Título de la alarma

        :return: Título de la alarma
        :rtype: str
        """
        return self.__title

    @title.setter
    def title(self, value: str):
        self.__title = value

    @property
    def trouble_ticket_id(self) -> str:
        """
        Trouble ticket id de la alarma

        :return: Trouble ticket id de la alarma
        :rtype: str
        """
        return self.__trouble_ticket_id

    @trouble_ticket_id.setter
    def trouble_ticket_id(self, value: str):
        self.__trouble_ticket_id = value

    @property
    def creation_date_timestamp(self) -> int:
        """
        Fecha de creación de la alerta en timestamp

        :return: Fecha de creación de la alerta en timestamp
        :rtype: int
        """
        return self.__creation_date_timestamp

    @creation_date_timestamp.setter
    def creation_date_timestamp(self, value: int):
        self.__creation_date_timestamp = int(value)

    @property
    def last_modified_date_timestamp(self) -> int:
        """
        Fecha de la última modificación de la alerta en timestamp

        :return: Fecha de la última modificación de la alerta en timestamp
        :rtype: int
        """
        return self.__last_modified_date_timestamp

    @last_modified_date_timestamp.setter
    def last_modified_date_timestamp(self, value: int):
        self.__last_modified_date_timestamp = int(value)

    @property
    def cause_code(self) -> int:
        """
        Cause Code

        :return: Cause code
        :rtype: int
        """
        return self.__cause_code

    @cause_code.setter
    def cause_code(self, value: int):
        self.__cause_code = int(value)

    @property
    def landscape_name(self) -> str:
        """
        Nombre del landscape o host al que pertenece la alarma

        :return: Trouble ticket id de la alarma
        :rtype: str
        """
        return self.__landscape_name

    @landscape_name.setter
    def landscape_name(self, value: str):
        self.__landscape_name = value

    @property
    def creation_date(self) -> Optional[datetime]:
        """
        Fecha de creación de la alarma

        :return: Fecha de creación de la alarma
        :rtype: Optional[datetime, None]
        """

        if self.__creation_date_timestamp:
            return datetime.fromtimestamp(self.__creation_date_timestamp)

        return None

    @property
    def event_id(self) -> Optional[str]:
        """
        Event id, para obtener este la propiedad CauseCode debe estar con algún valor

        :return: Event id
        :rtype: Optional[str, None]
        """

        if self.__cause_code:
            return hex(self.__cause_code)

        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "model_handle": self.model_handle,
            "model_name": self.model_name,
            "title": self.title,
            "trouble_ticket_id": self.trouble_ticket_id,
            "creation_date_timestamp": self.creation_date_timestamp,
            "last_modified_date_timestamp": self.last_modified_date_timestamp.__str__(),
            "creation_date": self.creation_date.__str__(),
            "cause_code": self.cause_code,
            "landscape_name": self.landscape_name,
            "event_id": self.event_id
        }
