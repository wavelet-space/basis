from basis.persistence import MemoryRepository


class FakeEntity:
    def __init__(self, identifier: int) -> None:
        self.identifier: int = identifier


# Rest read operations


def test_memory_repository_finds_nothing():
    with MemoryRepository() as store:
        found = store.find(entity_id=1)
        assert found is None


def test_memory_repository_finds_something():
    with MemoryRepository(FakeEntity(1)) as store:
        found = store.find(entity_id=1)
        assert found.identifier == 1


def test_memory_repository_count():
    with MemoryRepository(*[FakeEntity(x) for x in range(5)]) as store:
        assert store.count() == 5


# Test write operations


def test_memory_repository_save_with_manual_commit():
    store = MemoryRepository()
    store.save(FakeEntity(1))
    store.save(FakeEntity(2))
    store.commit()
    assert store.count() == 2


def test_memory_repository_save_with_managed_commit():
    with MemoryRepository() as store:
        store.save(FakeEntity(1))
        store.save(FakeEntity(2))
    assert store.count() == 2
