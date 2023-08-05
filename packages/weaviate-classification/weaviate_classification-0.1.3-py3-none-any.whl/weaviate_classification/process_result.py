""" This module queries Weaviate """

import os
import math
import openpyxl

from .utilities import get_field_name_from_reference_property
from .utilities import get_cellid_of_field
from .query import count_number_of_unvalidated_datapoints
from .query import create_get_query_batch_number
from .imports import generate_uuid_for_datapoint
from.confidence import calculate_confidence_score_for_point
from.confidence import calculate_confidence_scores
from.confidence import get_confidence_buckets
from.confidence import get_bucket_id
from.confidence import calculate_confidence_scores
#from classification.Query import create_get_query_row_numbers

NON_PROPERTIES = ['classname', 'row', 'validated', 'preClassified', 'batchNumber']


############################################################################################################
##
## calculate_classification_score is only used in a validation run. It calculates which percentage of the
## classified items was correctly classified.
##
############################################################################################################


def _initialize_result_score(config, properties):
    score = {}
    score['total'] = 0
    for prop in properties:
        score[prop] = {}
        score[prop]['count'] = 0
        score[prop]['correct'] = 0
        score[prop]['incorrect'] = 0
        score[prop]['buckets'] = get_confidence_buckets(config)

    return score


def _index_datapoints_by_uuid(dataconfig, datapoints):
    index = {}
    for point in datapoints:
        temp = generate_uuid_for_datapoint(dataconfig, point)
        index[temp] = point
    return index


def _score_query_result(config, dataconfig, index, result, classname, properties, score):
    """ score the result of the classification by Weaviate """

    if result is None or 'data' not in result:
        print("No classified datapoints found --------:")
        return

    # Get the datapoints from the result argument
    points = result['data']['Get'][classname]

    # For each datapoint and for each property: check if the classification is the same as the original value
    for point in points:

        # count this datapoint in the total data point count
        score['total'] += 1

        # find the datapoint in the index
        puuid = point['_additional']['id']
        datapoint = index[puuid]

        # get the classification confidence score for this point
        confscore = calculate_confidence_score_for_point(config, dataconfig, puuid)

        # for each property, check if the classified value is the same as the stored value
        for prop in properties:

            bid = get_bucket_id(score[prop]['buckets'], confscore[prop])

            field = get_field_name_from_reference_property(prop)
            if prop in point and point[prop] is not None:

                score[prop]['count'] += 1
                score[prop]['buckets'][bid]['count'] += 1
                if point[prop][0]['name'] == datapoint[field]:
                    score[prop]['correct'] += 1
                    score[prop]['buckets'][bid]['correct'] += 1
                else:
                    score[prop]['incorrect'] += 1
                    score[prop]['buckets'][bid]['incorrect'] += 1
            else:
                print(point['row'], ";Warning: property", prop, "not found.")


def calculate_classification_score(client, config, dataconfig, datapoints):
    """ process result """

    if client is not None and config is not None and dataconfig is not None:

        # get the classname of the property that was classified
        classname = config['classification']['classify_class']

        # Determine the properties that have been classified
        properties = []
        if 'classification' in config and 'classify_properties' in config['classification']:
            for prop in config['classification']['classify_properties']:
                properties.append(prop)

        # get the maximum batch size from the config file
        if 'classification' in config and 'max_batch_size' in config['classification']:
            maxbatch = config['classification']['max_batch_size']

        # count the number of instances of the main class in Weaviate
        count = count_number_of_unvalidated_datapoints(client, classname)

        # initialize the dict that keeps score of the number of properties correctly classified
        score = _initialize_result_score(config, properties)

        # initialize a lookup table of all datapoints by uuid
        index = _index_datapoints_by_uuid(dataconfig, datapoints)

        # if count > maxbatch, we need to pull the result out in batches.
        batchcount = math.ceil(count / maxbatch)
        for batch in range(1, batchcount + 1):

            query = create_get_query_batch_number(client, config, dataconfig, batch)
            result = client.query.raw(query)

            _score_query_result(config, dataconfig, index, result, classname, properties, score)
            print("Total number of datapoints found ------:", score['total'])

        print(score)
        return

        if score['total'] > 0:
            for prop in properties:
                print(score[prop], "=", round((score[prop]/score['total'])*100),"%", "-", prop)
        else:
            print("Warning: zero classified data points --:")


############################################################################################################
##
## write_classification_result writes the outcome of the classification to an excel output file. The location
## of the file is determined by the config file, the filename is determined by the input file
##
############################################################################################################


def _write_query_result(sheet, result, dataconfig, properties, classname, score):
    """ Query Weaviate """

    if sheet is None or result is None or 'data' not in result:
        return

    # Prepare the result calculation. We count the number of correct matches. Initialize to zero for each property
    datapoints = result['data']['Get'][classname]

    # For each datapoint store the classified value
    for point in datapoints:
        score['total'] += 1
        for prop in properties:
            if prop in point and point[prop] is not None:
                field = get_field_name_from_reference_property(prop)
                cell = get_cellid_of_field(dataconfig, field, point['row'])
                if cell is not None:
                    sheet[cell] = point[prop][0]['name']


def write_classification_result(client, config, dataconfig, datapath):
    """ process result """

    if client is not None and config is not None and dataconfig is not None:

        # get the classname of the property that was classified
        classname = config['classification']['classify_class']

        # Determine the properties that have been classified
        properties = []
        if 'classification' in config and 'classify_properties' in config['classification']:
            for prop in config['classification']['classify_properties']:
                properties.append(prop)

        # get the maximum batch size from the config file
        if 'classification' in config and 'max_batch_size' in config['classification']:
            maxbatch = config['classification']['max_batch_size']

        # count the number of instances of the main class in Weaviate
        count = count_number_of_unvalidated_datapoints(client, classname)

        # initialize the dict that keeps score of the number of properties classified
        score = _initialize_result_score(config, properties)

        # create the excel file to write the result to
        workbook = openpyxl.load_workbook(datapath)
        sheet = workbook.active

        # if count > maxbatch, we need to pull the result out in batches.
        batchcount = math.ceil(count / maxbatch)
        for batch in range(1, batchcount + 1):

            query = create_get_query_batch_number(client, config, dataconfig, batch)
            print(query)
            result = client.query.raw(query)

            _write_query_result(sheet, result, dataconfig, properties, classname, score)
            print("Total number of datapoints found ------:", score['total'])
 
        _, tail = os.path.split(datapath)

        if 'output_path' in config:
            filename = config['output_path'] + tail
        else:
            filename = tail

        workbook.save(filename)
        workbook.close()


def write_datapoints_to_file(dataconfig, datapoints, filename, validated=None):
    """ write datapoints to file """

    if dataconfig is not None and datapoints is not None and filename is not None:

        # create the excel file to write the result to
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # For each datapoint store the classified value if we need to write it
        row = 1
        for point in datapoints:
            write = False
            if validated is None:
                write = True
            elif point['validated'] == validated:
                    write = True

            if write:
                row += 1
                for prop in point:
                    if prop not in NON_PROPERTIES:
                        cell = get_cellid_of_field(dataconfig, prop, row)
                        if cell is not None:
                            sheet[cell] = point[prop]

        workbook.save(filename)
        workbook.close()
    else:
        print("Error: can not write data points to file. Incomplete arguments")
