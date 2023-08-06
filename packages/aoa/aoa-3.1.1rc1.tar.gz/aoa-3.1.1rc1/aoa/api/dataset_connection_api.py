from __future__ import absolute_import
from typing import Dict

from aoa.api.iterator_base_api import IteratorBaseApi


class DatasetConnectionApi(IteratorBaseApi):
    path = "/api/datasetConnections/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all dataset connections of a project

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all dataset connections
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection', 'sort', 'page', 'size', 'sort']
        query_vals = [projection, sort, page, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path,
            header_params,
            query_params)

    def find_by_id(self, dataset_connection_id: str, projection: str = None):
        """
        returns a dataset connection of a project

        Parameters:
           dataset_connection_id (str): dataset connection id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): dataset connection
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + dataset_connection_id,
            header_params,
            query_params)

    def render_vars(self, dataset_connection_id: str):
        """
        returns dictionary with the env vars for a given dataset connection of a project

        Parameters:
           dataset_connection_id (str): dataset connection id(uuid) to find

        Returns:
            (dict): dataset connection envs
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        return self.aoa_client.get_request(
            self.path + dataset_connection_id + "/renderVars",
            header_params,
            dict())

    def save(self, dataset_connection: Dict[str, str]):
        """
        register a dataset connection

        Parameters:
           dataset connection (dict): dataset connection to register

        Returns:
            (dict): dataset template
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        self.required_params(['name', 'description', 'type', 'metadata', 'credentials'], dataset_connection)

        query_params = {}

        return self.aoa_client.post_request(
            self.path,
            header_params,
            query_params,
            dataset_connection)
