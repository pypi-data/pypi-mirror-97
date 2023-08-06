
class ClientException(Exception):
    pass


class QueueNotCached(ClientException):
    pass


class ExchangeNotCached(ClientException):
    pass


class ConsumerNotCached(ClientException):
    pass


class Timeout(ClientException):
    def __init__(self, timeout):
        self.timeout = timeout

    def __str__(self):
        return "An AMQP timeout occured after {} seconds".format(self.timeout)
