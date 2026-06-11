# patot

Hebrew/English-aware semantic chunking and Gemini embedding pipeline, extracted from
[Sefaria/ML-Workflows](https://github.com/Sefaria/ML-Workflows) (`app/embeddings/steps/patot`).

## Installation

```bash
pip install "patot[chunking,pdf] @ git+https://github.com/Sefaria/patot@v0.1.0"
```

- Core install (`pip install patot`) provides JSON segment loading and the Gemini embedding
  client/cache.
- `[chunking]` adds the statistical chunker (`PatotChunker`), which depends on
  `transformers`, `huggingface-hub`, `semantic-chunkers`, and `semantic-router`.
- `[pdf]` adds `patot.debug_report` for rendering chunking debug traces to PDF, which
  depends on `reportlab` and `python-bidi`.

## Usage

```python
from patot import ChunkerConfig, PatotChunker, load_segment_records_from_section

config = ChunkerConfig(debug=False)
chunker = PatotChunker(api_key="...", config=config)
result = chunker.chunk_segments(segment_records)
```

## Development

```bash
pip install -e ".[chunking,pdf]"
pip install pytest
pytest
```
