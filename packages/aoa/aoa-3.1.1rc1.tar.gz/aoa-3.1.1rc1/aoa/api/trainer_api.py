from __future__ import absolute_import

from aoa.api.base_api import BaseApi


class TrainerApi(BaseApi):

    path = "/api/trainers"

    def find_all(self, projection: str = None):
        """
        returns all trainers

        Parameters:
           projection (str): projection type

        Returns:
            (dict): trainers
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
            self.path,
            header_params,
            query_params)
