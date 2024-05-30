import os
from typing import Any

from basis.aggregate import Entity
from basis.persistence import RestRepository


class FakeEntity(Entity[int]):
    def __init__(self,
                 identifier: int = None,
                 real: float = None,
                 text: str = None):
        super().__init__(identifier)
        self.float = real
        self.text = text


def compare_fake_entities(first: FakeEntity, second: FakeEntity) -> bool:
    are_same = True
    if first.identifier != second.identifier:
        are_same = False
    elif first.float != second.float:
        are_same = False
    return are_same


class FakeRequester:

    def __init__(self, server: dict = None):
        if server is None:
            self._server = {}
        else:
            self._server = server

    @staticmethod
    def _split_path(url: str) -> (str, str, int):
        url, data_type, data_id = url.split(os.path.sep)
        data_id = int(data_id)
        return url, data_type, data_id

    def _has_path(self, url, data_type, data_id) -> bool:
        if url not in self._server.keys():
            return False
        if data_type not in self._server[url].keys():
            return False
        if data_id not in self._server[url][data_type].keys():
            return False
        return True

    def _create_path_if_not_exist(self, url, data_type):
        if url not in self._server.keys():
            self._server[url] = {}
        if data_type not in self._server[url].keys():
            self._server[url][data_type] = {}

    def get(self, url) -> dict:
        url, data_type, data_id = self._split_path(url)
        if self._has_path(url, data_type, data_id):
            return self._server[url][data_type][int(data_id)]
        else:
            ValueError(f"Resource {url} not found.")

    def put(self, url, data: dict):
        url, data_type, data_id = self._split_path(url)
        if self._has_path(url, data_type, data_id):
            for key in self._server[url][data_type][int(data_id)].keys():
                self._server[url][data_type][int(data_id)][key] = data[key]
        else:
            raise ValueError(f"Resource {url} not found.")

    def post(self, url, data: dict):
        url, data_type = url.split(os.path.sep)
        self._create_path_if_not_exist(url, data_type)
        ids = self._server[url][data_type].keys()
        if len(ids) == 0:
            new_id = 0
        else:
            new_id = max(ids) + 1
        data['id'] = new_id
        self._server[url][data_type][new_id] = data
        return data

    def delete(self, url: str):
        url, data_type, data_id = self._split_path(url)
        if self._has_path(url, data_type, data_id):
            del self._server[url][data_type][int(data_id)]
        raise ValueError(f"{url}/{data_type}/{data_id} not found.")

    def get_count_with(self, uri: str) -> int:
        url, data_type = uri.split(os.path.sep)
        if url not in self._server.keys():
            return 0
        if data_type not in self._server[url].keys():
            return 0
        wanted_keys = self._server[url][data_type].keys()
        return len(wanted_keys)


FLOAT = 'FLOAT'
TEXT = 'TEXT'


class ExampleRestRepository(RestRepository[FakeEntity, int, dict[str, Any]]):
    def __init__(self, url='url', entity_uri='entity', requester=FakeRequester()):
        super().__init__(url, entity_uri)
        self._requester = requester

    def _to_data(self, entity: FakeEntity) -> dict[str, Any]:
        return {FLOAT: entity.float,
                TEXT: entity.text,
                'id': entity.identifier}

    def _to_entity(self, data: dict[str, Any]) -> FakeEntity:
        entity = FakeEntity(data['id'])
        entity.float = data[FLOAT]
        entity.text = data[TEXT]
        return entity

    def count(self) -> int:
        return self._requester.get_count_with(os.path.join(self._base_url, self._entity_uri))


def test__rest_repository__empty_repository():
    repository = ExampleRestRepository('empty')
    assert repository.count() == 0


def test__rest_repository__save_and_get():
    repository = ExampleRestRepository('save')

    entity = FakeEntity()
    entity.float = 3.14
    entity.text = 'testing now'

    entity = FakeEntity(repository.save(entity),
                        real=entity.float,
                        text=entity.text)

    assert compare_fake_entities(entity, repository.find(entity.identifier))
    assert repository.count() == 1


def test__rest_repository__entity_not_stored__return_none():
    with ExampleRestRepository('test') as store:
        found = store.find(entity_id=1)
        assert found is None

    server = {'test': {'not_test': {25: {FLOAT: 1.15,
                                         'id': 25,
                                         TEXT: 'jkl'}
                                    }
                       }
              }
    requester = FakeRequester(server)
    with ExampleRestRepository(url='test', entity_uri='test', requester=requester):
        found = store.find(entity_id=25)
        assert found is None


def test__rest_repository___entity_stored__return_it():
    server = {'test': {'not_test': {25: {FLOAT: 1.15,
                                         'id': 25,
                                         TEXT: 'jkl'}
                                    }
                       }
              }
    requester = FakeRequester(server)
    with ExampleRestRepository('test', 'not_test', requester) as store:
        found = store.find(entity_id=25)
        assert found.identifier == 25


def test__rest_repository__three_entites_stored__count_three():
    server = {'test': {'not_test': {25: {FLOAT: 1.15,
                                         'id': 25,
                                         TEXT: 'jkl'},
                                    1: {FLOAT: 13,
                                        'id': 1,
                                        TEXT: 'here'},
                                    2: {FLOAT: 11,
                                        'id': 2,
                                        TEXT: 'this'}
                                    }
                       }
              }
    requester = FakeRequester(server)
    with ExampleRestRepository('test', 'not_test', requester) as store:
        assert store.count() == 3


def test__rest_repository__entity_stored__exists_return_true():
    server = {'test': {'not_test': {25: {FLOAT: 1.15,
                                         'id': 25,
                                         TEXT: 'jkl'}
                                    }
                       }
              }
    entity = FakeEntity(identifier=25, real=1.15, text='jkl')
    requester = FakeRequester(server)
    with ExampleRestRepository('test', 'not_test', requester) as store:
        assert store.exists(entity) is True


# Test write operations.


def test__rest_repository__entities_stored():
    store = ExampleRestRepository('test')
    store.save(FakeEntity(real=15, text='jk'))
    store.save(FakeEntity(real=13, text='f'))
    assert store.count() == 2
