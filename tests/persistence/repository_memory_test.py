from basis.persistence import MemoryRepository
from basis.persistence import ConflictError


class FakeEntity:
    def __init__(self, identifier: int) -> None:
        self.identifier: int = identifier


# Test read operations.


def test__memory_repository__entity_not_stored__return_none():
    with MemoryRepository() as store:
        found = store.find(entity_id=1)
        assert found is None


def test__memory_repository___entity_stored__return_it():
    with MemoryRepository([FakeEntity(1)]) as store:
        found = store.find(entity_id=1)
        assert found.identifier == 1


def test__memory_repository__three_entites_stored__count_three():
    with MemoryRepository([FakeEntity(x) for x in range(3)]) as store:
        assert store.count() == 3


def test__memory_repository__entity_stored__exists_return_true():
    entity = FakeEntity(1)
    with MemoryRepository([entity]) as store:
        assert store.exists(entity) is True


# Test write operations.


def test__memory_repository__entities_stored_after_manual_commit():
    store = MemoryRepository()
    store.save(FakeEntity(1))
    store.save(FakeEntity(2))
    store.commit()
    assert store.count() == 2


def test__memory_repository__entities_not_stored_after_manual_revert():
    store = MemoryRepository()
    store.save(FakeEntity(1))
    store.save(FakeEntity(2))
    store.revert()
    assert store.count() == 0


def test_memory_repository__entities_stored_after_managed_commit():
    with MemoryRepository() as store:
        store.save(FakeEntity(1))
        store.save(FakeEntity(2))
    assert store.count() == 2


def test_memory_repository_custom_function_init_store():
    first = {'identifier': 1, 'data': 'n;jkl;jioiijkljl'}
    second = {'identifier': 2, 'data': 'wfdsafskljl'}
    third = {'identifier': 3, 'data': 'n;hjgfd'}

    with MemoryRepository((first, second, third), lambda x: x['identifier']) as store:
        assert second == store.find(2)
        assert first == store.find(1)
        assert third == store.find(3)


def test_memory_repository_custom_function_store():
    first = {'identifier': 1, 'data': 'n;jkl;jioiijkljl'}
    second = {'identifier': 2, 'data': 'wfdsafskljl'}

    store = MemoryRepository(identity_function=lambda x: x['identifier'])
    store.save(first)
    store.save(second)
    store.commit()
    assert store.find(1) == first
    assert store.find(2) == second


def test_memory_repository_entity_conflict():
    with MemoryRepository([FakeEntity(1)]) as store:
        try:
            store.save(FakeEntity(1))
            assert False
        except ConflictError:
            assert True
