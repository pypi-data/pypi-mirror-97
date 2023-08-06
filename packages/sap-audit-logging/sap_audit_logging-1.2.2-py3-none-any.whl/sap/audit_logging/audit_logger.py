'''
Audit logger message factory.
'''
import logging
from cfenv import AppEnv
from sap.audit_logging.loggers import ConsoleLogger, HttpLogger
from sap.audit_logging.messages.configuration_change_message import ConfigurationChangeMessage
from sap.audit_logging.messages.data_access_message import DataAccessMessage
from sap.audit_logging.messages.data_modification_message import DataModificationMessage
from sap.audit_logging.messages.security_event_message import SecurityEventMessage
AUDIT_LOG_LABEL = 'auditlog'


class AuditLogger:
    ''' AuditLogger '''

    def __init__(self, service_instance_name=None):
        app_env = AppEnv()
        audit_log_service = None
        if service_instance_name is not None:
            audit_log_service = app_env.get_service(name=service_instance_name)
            if not audit_log_service:
                raise ValueError(
                    'Could not find service with name={0}'.format(service_instance_name))
        else:
            audit_log_service = app_env.get_service(label=AUDIT_LOG_LABEL)

        if audit_log_service is None:
            logging.basicConfig()
            logging.getLogger(__name__).warning(
                'Audit log service not found. Using console logger.')
            self._logger = ConsoleLogger()
        else:
            self._logger = HttpLogger(audit_log_service.credentials)

    def create_data_access_msg(self):
        ''' create data access message '''
        return DataAccessMessage(self._logger)

    def create_data_modification_msg(self):
        ''' create data modification message '''
        return DataModificationMessage(self._logger)

    def create_configuration_change_msg(self):
        ''' create configuration change message '''
        return ConfigurationChangeMessage(self._logger)

    def create_security_event_msg(self):
        ''' create security event message '''
        return SecurityEventMessage(self._logger)
