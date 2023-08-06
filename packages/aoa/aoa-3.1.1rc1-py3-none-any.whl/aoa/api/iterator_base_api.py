import abc
from aoa.api.base_api import BaseApi
from aoa.api.api_iterator import ApiIterator


class IteratorBaseApi(BaseApi):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def find_all(self):
        pass

    def __iter__(self):
        return ApiIterator(api_func=self.find_all, entities=self.path.split('/')[-2])

    def __len__(self):
        return self.find_all()['page']['totalElements']
