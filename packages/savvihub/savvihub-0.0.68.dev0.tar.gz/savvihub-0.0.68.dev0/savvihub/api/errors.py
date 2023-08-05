import json
import sys


class SavviHubError(Exception):
    error_code = 'UnexpectedProblem'
    _message = 'Unexpected problem found.'
    fields = []

    def __init__(self, message, fields=None):
        if message:
            self._message = message
        if fields:
            self.fields = fields

    def __eq__(self, other):
        return self.error_code == other.error_code

    def message(self):
        msg = self._message
        if self.fields:
            msg += ' ('
            for i, field in enumerate(self.fields):
                if i > 0:
                    msg += ', '
                msg += field['name']
                if field['value']:
                    msg += f': {field["value"]}'
            msg += ')'

        return msg


def inheritors(klass):
    subclasses = []
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.append(child)
                work.append(child)
    return subclasses


class SavviHubUnexpectedProblemError(SavviHubError):
    error_code = 'UnexpectedProblem'


class SavviHubNotADirectoryError(SavviHubError):
    error_code = 'NotADirectory'


class SavviHubNoSuchFileOrDirectoryError(SavviHubError):
    error_code = 'NoSuchFileOrDirectory'


class SavviHubK8sUnauthorizedError(SavviHubError):
    error_code = 'K8sUnauthorized'


class SavviHubK8sPermissionDeniedError(SavviHubError):
    error_code = 'K8sPermissionDenied'


class SavviHubK8sTimeoutError(SavviHubError):
    error_code = 'K8sTimeout'


class SavviHubConnectionRefusedError(SavviHubError):
    error_code = 'ConnectionRefused'


class SavviHubInvalidCACertError(SavviHubError):
    error_code = 'InvalidCACert'


class SavviHubNetworkTimeoutError(SavviHubError):
    error_code = 'NetworkTimeout'


def parse_error_code(resp):
    try:
        code = resp.json().get('code')
        message = resp.json().get('message')
        fields = resp.json().get('fields')

        for klass in inheritors(SavviHubError):
            if klass.error_code == code:
                return klass(message, fields)

        return SavviHubUnexpectedProblemError(message, fields)

    except Exception as e:
        return SavviHubUnexpectedProblemError(sys.exc_info()[0])
