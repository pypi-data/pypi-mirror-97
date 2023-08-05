""" This module calculates the confidence score from classification by Weaviate """

import os
import math
import weaviate
from .utilities import get_weaviate_client
from .utilities import get_field_name_from_reference_property
from .utilities import get_confidence_score_field_name_from_reference_property
from .utilities import get_confidence_bucket_field_name_from_reference_property
from .query import count_number_of_unvalidated_datapoints
from .query import create_get_query_batch_number


def _pull_all_classified_datapoints_from_Weaviate(client, config, dataconfig):

    # initialize the return value
    datapoints = []

    if client is not None and config is not None:

        # get the classname of the property that was classified
        classname = config['classification']['classify_class']

        # get the maximum batch size from the config file
        maxbatch = 10000
        if 'classification' in config and 'max_batch_size' in config['classification']:
            maxbatch = config['classification']['max_batch_size']

        # count the number of instances of the main class in Weaviate
        count = count_number_of_unvalidated_datapoints(client, classname)

        # if count > maxbatch, we need to pull the result out in batches.
        batchcount = math.ceil(count / maxbatch)
        for batch in range(1, batchcount + 1):

            query = create_get_query_batch_number(client, config, dataconfig, batch)
            result = client.query.raw(query)
            if result is not None and 'data' in result:
                datapoints += result['data']['Get'][classname]

    return datapoints


def _extract_classification_scores(config, dataconfig, point):

    # initialize the return value
    score = {}

    if config is not None and dataconfig is not None and point is not None:

        # check if the point is pre-classified. If so, all scores should be 1.0
        preclass = False
        if 'preClassified' in point['properties'] and point['properties']['preClassified']:
            preclass = True

        for prop in config['classification']['classify_properties']:
            if 'properties' in point and prop in point['properties'] and len(point['properties'][prop]) > 0:
                if preclass:
                    score[prop] = 1.0
                elif 'classification' in point['properties'][prop][0]:
                    outcome = point['properties'][prop][0]['classification']
                    score[prop] = outcome['winningCount'] / outcome['overallCount']

    return score


def get_bucket_id(buckets, score):

    # initialize the return value
    result = 0
    if score > 0.0:
        for bid in buckets:
            if score > buckets[bid]['lower'] and score <= buckets[bid]['upper']:
                result = bid

    return result


def get_confidence_buckets(config):

    # initialize the return value
    buckets = {}

    # get the confidence score intervals from the config file (if present). Default = [0.0, 1.0]
    if config is not None and 'classification' in config and 'confidence_buckets' in config['classification']:
        intervals = config['classification']['confidence_buckets']
    else:
        intervals = [0.0, 1.0]

    length = len(intervals)
    for count in range(length-1):
        buckets[count] = {}
        buckets[count]['lower'] = intervals[count]
        buckets[count]['upper'] = intervals[count+1]
        buckets[count]['correct'] = 0
        buckets[count]['incorrect'] = 0
        buckets[count]['count'] = 0

    return buckets


def calculate_confidence_scores(client, config, dataconfig):
    """ calculate the confidence scores for datapoints """

    # first get the confidence buckets from the config file
    buckets = get_confidence_buckets(config)

    count = 0
    datapoints = _pull_all_classified_datapoints_from_Weaviate(client, config, dataconfig)
    for point in datapoints:
        if '_additional' in point and 'id' in point['_additional']:
            count += 1
            puuid = point['_additional']['id']
            path = "/objects/" + puuid + "?include=classification"
            result = client._connection.run_rest(path, 0)
            score = _extract_classification_scores(config, dataconfig, result.json())
            for prop in score:

                # initialize the update
                update = {}

                # calculate the confidence score
                scoreprop = get_confidence_score_field_name_from_reference_property(prop)
                update[scoreprop] = score[prop]

                # calculate the confidence bucket
                bucketprop = get_confidence_bucket_field_name_from_reference_property(prop)
                bid = get_bucket_id(buckets, score[prop])
                update[bucketprop] = bid

                # do the actual update
                client.data_object.update(update, "Component", puuid)

                print("Number of data points scored ----------:", count, end="\r")
    print("Number of data points scored ----------:", count)


def calculate_confidence_score_for_point(config, dataconfig, puuid):

    # initialize the return value
    score = None

    # get the Weaviate client
    client = get_weaviate_client(config)

    if client is not None and dataconfig is not None:
        path = "/objects/" + puuid + "?include=classification"
        result = client._connection.run_rest(path, 0)
        score = _extract_classification_scores(config, dataconfig, result.json())

    return score
