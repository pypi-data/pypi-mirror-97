'''
Data access message
'''

from sap.audit_logging.util import check_boolean, check_non_empty_string, validate_object
from sap.audit_logging.messages.audit_message import AuditMessage

DATA_ACCESS_ENDPOINT = '/data-accesses'


class DataAccessMessage(AuditMessage):
    ''' DataAccessMessage '''

    def __init__(self, logger):
        # pylint: disable=super-with-arguments
        super(DataAccessMessage, self).__init__(logger, DATA_ACCESS_ENDPOINT)
        self._mandatory_properties.extend(['attributes', 'object', 'data_subject'])

    def set_channel(self, channel):
        '''
        Sets the data access channel type (e.g. RFC, web service, IDOC,
        file based interfaces, user interface, spool, printing etc.).

        :param channel: The type of data access channel
        '''
        check_non_empty_string(channel, 'channel')
        self._message['channel'] = channel
        return self

    def set_object(self, object_attributes):
        '''
        Sets the object properties.

        :param object_attributes: Dict containing the object attributes.
        '''
        validate_object(object_attributes, 'object_attributes')
        self._message['object'] = object_attributes
        return self

    def set_data_subject(self, data_subject):
        '''
        Sets the data_subject properties.

        :param data_subject: Dict containing the data_subject attributes.
        '''
        validate_object(data_subject, 'data_subject')
        self._message['data_subject'] = data_subject
        return self

    def add_attribute(self, name, is_successful):
        '''
        Sets the heading name for the attribute that has been read, either successfully or not.

        :param name: The attribute name
        :param is_successful: Whether or not the access to the attribute was successful
        '''
        check_boolean(is_successful, 'is_successful')
        self._add_entity({
            'name': name,
            'successful': is_successful
        }, 'attributes', 'name')
        return self

    def add_attachment(self, attachment_id, name):
        '''
        Sets the attachment name and id in case the event is triggered
        by the download or display of some attachments or files.

        :param attachment_id: Attachment id
        :param name: Attachment name
        '''
        check_non_empty_string(name, 'name')
        self._add_entity({
            'id': attachment_id,
            'name': name
        }, 'attachments', 'id')
        return self
