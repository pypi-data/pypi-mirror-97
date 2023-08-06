'''
Configuration change message
'''


from sap.audit_logging.messages.transactional_message import TransactionalMessage

CONFIGURATION_CHANGE_ENDPOINT = '/configuration-changes'


class ConfigurationChangeMessage(TransactionalMessage):
    ''' ConfigurationChangeMessage '''

    def __init__(self, logger):
        # pylint: disable=super-with-arguments
        super(ConfigurationChangeMessage, self).__init__(
            logger, CONFIGURATION_CHANGE_ENDPOINT)
