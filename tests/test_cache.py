from patot.cache import cache_lookup, cache_update


def test_cache_lookup_miss_returns_none(tmp_path):
    cache_path = str(tmp_path / "cache.sqlite")
    assert cache_lookup("prompt", "llm-string", cache_path) is None


def test_cache_update_then_lookup_returns_values(tmp_path):
    cache_path = str(tmp_path / "cache.sqlite")
    values = [0.1, 0.2, 0.3]
    cache_update("prompt", "llm-string", values, cache_path)
    assert cache_lookup("prompt", "llm-string", cache_path) == values


def test_cache_lookup_distinguishes_llm_string(tmp_path):
    cache_path = str(tmp_path / "cache.sqlite")
    cache_update("prompt", "llm-a", [1.0], cache_path)
    assert cache_lookup("prompt", "llm-b", cache_path) is None
    assert cache_lookup("prompt", "llm-a", cache_path) == [1.0]


def test_cache_update_overwrites_existing_entry(tmp_path):
    cache_path = str(tmp_path / "cache.sqlite")
    cache_update("prompt", "llm-string", [1.0], cache_path)
    cache_update("prompt", "llm-string", [2.0], cache_path)
    assert cache_lookup("prompt", "llm-string", cache_path) == [2.0]


def test_cache_max_entries_evicts_oldest(tmp_path):
    cache_path = str(tmp_path / "cache.sqlite")
    cache_update("prompt-1", "llm-string", [1.0], cache_path, max_entries=2)
    cache_update("prompt-2", "llm-string", [2.0], cache_path, max_entries=2)
    cache_update("prompt-3", "llm-string", [3.0], cache_path, max_entries=2)

    # The oldest entry (prompt-1) should have been evicted to keep at most 2 rows.
    assert cache_lookup("prompt-1", "llm-string", cache_path) is None
    assert cache_lookup("prompt-2", "llm-string", cache_path) == [2.0]
    assert cache_lookup("prompt-3", "llm-string", cache_path) == [3.0]


def test_cache_max_entries_must_be_positive(tmp_path):
    cache_path = str(tmp_path / "cache.sqlite")
    try:
        cache_update("prompt", "llm-string", [1.0], cache_path, max_entries=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for max_entries=0")
