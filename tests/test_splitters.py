from semantic_chunkers.splitters.regex import RegexSplitter

from patot.splitters import HebrewTokenizerSplitter, fallback_clause_split, sentence_splitter_for_language


def test_hebrew_tokenizer_splitter_splits_hebrew_sentences():
    splitter = HebrewTokenizerSplitter()
    result = splitter("שלום עולם. מה שלומך? טוב מאוד!")
    assert result == ["שלום עולם .", "מה שלומך ?", "טוב מאוד !"]


def test_hebrew_tokenizer_splitter_splits_english_sentences():
    splitter = HebrewTokenizerSplitter()
    result = splitter("hello world. how are you? fine!")
    assert result == ["hello world .", "how are you ?", "fine !"]


def test_hebrew_tokenizer_splitter_single_sentence_no_separators():
    splitter = HebrewTokenizerSplitter()
    assert splitter("one two three") == ["one two three"]


def test_hebrew_tokenizer_splitter_falls_back_to_clause_split():
    splitter = HebrewTokenizerSplitter()
    # No sentence-ending punctuation, but commas allow a clause-level fallback split.
    assert splitter("one, two, three") == ["one,", "two,", "three"]


def test_hebrew_tokenizer_splitter_empty_input():
    splitter = HebrewTokenizerSplitter()
    assert splitter("") == []


def test_sentence_splitter_for_language_hebrew():
    assert isinstance(sentence_splitter_for_language("he"), HebrewTokenizerSplitter)


def test_sentence_splitter_for_language_other_languages():
    assert isinstance(sentence_splitter_for_language("en"), RegexSplitter)
    assert isinstance(sentence_splitter_for_language("fr"), RegexSplitter)


def test_fallback_clause_split_basic():
    assert fallback_clause_split("a, b: c") == ["a,", "b:", "c"]


def test_fallback_clause_split_no_separators_returns_single_chunk():
    assert fallback_clause_split("just text") == ["just text"]


def test_fallback_clause_split_strips_whitespace():
    assert fallback_clause_split("  a , b  ") == ["a ,", "b"]


def test_fallback_clause_split_empty_string():
    assert fallback_clause_split("") == []
