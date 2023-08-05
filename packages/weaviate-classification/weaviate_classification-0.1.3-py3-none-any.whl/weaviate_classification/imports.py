""" This module parses ex-factory excel file from PVM """

import uuid
import weaviate
from .utilities import get_reference_class_name_from_field
from .utilities import get_reference_property_name_from_field
from .query import get_classification_configuration


def _generate_uuid_for_entity(entity, key):

    newuuid = ""

    uuidstring = entity + "_" + key
    newuuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, uuidstring))

    return newuuid


def generate_uuid_for_datapoint(dataconfig, point):

    newuuid = ""

    if dataconfig is not None and point is not None:
        for dataclass in dataconfig['classes']:
            if dataclass['classname'] == point['classname']:
                string = "point_"

                # loop through the columns and add values for those columns that are identifier columns
                for col in dataclass['columns']:
                    if col['id']:
                        string = string + point[col['name']]

                    # generate the new uuid
                    newuuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
                break

    return newuuid


def set_cross_references(client, dataconfig, datapoints, entities):
    """ set cross references """

    pointcount = batchcount = 0
    if client is None or dataconfig is None or datapoints is None or entities is None:
        return

    batch = weaviate.ReferenceBatchRequest()
    for point in datapoints:

        # first get the classname from the data configuration
        classname = point['classname']

        # Only set the references if the point is validated
        if point['validated'] or point['preClassified']:
            pointcount += 1

            # Determine the uuid of the point
            produuid = generate_uuid_for_datapoint(dataconfig, point)

            for key in point:
                if key != 'classname' and point[key] is not None and point[key] != '':
                    entity = get_reference_class_name_from_field(key)
                    if entity in entities:

                        # Determine the uuid of the entity
                        entuuid = _generate_uuid_for_entity(entity, point[key])

                        propertyname = "of" + entity
                        batch.add(produuid, classname, propertyname, entuuid)

                        batchcount += 1
                        if (batchcount % 999) == 0:
                            client.batch.create_references(batch)
                            batch = weaviate.ReferenceBatchRequest()
                            batchcount = 0
                            print("Cross reference data points -----------:", pointcount, end="\r")

    if batchcount > 0:
        client.batch.create_references(batch)
        print("Cross reference data points -----------:", pointcount)


def reset_classification_configuration(client, config):

    # initialize the return value
    ccuid = None

    if config is not None and client is not None:

        thing = {}
        thing['classname'] = config['classification']['classify_class']
        thing['type'] = config['classification']['classification_type']
        thing['numberOfNeighbors'] = config['classification']['number_of_neighbors']
        thing['batchCount'] = 1

        # add the properties that have been classified
        properties = ""
        for prop in config['classification']['classify_properties']:
            if properties != "":
                properties += " "
            properties += prop
        thing['properties'] = properties

        # count the number of confidence buckets. Default is 1
        thing['confidenceBuckets'] = 1
        if 'classification' in config and 'confidence_buckets' in config['classification']:
            length = len(config['classification']['confidence_buckets']) - 1
            if length > 0:
                thing['confidenceBuckets'] = length

        # check if an instance of the classification configuration is already in Weaviate
        ccuuid = get_classification_configuration(client)

        # if not, then import it
        if ccuuid is None:
            ccuuid = client.data_object.create(thing, "ClassificationConfiguration")
        # otherwise reset it
        else:
            client.data_object.update(thing, "ClassificationConfiguration", ccuuid)

    return ccuuid


def import_entities_to_weaviate(client, entities):
    """ import entities """

    if client is not None and entities is not None:

        # initialize the count variables
        totalcount = batchcount = 0

        # create the first batch request
        batch = weaviate.ObjectsBatchRequest()

        # loop through all the entities and create an instance for each value
        for entity in entities:
            for name in entities[entity]:
                thing = {}
                thing['name'] = name
                newuuid = _generate_uuid_for_entity(entity, name)
                batch.add(thing, entity, newuuid)

                batchcount += 1
                totalcount += 1
                if (batchcount % 1000) ==0:
                    print("len batch:", len(batch))
                    print("Entities imported into Weaviate -------:", totalcount, end="\r")
                    result = client.batch.create_objects(batch)
                    batch = weaviate.ObjectsBatchRequest()
                    batchcount = 0
        if batchcount > 0:
            result = client.batch.create_objects(batch)
            print("Entities imported into Weaviate -------:", totalcount)


def import_datapoints_to_weaviate(config, client, dataconfig, datapoints, validated=True):
    """ import the datapoints """

    if client is not None and dataconfig is not None and datapoints is not None:

        # initialize the count variables
        totalcount = batchcount = 0

        # create the first batch request
        batch = weaviate.ObjectsBatchRequest()

        # loop through all data points and create an instance for each data point
        for point in datapoints:

            # first get the classname from the data configuration
            classname = point['classname']

            if point['validated'] == validated:

                # create the thing dictionary with all the values for the properties
                thing = {}
                for key in point:
                    if key != 'classname':
                        prop = get_reference_property_name_from_field(key)
                        if point['validated'] or point['preClassified'] or prop not in config['classification']['classify_properties']:
                            thing[key] = point[key]

                # create the uuid for the new data point
                newuuid = generate_uuid_for_datapoint(dataconfig, point)

                # Add the datapoint to the batch and increase the counters
                batch.add(thing, classname, newuuid)
                batchcount += 1
                totalcount += 1

                # if the batch size reaches the maximum size, import and start a new batch
                if (batchcount % 999) == 0:
                    print("Data points imported into Weaviate ----:", totalcount, end="\r")
                    result = client.batch.create_objects(batch)
                    batch = weaviate.ObjectsBatchRequest()
                    batchcount = 0

        # if there are left over points in the last batch, import these last data points
        if batchcount > 0:
            result = client.batch.create_objects(batch)
            print("Data points imported into Weaviate ----:", totalcount)
