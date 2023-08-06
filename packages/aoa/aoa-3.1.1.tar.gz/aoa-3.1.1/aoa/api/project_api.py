from __future__ import absolute_import
from typing import Dict

from aoa.api.iterator_base_api import IteratorBaseApi


class ProjectApi(IteratorBaseApi):

    path = "/api/projects/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all projects

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all projects
        """
        header_vars = ['Accept']
        header_vals = ['application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection', 'page', 'sort', 'size', 'sort']
        query_vals = [projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path,
            header_params,
            query_params)
    
    def find_by_id(self, project_id: str, projection: str = None):
        """
        returns a project

        Parameters:
           project_id (str): project id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): project
        """
        header_vars = ['Accept']
        header_vals = ['application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + project_id,
            header_params,
            query_params)
    
    def save(self, project: Dict[str, str]):
        """
        create a project

        Parameters:
           project (dict): project to create

        Returns:
            (dict): project
        """
        header_vars = ['Accept']
        header_vals = ['application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_params = {}

        self.required_params(['description', 'gitRepositoryUrl', 'groupId', 'name'], project)

        return self.aoa_client.post_request(
            self.path,
            header_params,
            query_params,
            project)

    def update(self, project: Dict[str, str]):
        """
        update a project

        Parameters:
           project (dict): project to update

        Returns:
            (dict): project
        """
        header_vars = ['Accept']
        header_vals = ['application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_params = {}

        self.required_params(['description', 'gitRepositoryUrl', 'groupId', 'name'], project)

        return self.aoa_client.put_request(
            self.path + self.aoa_client.project_id,
            header_params,
            query_params,
            project)
