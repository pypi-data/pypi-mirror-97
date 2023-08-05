""" This module is for debugging only """

import sys
from .utilities import time_delay


def _count_datapoints_with_aggregate(client, dataconfig, whereclause=None):

    # Initialize the return value
    count = 0

    if client is not None and dataconfig is not None and 'classname' in dataconfig:

        # first get the classname from the data configuration
        classname = dataconfig['classname']

        # build the aggregate query
        builder = client.query.aggregate \
            .objects(classname) \
            .with_fields('meta { count }')

        # if there is a 'where_filter' specified, add it to the query
        if whereclause is not None:
            builder = builder.with_where(whereclause)

        # run the query and get the count from the query result
        result = builder.do()
        if result['errors'] is None:
            count = result["data"]["Aggregate"][classname][0]["meta"]["count"]

    return count


def _count_datapoints_with_get(client, dataconfig, whereclause=None):

    # Initialize the return value
    count = 0

    if client is not None and dataconfig is not None and 'classname' in dataconfig:

        # first get the classname from the data configuration
        classname = dataconfig['classname']

        # build the get query
        builder = client.query.get \
            .objects(classname, "validated") \
            .with_limit(10000)

        # if there is a 'where_filter' specified, add it to the query
        if whereclause is not None:
            builder = builder.with_where(whereclause)

        # run the query and get the count from the query result
        result = builder.do()
        count = len(result["data"]["Get"][classname])

    return count


def debug_compare_datapoint_count(client, config, dataconfig):
    """ debug """

    # add a small time delay to make sure all is updated
    time_delay(config)

    if client is not None and dataconfig is not None:

        # Count the number of datapoints using the aggregate query
        total = _count_datapoints_with_aggregate(client, dataconfig)

        where = {"operator": "Equal", "valueBoolean": True, "path": ["validated"]}
        aggvalidatedtrue = _count_datapoints_with_aggregate(client, dataconfig, where)
        getvalidatedtrue = _count_datapoints_with_get(client, dataconfig, where)

        where = {"operator": "Equal", "valueBoolean": False, "path": ["validated"]}
        aggvalidatedfalse = _count_datapoints_with_aggregate(client, dataconfig, where)
        getvalidatedfalse = _count_datapoints_with_get(client, dataconfig, where)

        print("\n\nAggregate")
        print("\ttotal (control): {}\n\tsum select {}\n".format(total, aggvalidatedtrue + aggvalidatedfalse))
        print("Get")
        print("\ttotal (control): {}\n\tsum select {}\n".format(total, getvalidatedtrue + getvalidatedfalse))
    else:
        print("Warning, can not print debug info: client or dataconfig None")

def _where_eligible_for_classification(props):
    operands = []
    for prop in props:
        operands += [{
            'valueInt': 0,
            'path': [prop],
            'operator': 'Equal',
        }]

    return {
        'operator': 'And',
        'operands': operands,
    }


def debug_assert_eligible_for_classification(client, config, dataconfig,
        expected_count=0):
    """
    Verifies the amount of items found to be classified matches the
    expected count. It will stop the entire script otherwise. Therefore
    only used with debugging flag.
    """

    if client is None or config is None:
        print("Warning, can not print debug info: client or config None")
        return

    props = config['classification']['classify_properties']
    where = _where_eligible_for_classification(props)

    actual_count = _count_datapoints_with_get(client, dataconfig, where)

    if actual_count != expected_count:
        msg = """
Fatal Classification Error: expected to find {} items eligble
for classification, but found {} instead.

This is not recoverable, exiting. To ignore this error, turn off
debug mode.
        """.format(expected_count, actual_count)
        print(msg)
        sys.exit(1)
    else:
        print("Found {} items eligble for classification - as expected".
                format(expected_count))
