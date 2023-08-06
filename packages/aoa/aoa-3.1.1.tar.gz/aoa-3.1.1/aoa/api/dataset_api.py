from __future__ import absolute_import
from typing import Dict

from aoa.api.iterator_base_api import IteratorBaseApi


class DatasetApi(IteratorBaseApi):
    path = "/api/datasets/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all datasets of a project

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all datasets
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

    def find_by_id(self, dataset_id: str, projection: str = None):
        """
        returns a dataset of a project

        Parameters:
           dataset_id (str): dataset id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): dataset
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
            self.path + dataset_id,
            header_params,
            query_params)

    def find_by_name(self, dataset_name: str, projection: str = None):
        """
        returns a dataset of a project by name

        Parameters:
           dataset_name (str): dataset name(string) to find
           projection (str): projection type

        Returns:
            (dict): datasets
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

        query_vars = ['name', 'projection']
        query_vals = [dataset_name, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + "search/findByName",
            header_params,
            query_params)

    def find_by_dataset_template_id(self, dataset_template_id: str, projection: str = None):
        """
        returns a dataset of a project by name

        Parameters:
           dataset_template_id (str): dataset_template_id
           projection (str): projection type

        Returns:
            (dict): datasets
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

        query_vars = ['datasetTemplateId', 'projection']
        query_vals = [dataset_template_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + "search/findByDatasetTemplateId",
            header_params,
            query_params)

    def save(self, dataset: Dict[str, str]):
        """
        register a dataset

        Parameters:
           dataset (dict): dataset to register

        Returns:
            (dict): dataset
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

        self.required_params(['name', 'metadata'], dataset)

        query_params = {}

        return self.aoa_client.post_request(
            self.path,
            header_params,
            query_params,
            dataset)

