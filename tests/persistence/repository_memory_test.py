from basis.persistence import MemoryRepository


class FakeEntity:
    def __init__(self, identifier: int) -> None:
        self.identifier: int = identifier


# Test read operations.


def test__memory_repository__there_entity_not_stored__return_none():
    with MemoryRepository() as store:
        found = store.find(entity_id=1)
        assert found is None


def test__memory_repository__when__entity_stored__return_it():
    with MemoryRepository(FakeEntity(1)) as store:
        found = store.find(entity_id=1)
        assert found.identifier == 1


def test__memory_repository__three_entites_stored__count_three():
    with MemoryRepository(*[FakeEntity(x) for x in range(3)]) as store:
        assert store.count() == 3


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
