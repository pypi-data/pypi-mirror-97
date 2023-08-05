from pika import PlainCredentials, ConnectionParameters


class RabbitConfig:

    def __init__(self,
                 host: str,
                 port: int,
                 exchange: str,
                 credentials: PlainCredentials) -> None:
        self.host = host
        self.port = port
        self.exchange: str = exchange
        self.credentials = credentials
        self.params = ConnectionParameters(host, port, '/', self.credentials)

    @staticmethod
    def from_dict(dictionary: dict[str, any]) -> 'RabbitConfig':
        host = dictionary['host']
        port = int(dictionary['port'])
        exchange = dictionary['exchange']
        credentials = PlainCredentials(dictionary['user'], dictionary['pass'])
        return RabbitConfig(host, port, exchange, credentials)
