from patot.text_utils import (
    detect_language,
    extract_html_footnotes,
    find_html_footnote_spans,
    normalize_whitespace,
    remove_html_footnotes,
    strip_hebrew_niqqud,
    strip_html,
)


def test_strip_html_replaces_tags_with_space():
    assert strip_html("<b>hello</b> <i>world</i>") == " hello   world "


def test_strip_html_no_tags():
    assert strip_html("plain text") == "plain text"


def test_find_html_footnote_spans_single():
    text = (
        'before '
        '<sup class="footnote-marker">1</sup><i class="footnote">note text</i>'
        ' after'
    )
    spans = find_html_footnote_spans(text)
    assert len(spans) == 1
    start, end = spans[0]
    assert text[start:end] == (
        '<sup class="footnote-marker">1</sup><i class="footnote">note text</i>'
    )


def test_find_html_footnote_spans_nested_italics():
    text = (
        '<sup class="footnote-marker">1</sup>'
        '<i class="footnote">outer <i>inner</i> tail</i>'
    )
    spans = find_html_footnote_spans(text)
    assert len(spans) == 1
    start, end = spans[0]
    assert text[start:end] == text


def test_find_html_footnote_spans_no_match():
    assert find_html_footnote_spans("no footnotes here") == []


def test_extract_html_footnotes():
    text = (
        'a '
        '<sup class="footnote-marker">1</sup><i class="footnote">first</i>'
        ' b '
        '<sup class="footnote-marker">2</sup><i class="footnote">second</i>'
        ' c'
    )
    footnotes = extract_html_footnotes(text)
    assert footnotes == [
        '<sup class="footnote-marker">1</sup><i class="footnote">first</i>',
        '<sup class="footnote-marker">2</sup><i class="footnote">second</i>',
    ]


def test_remove_html_footnotes():
    text = (
        'a '
        '<sup class="footnote-marker">1</sup><i class="footnote">first</i>'
        ' b'
    )
    assert remove_html_footnotes(text) == "a   b"


def test_remove_html_footnotes_no_footnotes_returns_same_text():
    text = "no footnotes here"
    assert remove_html_footnotes(text) is text


def test_strip_hebrew_niqqud_removes_vowel_points():
    # "שָׁלוֹם" with niqqud should become "שלום" without
    with_niqqud = "שָׁלוֹם"
    assert strip_hebrew_niqqud(with_niqqud) == "שלום"


def test_strip_hebrew_niqqud_leaves_plain_text_unchanged():
    assert strip_hebrew_niqqud("hello world") == "hello world"


def test_detect_language_hebrew():
    assert detect_language("שלום") == "he"


def test_detect_language_english():
    assert detect_language("hello world") == "en"


def test_detect_language_mixed_majority_hebrew():
    assert detect_language("שלום ab") == "he"


def test_normalize_whitespace_collapses_and_strips():
    assert normalize_whitespace("  a   b\n\tc  ") == "a b c"
