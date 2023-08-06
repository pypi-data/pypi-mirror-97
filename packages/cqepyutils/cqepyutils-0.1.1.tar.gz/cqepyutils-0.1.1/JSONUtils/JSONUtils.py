import json
import pandas as pd


def extract_partial_data_from_json(json_data: str, json_partial_data_key: str):
    """
    This method is used to extract partial data based on the key from json
    :param json_data:
    :param json_partial_data_key:
    :return:
    """

    # filter data based on key from json
    json_required_data = json_data[json_partial_data_key]

    # return the filtered json data
    return json_required_data


def convert_dict_to_df(dict_data: dict):
    """
    This method is used to convert dictionary data to pandas data frame
    :param dict_data:
    :return:
    """

    # create df using dict
    dict_data_df = pd.DataFrame.from_dict([dict_data])

    # return the converted df
    return dict_data_df


def convert_json_to_df(json_data: str):
    """
    This method is used to convert json data to pandas data frame
    :param json_data:
    :return:
    """

    # create df using dict
    json_data_df = pd.DataFrame([json_data])

    # return the converted df
    return json_data_df


# def write_json_file(json_object: object, file_path: str, file_name: str):
#     """
#     This method is used to create json file using json object
#     :param json_object:
#     :param file_path:
#     :param file_name:
#     :return:
#     """
#
#     # create df using dict
#     json_data_df = pd.DataFrame([json_data])
#
#     # return the converted df
#     return json_data_df
