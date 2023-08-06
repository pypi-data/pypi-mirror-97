class HostModel:
    """
    Modelo con las propiedades requeridas para describir un host
    """

    # ATTRIBUTES
    __host: str
    __port: int
    __http_protocol: str

    def __init__(self):
        self.__http_protocol = 'https'
        self.__port = 443

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, value: str):
        self.__host = value

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, value: int):
        self.__port = value

    @property
    def http_protocol(self) -> str:
        return self.__http_protocol

    @http_protocol.setter
    def http_protocol(self, value: str):
        self.__http_protocol = value

    @property
    def url(self) -> str:
        return f'{self.http_protocol}://{self.host}:{self.http_protocol}'

    def to_dict(self) -> dict:
        return {
            "host": self.host
            , "port": self.port
            , "http_protocol": self.http_protocol
            , "url": self.url
        }
