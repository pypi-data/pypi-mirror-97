from __future__ import absolute_import

from typing import List, Dict

from aoa.api_client import AoaClient


class BaseApi(object):
    path = ''

    def __init__(self, aoa_client=None):
        """
        constructor for api

        Parameters:
           aoa_client (AoaClient): AoaClient to use with api, if not specified will create a new AoaClient object
        """
        if aoa_client is None:
            aoa_client = AoaClient()
        self.aoa_client = aoa_client

    def generate_params(self, header_params: List[str], header_vals: List[str]):
        """
        returns generated parameters

        Parameters:
           header_params (List[str]): list of parameter names
           header_vals (List[str]): list of parameter values

        Returns:
            (dict): generated parameters
        """
        return dict(zip(header_params, header_vals))

    def required_params(self, param_names: List[str], dict_obj: Dict[str, str]):
        """
        checks required parameters, raises exception if the required parameter is missing in the dictionary

        Parameters:
           param_names (List[str]): list of required parameter names
           dict_obj (Dict[str, str]): dictionary to check for required parameters
        """
        for param in param_names:
            if param not in dict_obj:
                raise ValueError("Missing required value " + str(param))

