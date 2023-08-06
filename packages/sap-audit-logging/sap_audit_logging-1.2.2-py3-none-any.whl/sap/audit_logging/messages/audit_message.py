'''
Audit message
'''
from datetime import datetime
from uuid import uuid4
from sap.audit_logging.util import check_non_empty_string, check_unique

__metaclass__ = type # pylint: disable=invalid-name

class AuditMessage:
    ''' AuditMessage '''

    def __init__(self, logger, endpoint):
        self._logger = logger
        self._endpoint = endpoint
        self._message = {}
        self._already_logged = False
        self._mandatory_properties = ['user']

    def log(self):
        '''Persists the already created and populated with relevant data audit message.'''
        if self._already_logged:
            raise RuntimeError('Message already logged')

        self._update()
        for prop in self._mandatory_properties:
            if prop not in self._message:
                raise RuntimeError('{0} not found in message'.format(prop))

        self._logger.log(self._message, self._endpoint)
        self._already_logged = True

    def set_user(self, user):
        '''
        Sets the user that triggered the audit event

        :param user: The user name
        '''
        check_non_empty_string(user, 'user')
        self._message['user'] = user
        return self

    def set_tenant(self, tenant):
        '''
        Sets the tenant that triggered the audit event

        :param tenant: The tenant
        '''
        check_non_empty_string(tenant, 'tenant')
        self._message['tenant'] = tenant
        return self

    def _add_entity(self, entity, entity_name, unique_key):
        check_non_empty_string(entity[unique_key], unique_key)

        if entity_name not in self._message:
            self._message[entity_name] = []

        entities = self._message[entity_name]
        check_unique(entities, unique_key, entity[unique_key])
        entities.append(entity)

    def _update(self):
        self._message['uuid'] = uuid4().hex
        self._message['time'] = datetime.utcnow().isoformat() + 'Z'
