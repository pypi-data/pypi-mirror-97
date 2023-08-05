""" This module contains general utulity functions """

import math
import time
import yaml
import weaviate


DEFAULT_WEAVIATE = 'http://localhost:8080'


def read_classification_configuration_file():
    """ Read the classification configuration file """

    config = None
    with open('./config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


def get_weaviate_client(config):
    """ get the Weaviate client """

    client = None

    weaviatepath = DEFAULT_WEAVIATE
    if config is not None and 'weaviate' in config and 'path' in config['weaviate']:
        weaviatepath = config['weaviate']['path']

    client = weaviate.Client(weaviatepath)

    return client


def time_delay(config):
    """ get the delay """

    delay = 2.0
    if config is not None:
        if 'weaviate' in config and 'delay' in config['weaviate']:
            delay = config['weaviate']['delay']
    time.sleep(delay)


def calculate_size_training_set(config, data):
    """ calculate the size of the training set """

    # Initialize the return value
    size = None

    if config is not None and data is not None:
        size = {}
        size['total'] = 0
        size['validation_percentage'] = 20
        size['training_size'] = 0
        size['validation_size'] = 0
        size['max_batch_size'] = 5000
        size['random_selection'] = True
        size['modulus'] = 10

        # First determine the number of datapoints in Weaviate
        if 'count' in data:
            size['total'] = data['count']

        # read the sample percentage from the config file.
        if 'validation' in config and 'validation_percentage' in config['validation']:
            size['validation_percentage'] = config['validation']['validation_percentage']

        # determine the max batch size
        if 'classification' in config and 'max_batch_size' in config['classification']:
            size['max_batch_size'] = config['classification']['max_batch_size']

        # Check if the validation size will not exceed the max batch size
        if round(size['total'] * (size['validation_percentage'] / 100)) > size['max_batch_size']:
            size['validation_percentage'] = math.floor((size['max_batch_size'] / size['total']) * 100) - 1
            if size['validation_percentage'] == 0:
                size['validation_percentage'] = 1
            print("Warning: validation size exceeds limit, resetting to:", size['validation_percentage'])

        # check whether selection of the validation data is random or fixed
        if 'validation' in config and 'random_selection' in config['validation']:
            size['random_selection'] = config['validation']['random_selection']

        size['modulus'] = round(size['total'] / (size['total'] * (size['validation_percentage'] / 100)))

    return size


def get_class_name_from_reference_property(prop):
    """ This function generates the right name of the property / class based on the input
        example:
            field name = flavour
            reference property name = ofFlavour
            entity class name = Flavour
            confidence score field name = flavourConfidenceScore
            confidence bucket field name = flavourConfidenceBucket
    """
    # turns "ofFlavour" into "Flavour" - note the upper case 'F' at the start
    return prop[2:]


def get_field_name_from_reference_property(prop):
    """ This function generates the right name of the property / class based on the input
        example:
            field name = flavour
            reference property name = ofFlavour
            entity class name = Flavour
            confidence score field name = flavourConfidenceScore
            confidence bucket field name = flavourConfidenceBucket
    """
    # turns "ofFlavour" into "flavour" - note the lower case 'f' at the start
    return prop[2].lower() + prop[3:]


def get_confidence_score_field_name_from_reference_property(prop):
    """ This function generates the right name of the property / class based on the input
        example:
            field name = flavour
            reference property name = ofFlavour
            entity class name = Flavour
            confidence score field name = flavourConfidenceScore
            confidence bucket field name = flavourConfidenceBucket
    """
    # turns "ofFlavour" into "flavourConfidenceScore"
    return prop[2].lower() + prop[3:] + "ConfidenceScore"


def get_confidence_bucket_field_name_from_reference_property(prop):
    """ This function generates the right name of the property / class based on the input
        example:
            field name = flavour
            reference property name = ofFlavour
            entity class name = Flavour
            confidence score field name = flavourConfidenceScore
            confidence bucket field name = flavourConfidenceBucket
    """
    # turns "ofFlavour" into "flavourConfidenceScore"
    return prop[2].lower() + prop[3:] + "ConfidenceBucket"


def get_reference_property_name_from_field(field):
    """ This function generates the right name of the property / class based on the input
        example:
            field name = flavour
            reference property name = ofFlavour
            entity class name = Flavour
            confidence score field name = flavourConfidenceScore
            confidence bucket field name = flavourConfidenceBucket
    """
    # turns "flavour" into "ofFlavour"
    return 'of' + field[:1].upper() + field[1:]


def get_reference_class_name_from_field(field):
    """ This function generates the right name of the property / class based on the input
        example:
            field name = flavour
            reference property name = ofFlavour
            entity class name = Flavour
            confidence score field name = flavourConfidenceScore
            confidence bucket field name = flavourConfidenceBucket
    """
    # turns "flavour" into "Flavour" - note the upper case 'F' at the start
    return field[:1].upper() + field[1:]


def get_cellid_of_field(dataconfig, field, row):
    """ get the id if a cell in excel """

    # first get the number of the column for this field
    for dataclass in dataconfig['classes']:
        for col in dataclass['columns']:
            if col['name'] == field:
                number = col['number']

    # then translate the number of the column to a excel string
    string = ""
    while number > 0:
        number, remainder = divmod(number - 1, 26)
        string = chr(65 + remainder) + string

    return string + str(row)
