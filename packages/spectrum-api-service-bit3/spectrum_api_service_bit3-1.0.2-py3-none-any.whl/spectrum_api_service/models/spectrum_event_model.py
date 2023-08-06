from datetime import datetime
from typing import Optional


class SpectrumEventModel:
    # ATTRIBUTES
    __id: str
    __created_by: str
    __creation_date_timestamp: int
    __event_description: str
    __event_type: str
    __severity: int
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
    def created_by(self) -> str:
        """
        Identificador del creador del evento sobre la alarma

        :return: Identificador del creador del evento sobre la alarma
        :rtype: str
        """
        return self.__created_by

    @created_by.setter
    def created_by(self, value: str):
        self.__created_by = value

    @property
    def event_description(self) -> str:
        """
        Descripción del evento

        :return: Descripción del evento
        :rtype: str
        """
        return self.__event_description

    @event_description.setter
    def event_description(self, value: str):
        self.__event_description = value

    @property
    def event_type(self) -> str:
        """
        Tipo de evento

        :return: Tipo de evento
        :rtype: str
        """
        return self.__event_type

    @event_type.setter
    def event_type(self, value: str):
        self.__event_type = value

    @property
    def creation_date_timestamp(self) -> int:
        """
        Fecha de creación del evento en timestamp

        :return: Fecha de creación del evento en timestamp
        :rtype: int
        """
        return self.__creation_date_timestamp

    @creation_date_timestamp.setter
    def creation_date_timestamp(self, value: int):
        self.__creation_date_timestamp = int(value)

    @property
    def severity(self) -> int:
        """
        Severidad del evento

        :return: Si el numero es menor a cero la severidad no existe, de lo contrario se califican de 1 a 3, donde
                3 es critical
        :rtype: int
        """
        return self.__severity

    @severity.setter
    def severity(self, value: int):
        if value == 'null':
            self.__severity = None
            return

        self.__severity = int(value)

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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_by": self.created_by,
            "event_description": self.event_description,
            "event_type": self.event_type,
            "creation_date_timestamp": self.creation_date_timestamp,
            "creation_date": self.creation_date.__str__(),
            "severity": self.severity,
            "landscape_name": self.landscape_name,
        }
