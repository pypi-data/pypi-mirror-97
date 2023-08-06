'''
Transactional message
'''

from sap.audit_logging.messages.audit_message import AuditMessage
from sap.audit_logging.util import validate_object


class TransactionalMessage(AuditMessage):
    ''' TransactionalMessage '''

    def __init__(self, logger, endpoint):
        # pylint: disable=super-with-arguments
        super(TransactionalMessage, self).__init__(logger, endpoint)
        self._mandatory_properties.extend(['object', 'attributes'])

    def log_prepare(self):
        ''' Indicate that the audit event is about to happen. '''
        self.log()

    def log_success(self):
        ''' Indicate that the audit event has been successful. '''
        self._log_state(True)

    def log_failure(self):
        ''' Indicate that the audit event has failed. '''
        self._log_state(False)

    def set_object(self, object_attributes):
        '''
        Sets the object properties.

        :param object_attributes: Dict containing the object attributes.
        '''
        validate_object(object_attributes, 'object_attributes')
        self._message['object'] = object_attributes
        return self

    def add_attribute(self, name, old_value=None, new_value=None):
        '''
        Used when a new value is added, and existing one is modified or removed.
        Sets the heading name for the attribute that has been modified.

        :param name: The attribute name
        :param old_value: The old value of the attribute.
            Should be used for modified and removed values.
        :param new_value: The new value of the attribute.
            Should be used for newly added and new modified values.
        '''
        entity = {
            'name': name
        }
        if old_value or new_value:
            entity['old'] = old_value
            entity['new'] = new_value
        self._add_entity(entity, 'attributes', 'name')

        return self

    def _log_state(self, state):
        if 'success' in self._message:
            raise RuntimeError('Message status already logged')

        self._update()
        self._message['success'] = state
        if not self._already_logged:
            self.log()
        else:
            self._logger.log(self._message, self._endpoint)
