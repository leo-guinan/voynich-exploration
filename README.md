# Voynich Manuscript Research Repository

## Introduction: Mapping Knowledge by Its Constraints

The Voynich Manuscript has resisted more than a century of attempts at decipherment. It has been treated as a cipher, a hoax, a lost language, or a puzzle awaiting the right key. Each of these approaches assumes that the manuscript is the primary object of inquiry—that meaning is contained within it, and that progress depends on extracting that meaning more effectively.

This project begins from a different premise.

We do not treat the Voynich Manuscript as a message to be decoded, but as an environmental artifact—a structured residue left behind by the information landscape that produced it. Rather than asking what the manuscript means, we ask what kind of world would rationally generate an object with these properties, and what constraints shaped its form.

In this view, the Voynich Manuscript is not anomalous because it is unintelligible. It is anomalous because it is coherent without being legible. That coherence suggests design, but not the design of a text meant to inform a general reader. It suggests an artifact optimized to survive, transmit, and stabilize certain kinds of knowledge under conditions where explicit explanation was unsafe, illegitimate, or impossible.

### Knowledge Does Not Disappear Under Exclusion

Across history, when knowledge is systematically excluded from formal institutions—when it cannot be taught openly, cited authoritatively, or transmitted through sanctioned channels—it does not vanish. Instead, it changes shape.

Excluded knowledge tends to become:

- **procedural** rather than propositional
- **diagrammatic** rather than discursive
- **anonymized** rather than authored
- **cyclical** rather than linear
- **recognitional** rather than explanatory

These are not aesthetic choices. They are survival strategies.

The late medieval period in Central Europe was characterized by sharply defined legitimacy filters. Universities, monasteries, courts, guilds, and the Church each governed what counted as "knowledge," who could produce it, and how it could circulate. Domains that fell outside these filters—especially embodied, domestic, medical, and process-oriented knowledge—were often practiced, relied upon, and transmitted, but rarely legitimized in canonical texts.

The absence of such knowledge from formal records should not be read as absence of the knowledge itself. It should be read as a signal about the control networks that filtered it out.

### From Text Analysis to Semantic Cartography

This project proposes a shift from textual interpretation to semantic cartography.

Rather than mapping words to meanings, we map:

- knowledge domains
- control networks
- transmission modes
- risk profiles

We ask:

- Who was permitted to hold this knowledge?
- Through which institutions could it move?
- What punishments accompanied misuse or exposure?
- What forms of representation were safe, tolerated, or invisible?

The result is a semantic map of the information landscape of early 15th-century Europe—a map colored not by topic, but by governance. Each region represents not just what was known, but how permission, risk, and legitimacy shaped its expression.

In such a map, the most interesting regions are not those densely populated with texts, but those where knowledge was real, necessary, and yet sparsely represented in explicit form. These gaps are not mysteries. They are structural shadows.

### The Voynich Manuscript as a Probe, Not a Puzzle

Within this framework, the Voynich Manuscript functions as a probe. Its unusual properties—diagrammatic density, procedural repetition, resistance to translation, lack of attribution, and apparent internal consistency—can be used to stress-test the semantic map.

Where the manuscript does not fit comfortably within established domains, we do not force an interpretation. Instead, we treat that misfit as evidence of tension between knowledge and control.

If the map is accurate, the Voynich Manuscript should not appear as an isolated anomaly. It should cluster near other shadow artifacts: works shaped by exclusion, risk, and the need for recognition-based transmission rather than explanation.

### Why This Strategy Matters

This approach reframes the Voynich Manuscript from an unsolved problem into a diagnostic instrument. It allows us to reason about absence, opacity, and illegibility without resorting to mysticism or speculation. It also creates a general framework for understanding how knowledge behaves under constraint—one that applies beyond the medieval world, and beyond this single manuscript.

Ultimately, this project is not about solving the Voynich Manuscript.

It is about understanding how worlds shape the knowledge they allow to exist—and how that knowledge leaves traces even when it is denied a name.

---

## Design Philosophy

This repository follows strict scientific archive principles:

- **Images are first-class citizens**: The manuscript images are the authoritative source. All text is derived, not original.
- **No flattening early**: Preserve all intermediate representations. Every transformation is reversible.
- **Pristine dataset**: You should be able to delete all analysis code and still have a complete, untouched dataset.
- **Scientific archive, not Kaggle project**: This is a research archive, not a competition entry.

## Repository Structure

```
voynich/
├── data/
│   ├── raw/          # Sacred - never overwrite
│   ├── processed/    # Reversible transformations
│   └── derived/      # Analysis outputs
├── notebooks/        # Exploratory analysis
├── src/             # Reusable code
├── experiments/      # Experimental runs
└── docs/            # Documentation and hypotheses
```

## Getting Started

### 1. Extract Images from PDF

```bash
# Extract images (lossless)
pdfimages -all data/raw/yale/pdf/ms408.pdf data/raw/yale/images/page

# Convert to PNG
mogrify -format png data/raw/yale/images/*.ppm

# Run canonical naming script
python src/ingestion/pdf_to_images.py

# Verify integrity
python src/ingestion/verify_images.py
```

### 2. Initial Analysis

Start with the exploration notebooks in order:
- `00_exploration.ipynb` - Visual sanity checks
- `01_layout_analysis.ipynb` - Layout statistics
- `02_token_stats.ipynb` - Token frequency analysis
- `03_compression.ipynb` - Compression baseline

## Guardrails

**Don't start with:**
- Translation attempts
- Cipher solvers
- Deep neural models
- "This glyph means X" assumptions

**Do start with:**
- Constraints and invariants
- What cannot be true
- Classification of system type

We're not trying to break the Voynich. We're trying to classify what type of system it is, and what constraints shaped its form. This classification serves the larger goal of semantic cartography—mapping the information landscape that produced artifacts like this manuscript.

## Documentation

- `docs/assumptions.md` - Working assumptions
- `docs/eliminated_hypotheses.md` - Disproven hypotheses (critical!)
- `docs/notes.md` - Research notes

## License

[Add your license here]

