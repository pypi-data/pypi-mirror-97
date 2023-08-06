from __future__ import absolute_import

from aoa.api.iterator_base_api import IteratorBaseApi


class DeploymentApi(IteratorBaseApi):
    path = "/api/deployments/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all deployments of a project

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all deployments
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

    def find_by_id(self, deployment_id: str, projection: str = None):
        """
        returns a deployment of a project

        Parameters:
           deployment_id (str): dataset id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): deployment
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
            self.path + deployment_id,
            header_params,
            query_params)

    def find_active_by_trained_model_and_engine_type(self, trained_model_id: str, engine_type: str, projection: str = None):
        """
        returns deployments by trained model and engine type

        Parameters:
           trained_model_id (str): trained model id(string) to find
           engine_type (str): engine type(string) to find
           projection (str): projection type

        Returns:
            (dict): deployments
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

        query_vars = ['trainedModelId', 'engineType', 'projection']
        query_vals = [trained_model_id, engine_type, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + "search/findActiveByTrainedModelIdAndEngineType",
            header_params,
            query_params)
