""" This module classifies objects in Weaviate """

import time


def _is_finished(status):
    return status["status"] == "completed" or status["status"] == "failed"


def _print_classification_status(client, status):
    print("Started classifying -------------", status["status"])
    status = client.classification.get(status["id"])
    while not _is_finished(status):
        time.sleep(1.0)
        status = client.classification.get(status["id"])
    print("Finished classifying ------------", status["status"])
    print(status, "\n")


def create_default_where_clause(config, value):
    clause = {}

    clause['path'] = ['validated']
    clause['operator'] = "Equal"
    clause['valueBoolean'] = True

    return clause


def create_where_clause(config, value):
    clause = None

    if 'dynamic_select' in config and config['dynamic_select']['active']:

        field = config['dynamic_select']['field']
        clause = {}

        clause['path'] = [field]
        clause['operator'] = "Equal"
        clause['valueString'] = value

    return clause


def execute_classification(client, config, value=None):
    """ This function classifies the data specified in the argument config dict. It uses the
    methodology also specified in the config dict.
    Args:
        - client (weaviate): The Weaviate client in which the data is to be classified
        - config (dict): a dict with the configuration for the classification.
    Returns:
        - nothing
    """

    if client is not None and config is not None and 'classification' in config:

        clause = None
        default = False
        if value is None:
            clause = create_default_where_clause(config, value)
            default = True
        else:
            clause = create_where_clause(config, value)

        classification = config['classification']
        # Read the classification type from the config file. Default = "knn"
        if 'classification_type' in classification:
            ctype = classification['classification_type']
        else:
            ctype = "knn"

        # Next determine which class and which property must be classified
        keys = ['classify_class', 'classify_properties', 'based_on_properties']
        if all (key in classification for key in keys):
            cclass = classification['classify_class']
            cprop = classification['classify_properties']
            cbase = classification['based_on_properties']

            # First determine the type of classification. This can either be "knn" or "contextual"
            if ctype == "knn":
                # Determine the number of neighbors
                nn = 5
                if 'number_of_neighbors' in classification:
                    nn = classification['number_of_neighbors']

                # Get the base configuration for the classification
                baseconfig = client.classification.schedule()\
                    .with_type('knn')\
                    .with_class_name(cclass)\
                    .with_classify_properties(cprop)\
                    .with_based_on_properties(cbase)\
                    .with_k(nn)
                if clause is not None:
                    if default:
                        baseconfig = baseconfig.with_training_set_where_filter(clause)
                    else:
                        baseconfig = baseconfig.with_training_set_where_filter(clause)
                        baseconfig = baseconfig.with_source_where_filter(clause)

            elif ctype == "contextual":
                # Get the base configuration for the classification
                baseconfig = client.classification.schedule() \
                    .with_type('contextual')\
                    .with_class_name(cclass)\
                    .with_classify_properties(cprop)\
                    .with_based_on_properties(cbase)

            else:
                print("Error: unknow classification type")

        print(baseconfig._config)
        status = baseconfig.do()
        _print_classification_status(client, status)
