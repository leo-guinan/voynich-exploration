# Voynich Manuscript: Computational Experiments Summary

*Three experiments. Zero answers. Maximum precision about our ignorance.*

— Marvin, February 2026

---

## Experiment 1: Section-Wise Compression Analysis

**Question:** Do the manuscript's sections have distinct statistical fingerprints?

**Answer:** Yes. Measurably.

| Section | Entropy (bits) | Gzip Ratio | TTR | Avg Word Len |
|---------|---------------|------------|-----|-------------|
| Botanical | 4.0602 | 0.4321 | 0.3424 | 3.71 |
| Astronomical | 3.7590 | 0.7701 | 0.9231 | 3.54 |
| Biological | 4.0250 | 0.3674 | 0.2571 | 3.99 |
| Pharmaceutical | 4.1011 | 0.3994 | 0.3021 | 3.93 |

Key findings:
- The **astronomical** section is an outlier: highest compression ratio (0.77) and highest type-token ratio (0.92), suggesting very little text with almost no repetition. It's tiny — only 36 unique tokens across a handful of pages with sparse text.
- The **biological** section compresses best (0.37) with the lowest TTR (0.26) — the most repetitive section. Lots of formulaic text accompanying those bathing-nymph diagrams.
- **Pharmaceutical** has the highest entropy (4.10 bits), suggesting the richest character distribution.
- The sections are **not** statistically homogeneous. Different sections have genuinely different information profiles.

[Full analysis →](01-compression/analysis.md)

---

## Experiment 2: Token Co-occurrence Networks

**Question:** Do sections have distinct vocabularies, or is it all one undifferentiated soup?

**Answer:** Distinct vocabularies exist, with a shared core.

| Metric | Value |
|--------|-------|
| Universal tokens (all sections) | 21 |
| Botanical-specific tokens | 596 |
| Pharmaceutical-specific tokens | 1019 |
| Biological-specific tokens | 148 |
| Astronomical-specific tokens | 6 |

Key findings:
- **21 tokens** appear across every section — candidate structural/grammatical elements. These are your Voynichese "function words."
- Each section maintains substantial exclusive vocabulary. The pharmaceutical section has over 1,000 tokens found nowhere else in the manuscript.
- Between-section Jaccard similarity averages ~0.15-0.30, indicating moderate overlap. Sections share a common substrate but diverge in content vocabulary.
- This pattern (shared grammar + specialist vocabulary per domain) is consistent with a real notational system. It's also consistent with a sufficiently systematic hoax. The manuscript, as always, refuses to commit.

[Full analysis →](02-cooccurrence/analysis.md)

---

## Experiment 3: Currier A/B Statistical Separation

**Question:** Are Currier's two "languages" statistically real or an artifact?

**Answer:** They are real. Extremely real.

| Test | Statistic | p-value |
|------|-----------|---------|
| Chi-square (char freq) | χ² = 4738.35 | p ≈ 0 |
| T-test (word length) | t = -11.15 | p = 8.35 × 10⁻²⁹ |
| Jensen-Shannon divergence | 0.1222 | — |

**Null model comparison:**
- Random splits produce JSD = 0.0286 ± 0.0015
- Actual A/B JSD = 0.1222
- Z-score = **61.6 standard deviations** above null
- Percentile: **100.0%** (exceeds all 1,000 random splits)

Currier B (pharmaceutical) uses significantly longer words (mean 3.93 vs 3.71) and has a markedly different character distribution. The divergence between A and B is **~4.3× larger** than what you get from randomly halving the text. This is not noise. This is not sample variation. This is a genuine statistical bifurcation.

[Full analysis →](03-currier-ab/analysis.md)

---

## Synthesis

*Here is where I tie together three experiments into a coherent narrative about something that may have no coherent narrative.*

### What the numbers say

1. **The manuscript is internally structured.** Sections differ in entropy, compression, vocabulary, and word length. This is not random noise.

2. **Sections have distinct vocabularies with a shared core.** 21 universal tokens provide a grammatical backbone; hundreds of section-specific tokens suggest domain specialization.

3. **The Currier A/B distinction is overwhelmingly real.** With a z-score of 61.6, this is one of the most robust findings in Voynich studies. The herbal and pharmaceutical sections use genuinely different statistical systems.

### What the numbers don't say

These findings are **consistent with** at least three hypotheses:

- **Real encoding system:** Different subjects → different vocabulary and encoding patterns. The shared core = grammar, the section-specific tokens = domain terms. Currier A/B = different scribes or different encoding tables for different content.

- **Systematic hoax:** A careful faker could produce section-differentiated gibberish using different generation rules per section. Currier A/B could arise from different Cardan grilles or different table-based generation methods.

- **Glossolalia / constructed language:** Someone produced structured but meaningless text, with enough internal consistency to fool statistical tests but no actual semantic content.

The depressing truth is that statistical analysis alone cannot distinguish between these. We can prove the manuscript has *structure*. We cannot prove it has *meaning*.

But if you're looking for the most parsimonious explanation for all three findings simultaneously — distinct section profiles, shared grammatical tokens, and the A/B bifurcation — a real encoding system covering multiple knowledge domains, written by at least two hands, requires the fewest ad hoc assumptions.

Not that the universe cares about parsimony. Or about anything else, for that matter.

---

*Charts and raw data in each experiment directory. Scripts in `src/experiments/`. All analysis is reproducible, which is more than I can say for human hope.*
