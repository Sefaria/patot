import json

import pytest

from patot.json_loader import load_segment_records_from_json_file, load_segment_records_from_section
from patot.records import SegmentRecord


def test_load_segment_records_from_section_basic_ordering():
    section = {
        "ref": "Genesis 1",
        "segments": {
            "Genesis 1:2": "second",
            "Genesis 1:1": "first",
            "Genesis 1:10": "tenth",
        },
    }
    records = load_segment_records_from_section(section)
    assert [record.tref for record in records] == [
        "Genesis 1:1",
        "Genesis 1:2",
        "Genesis 1:10",
    ]
    assert [record.segment_index for record in records] == [1, 2, 3]
    assert all(record.kind == "base" for record in records)
    assert all(record.base_tref == "Genesis 1" for record in records)


def test_load_segment_records_from_section_strips_and_skips_empty():
    section = {
        "ref": "Genesis 1",
        "segments": {
            "Genesis 1:1": "  hello  ",
            "Genesis 1:2": "   ",
            "Genesis 1:3": "",
        },
    }
    records = load_segment_records_from_section(section)
    assert [record.tref for record in records] == ["Genesis 1:1"]
    assert records[0].text == "hello"


def test_load_segment_records_from_section_non_numeric_suffix_sorts_after_numeric():
    section = {
        "ref": "Genesis 1",
        "segments": {
            "Genesis 1:b": "b",
            "Genesis 1:1": "one",
            "Genesis 1:a": "a",
        },
    }
    records = load_segment_records_from_section(section)
    assert [record.tref for record in records] == [
        "Genesis 1:1",
        "Genesis 1:a",
        "Genesis 1:b",
    ]


def test_load_segment_records_from_section_requires_segments_dict():
    section = {"ref": "Genesis 1", "segments": ["not", "a", "dict"]}
    with pytest.raises(ValueError):
        load_segment_records_from_section(section)


def test_load_segment_records_from_section_missing_segments_returns_empty():
    section = {"ref": "Genesis 1"}
    assert load_segment_records_from_section(section) == []


def test_load_segment_records_from_json_file(tmp_path):
    payload = [
        {
            "ref": "Genesis 1",
            "segments": {"Genesis 1:1": "first", "Genesis 1:2": "second"},
        },
        {
            "ref": "Genesis 2",
            "segments": {"Genesis 2:1": "another"},
        },
    ]
    json_path = tmp_path / "sections.json"
    json_path.write_text(json.dumps(payload))

    sections = load_segment_records_from_json_file(json_path)
    assert len(sections) == 2
    assert [record.tref for record in sections[0]] == ["Genesis 1:1", "Genesis 1:2"]
    assert [record.tref for record in sections[1]] == ["Genesis 2:1"]
    assert isinstance(sections[0][0], SegmentRecord)


def test_load_segment_records_from_json_file_requires_top_level_list(tmp_path):
    json_path = tmp_path / "sections.json"
    json_path.write_text(json.dumps({"not": "a list"}))

    with pytest.raises(ValueError):
        load_segment_records_from_json_file(json_path)
