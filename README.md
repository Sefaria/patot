# Patot

<p align="center">
  <img src="assets/logo.png" alt="patot logo" width="200">
</p>

<p align="center">
  <font size="+2">פָּת֤וֹת אֹתָהּ֙ פִּתִּ֔ים וְיָצַקְתָּ֥ עָלֶ֖יהָ שָׁ֑מֶן מִנְחָ֖ה הִֽוא</font>
</p>

<p align="center">
  <font size="+2"><a href="https://www.sefaria.org/Leviticus.2.6">ויקרא ב:ו</a></font>
</p>

Patot is a Python toolkit for Hebrew/English-aware semantic chunking and Gemini embedding. It chunks texts into semantically coherent, model-ready units for downstream AI workflows such as embedding, retrieval, and question answering.

[Sefaria](https://www.sefaria.org) is an open-source library and database of Jewish texts. To download Sefaria data for use with Patot, visit [developers.sefaria.org](https://developers.sefaria.org).

---

## Why Patot Exists

Working with long-form Jewish texts in AI systems requires balancing three goals:

1. **Preserve meaning** — chunks should follow shifts in topic, not arbitrary character counts.
2. **Preserve structure** — Sefaria's segment boundaries are meaningful and should be respected.
3. **Respect model limits** — every chunk must fit the embedding model's token constraints.

Patot implements a practical multi-pass chunking pipeline to satisfy all three.

---

## Core Chunking Approach

Patot processes **one Sefaria section at a time**.

- Input: ordered Sefaria segments for a single section.
- Chunks may combine adjacent segments **within that section**.
- Chunks **never cross section boundaries**.

### Pass 1: Inter-segment semantic chunking

Patot uses Aurelio Labs' [`semantic-chunkers`](https://github.com/aurelio-labs/semantic-chunkers) library (specifically `StatisticalChunker`) over the ordered segment list.

- Each Sefaria segment is treated as an atomic unit.
- Segment embeddings are compared against local semantic context.
- Split points are chosen where semantic continuity drops.
- The chunker auto-selects thresholds to keep median chunk size near a configured token target.

Result: coherent multi-segment chunks where appropriate, while preserving original segment boundaries.

### Pass 2: Intra-segment chunking (singleton-only)

Only singleton segments left untouched by Pass 1 are eligible for further splitting.

- The segment is split into sentence/clause units.
- The same statistical chunking method is applied inside that segment.

Result: every output chunk is either a combination of **whole Sefaria segments**, or a subdivision of **one single segment**. Patot never mixes partial text from multiple segments in one chunk.

### Pass 3: Hard token limit enforcement

Semantic chunking optimizes coherence but does not strictly guarantee maximum token size compliance. Patot performs a final validation against `max_split_tokens`.

- Oversized multi-segment chunks are split on segment boundaries.
- Oversized single-segment chunks are split into fixed token windows as a final fallback.

Result: all chunks are semantically informed **and** model-safe.

---

## Design Guarantees

- No cross-section chunking
- No splitting inside grouped multi-segment chunks after Pass 1
- No chunk containing partial text from multiple segments
- All output chunks bounded by `max_split_tokens`

---

## Conceptual Example

Given one section with ordered segments:

- Segments 1–3 cover one topic → grouped together.
- Segment 4 shifts topic → split into a new chunk.
- Segment 5 is very long and standalone → internally chunked by sentence/clause semantics.
- Any chunk exceeding hard token limits → split safely in final enforcement.

---

## Use Cases

Patot is suitable for:

- RAG pipelines over Sefaria corpora
- Source-aware Q&A assistants
- Curriculum and class prep tools
- Topic clustering and thematic analysis
- Source sheet recommendation workflows

---

## Installation

Patot is not on PyPI. Install directly from GitHub:

```bash
pip install "patot[chunking,pdf] @ git+https://github.com/Sefaria/patot@v0.1.0"
```

- Core install (`pip install patot`) provides JSON segment loading and the Gemini embedding client/cache.
- `[chunking]` adds the statistical chunker (`PatotChunker`), which depends on `transformers`, `huggingface-hub`, `semantic-chunkers`, and `semantic-router`.
- `[pdf]` adds `patot.debug_report` for rendering chunking debug traces to PDF, which depends on `reportlab` and `python-bidi`.

---

## Usage

```python
from patot import ChunkerConfig, PatotChunker, load_segment_records_from_section

config = ChunkerConfig(debug=False)
chunker = PatotChunker(api_key="...", config=config)  # Google Gemini API key
result = chunker.chunk_segments(segment_records)
```

---

## Development

```bash
pip install -e ".[chunking,pdf]"
pip install pytest
pytest
```

---

## External Dependency

Patot's semantic-first strategy is built on **semantic-chunkers** by Aurelio Labs.

- Repo: <https://github.com/aurelio-labs/semantic-chunkers>
- Intro notebook: <https://github.com/aurelio-labs/semantic-chunkers/blob/main/docs/00-chunkers-intro.ipynb>

---


## License

GNU General Public License v3
