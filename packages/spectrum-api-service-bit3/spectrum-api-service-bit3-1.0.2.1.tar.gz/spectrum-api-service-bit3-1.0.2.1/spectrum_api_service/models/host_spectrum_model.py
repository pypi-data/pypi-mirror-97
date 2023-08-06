from typing import List

from spectrum_api_service.models.host_model import HostModel


class HostSpectrumModel(HostModel):
    """
    Modelo con las propiedades requeridas para describir un host de SPECTRUM
    """

    # ATTRIBUTES
    __user: str
    __pass: str
    __landscape: List[str]

    def __init__(self):
        super().__init__()
        self.__landscape = ['0x1000000']

    @property
    def user(self) -> str:
        return self.__user

    @user.setter
    def user(self, value: str):
        self.__user = value

    @property
    def password(self) -> str:
        return self.__pass

    @password.setter
    def password(self, value: str):
        self.__pass = value

    @property
    def landscape(self) -> List[str]:
        return self.__landscape

    @landscape.setter
    def landscape(self, value: List[str]):
        self.__landscape = value

    def to_dict(self) -> dict:
        return {
            "host": self.host
            , "port": self.port
            , "http_protocol": self.http_protocol
            , "user": self.user
            , "password": self.password
            , "landscape": self.landscape
        }
