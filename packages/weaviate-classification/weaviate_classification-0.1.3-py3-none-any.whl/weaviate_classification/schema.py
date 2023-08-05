""" This module creates a Weaviate schema from a data configuration file """

from .utilities import get_reference_property_name_from_field
from .utilities import get_reference_class_name_from_field


def _create_default_schema(dataconfig):

    # Initialize the return value
    schema = None

    if dataconfig is not None and 'classes' in dataconfig:

        # Add the default emppty list for classes to the schema
        schema = {}
        schema['classes'] = []

    return schema


def _create_classification_config_class(dataconfig, modulename):
    newclass = None

    if dataconfig is not None:
        newclass = {}
        newclass['class'] = "ClassificationConfiguration"
        newclass['description'] = "This class stores the configuration of the classification"
        newclass['moduleConfig'] = {}
        newclass['moduleConfig'][modulename] = {}
        newclass['moduleConfig'][modulename]['vectorizeClassName'] = False
        newclass['properties'] = []

        # Add a property that holds the name of the class that has been classified
        prop = {}
        prop['name'] = 'classname'
        prop['dataType'] = ["string"]
        prop['description'] = "Name of this class that has been classified"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

        # Add a property that holds the names of the fields that have been classified
        prop = {}
        prop['name'] = 'properties'
        prop['dataType'] = ["string"]
        prop['description'] = "Names of properties that have been classified"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

        # Add a property that holds the number of batches that have been classified
        prop = {}
        prop['name'] = 'batchCount'
        prop['dataType'] = ["int"]
        prop['description'] = "Number of batches in the classification"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

        # Add a property that holds the type of classification
        prop = {}
        prop['name'] = 'type'
        prop['dataType'] = ["string"]
        prop['description'] = "Type of classification"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

        # Add a property that holds the number of neighbors (in case of a knn classification)
        prop = {}
        prop['name'] = 'numberOfNeighbors'
        prop['dataType'] = ["int"]
        prop['description'] = "The number of neighbors in a knn classification"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

        # Add a property that holds the number of confidence buckets
        prop = {}
        prop['name'] = 'confidenceBuckets'
        prop['dataType'] = ["int"]
        prop['description'] = "The number of confidence buckets in a classification"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

    return newclass


def _create_property_from_column(col, modulename):
    prop = None

    if col is not None:
        prop = {}
        prop['name'] = col['name']
        prop['dataType'] = [col['type']]
        prop['description'] = col['name']
        prop['indexInverted'] = col['indexInverted']
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = not prop['indexInverted']
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False

    return prop


def _create_confidence_score_property_from_column(col, modulename):
    prop = None

    if col is not None:
        prop = {}
        prop['name'] = col['name'] + 'ConfidenceScore'
        prop['dataType'] = ['number']
        prop['description'] = "This property stores the confidence score for classification"
        prop['indexInverted'] = False
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = True
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False

    return prop


def _create_confidence_bucket_property_from_column(col, modulename):
    prop = None

    if col is not None:
        prop = {}
        prop['name'] = col['name'] + 'ConfidenceBucket'
        prop['dataType'] = ['int']
        prop['description'] = "This property stores the confidence bucket for classification"
        prop['indexInverted'] = False
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = True
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False

    return prop


def _create_reference_property_from_column(col, modulename):
    prop = None

    if col is not None:
        prop = {}
        prop['name'] = get_reference_property_name_from_field(col['name'])
        prop['dataType'] = [get_reference_class_name_from_field(col['name'])]
        prop['description'] = prop['dataType'][0]
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False

    return prop


def _create_class_from_column(col, modulename):
    newclass = None

    if col is not None:
        newclass = {}
        newclass['class'] = get_reference_class_name_from_field(col['name'])
        newclass['description'] = newclass['class']
        newclass['moduleConfig'] = {}
        newclass['moduleConfig'][modulename] = {}
        newclass['moduleConfig'][modulename]['vectorizeClassName'] = True
        newclass['properties'] = []
        prop = {}
        prop['name'] = 'name'
        prop['dataType'] = ["string"]
        prop['description'] = "Name of this instance of this class"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = False
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        newclass['properties'].append(prop)

    return newclass


def _add_default_properties_to_mainclass(mainclass, modulename):

    if mainclass is not None:

        # the row proporty indicates the row number from the excel file that the data point was on
        prop = {}
        prop['name'] = 'row'
        prop['dataType'] = ["int"]
        prop['description'] = "The row number of the data point"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = True
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        mainclass['properties'].append(prop)

        # the validated property indicates whether this data point can be used for training
        prop = {}
        prop['name'] = 'validated'
        prop['dataType'] = ["boolean"]
        prop['description'] = "Indicates whether this data point can be used for training purposes"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = True
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        mainclass['properties'].append(prop)

        # the preClassified property indicates whether this data point can be used for training
        prop = {}
        prop['name'] = 'preClassified'
        prop['dataType'] = ["boolean"]
        prop['description'] = "Indicates whether this data point has been classified outside Weaviate"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = True
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        mainclass['properties'].append(prop)

        # the batchnumber property is used if the number of items to be classified exceeds the max
        prop = {}
        prop['name'] = 'batchNumber'
        prop['dataType'] = ["int"]
        prop['description'] = "Indicates the batch number if batching is used"
        prop['indexInverted'] = True
        prop['moduleConfig'] = {}
        prop['moduleConfig'][modulename] = {}
        prop['moduleConfig'][modulename]['skip'] = True
        prop['moduleConfig'][modulename]['vectorizePropertyName'] = False
        mainclass['properties'].append(prop)


def create_schema_from_data_configuration(config, dataconfig):
    """ create schema """

    # Initialize the return value
    schema = None

    # keep track of which classes for entities have been created
    entities = []

    # determine the module name. Default is 'text2vec-contextionary'
    modulename = "text2vec-contextionary"
    if config is not None and 'classification' in config and 'module_name' in config['classification']:
        modulename = config['classification']['module_name']

    # Create the schema from the data_configuration file
    if dataconfig is not None:
        schema = _create_default_schema(dataconfig)

        if schema is not None:

            # Add the class that holds the classification metadata
            newclass = _create_classification_config_class(dataconfig, modulename)
            schema['classes'].append(newclass)

            for dataclass in dataconfig['classes']:
                # Add the main class to the schema
                mainclass = {}
                mainclass['class'] = dataclass['classname']
                mainclass['moduleConfig'] = {}
                mainclass['moduleConfig'][modulename] = {}
                mainclass['moduleConfig'][modulename]['vectorizeClassName'] = True
                mainclass['description'] = "The class in this classification setup"
                mainclass['properties'] = []
                _add_default_properties_to_mainclass(mainclass, modulename)
                schema['classes'].append(mainclass)

                for col in dataclass['columns']:

                    # Create the property and add it to the schema
                    prop = _create_property_from_column(col, modulename)
                    if prop is not None:
                        mainclass['properties'].append(prop)

                    # If the column represents an entity we need to create a reference property and a new class
                    if col['entity']:
                        prop = _create_reference_property_from_column(col, modulename)
                        cprop = _create_confidence_score_property_from_column(col, modulename)
                        bprop = _create_confidence_bucket_property_from_column(col, modulename)
                        if prop is not None and cprop is not None and bprop is not None:
                            mainclass['properties'].append(prop)
                            mainclass['properties'].append(cprop)
                            mainclass['properties'].append(bprop)

                        if col['name'] not in entities:
                            entities.append(col['name'])
                            newclass = _create_class_from_column(col, modulename)
                            if newclass is not None:
                                schema['classes'].append(newclass)

    return schema
