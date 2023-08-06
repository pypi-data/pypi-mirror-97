'''
Utility functions
'''


def check_non_empty_string(string, name):
    ''' Checks if the provided argument is a non-empty string '''
    if not isinstance(string, str) or not string:
        raise ValueError('"{0}" should be a non-empty string'.format(name))


def check_unique(entities, key, value):
    ''' Checks if entity key is unique '''
    for entity in entities:
        if entity[key] == value:
            raise ValueError('Duplicate {0}: {1}'.format(key, value))


def check_boolean(value, name):
    ''' Checks if value is boolean '''
    if not isinstance(value, bool):
        raise ValueError('"{0}" should be boolean'.format(name))


def check_object_attribute(obj, obj_name, attr, attr_type):
    ''' Checks if object contains 'attr' of type 'attr_type' '''
    if not attr in obj or not isinstance(obj[attr], attr_type):
        raise ValueError(
            '"{0}" must contain a {1} attribute - "{2}"'.format(
                obj_name, attr_type, attr))

def validate_object(obj, obj_name):
    ''' Validates 'object_attributes' or 'data_subject' parameters '''
    if not isinstance(obj, dict) or not obj:
        raise ValueError(
            'Parameter "{0}" should be a non-empty dict'.format(obj_name))
    check_object_attribute(obj, obj_name, 'type', str)
    check_object_attribute(obj, obj_name, 'id', dict)
