'''
Security event message
'''
from sap.audit_logging.util import check_non_empty_string
from sap.audit_logging.messages.audit_message import AuditMessage

SECURITY_EVENT_ENDPOINT = '/security-events'


class SecurityEventMessage(AuditMessage):
    ''' SecurityEventMessage '''

    def __init__(self, logger):
        # pylint: disable=super-with-arguments
        super(SecurityEventMessage, self).__init__(
            logger, SECURITY_EVENT_ENDPOINT)
        self._mandatory_properties.extend(['data'])

    def set_ip(self, source_ip):
        '''Sets the source IP address (in case of external access) that triggered the event.

        :param source_ip: The source IP address
        '''
        check_non_empty_string(source_ip, 'source_ip')
        self._message['ip'] = source_ip
        return self

    def set_data(self, data):
        '''
        Sets any data needed to fully understand the security relevant event.

        :param data: The detailed data describing this security event
        '''
        check_non_empty_string(data, 'data')
        self._message['data'] = data
        return self
