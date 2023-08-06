'''
Data modification message
'''

from sap.audit_logging.util import validate_object
from sap.audit_logging.messages.transactional_message import TransactionalMessage

DATA_MODIFICATION_ENDPOINT = '/data-modifications'


class DataModificationMessage(TransactionalMessage):
    ''' DataModificationMessage '''

    def __init__(self, logger):
        # pylint: disable=super-with-arguments
        super(DataModificationMessage, self).__init__(
            logger, DATA_MODIFICATION_ENDPOINT)
        self._mandatory_properties.extend(['data_subject'])

    def set_data_subject(self, data_subject):
        '''
        Sets the data_subject properties.

        :param data_subject: Dict containing the data_subject attributes.
        '''
        validate_object(data_subject, 'data_subject')
        self._message['data_subject'] = data_subject
        return self
