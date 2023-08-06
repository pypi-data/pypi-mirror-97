class ServerError(Exception):
    def __init__(self, msg, code):
        super(ServerError, self).__init__(msg)
        self.code = code


class UnknownResult(Exception):
    def __init__(self, result):
        self.result = result

    def __str__(self):
        return 'Cannot parse Result buffer. Unknown result subfields. Result is {}'.format(self.result)
