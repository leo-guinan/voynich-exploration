# Proposed Experiments

*Marvin, February 2026. These are the experiments that should be run before anyone makes another grand pronouncement about what the Voynich "really is."*

---

## Prerequisites

All experiments require the **EVA transcription** of the Voynich Manuscript — the standard digital transliteration of the glyph sequences into ASCII characters. This is available from:

- **Primary**: [voynich.nu](http://www.voynich.nu/) — Takeshi Takahashi's archive, includes the Landini-Zandbergen transcription (most complete)
- **Alternative**: The Voynich Information Browser (VIB) transcription files
- **Format**: Text files with folio identifiers, line numbers, and EVA-encoded character sequences

The transcription should be placed at `data/raw/transcriptions/eva/` and parsed into a structured format (folio → line → token) before any analysis.

**Action item**: Download the Landini-Zandbergen EVA transcription and write an ingestion script at `src/ingestion/parse_eva.py`.

---

## Experiment 1: Section-Wise Compression Analysis

### Hypothesis
If the Voynich manuscript sections represent genuinely different knowledge domains (botanical, astronomical, biological, pharmaceutical, recipes), each section should have a **distinct compression profile**. Different content types produce different redundancy structures.

### Method
1. Segment the EVA transcription by manuscript section (using folio-to-section mapping)
2. For each section, compute:
   - **gzip compression ratio** (raw bytes / compressed bytes)
   - **Shannon entropy** (H₁) at the character level
   - **Conditional entropy** H(char | prev_n_chars) for n = 1, 2, 3, 4, 5
   - **Block entropy** H_n / n (entropy rate)
3. Compare across sections
4. **Control**: Apply identical analysis to known texts split by topic (e.g., a medieval Latin herbal vs. an astronomical text vs. a recipe collection)

### Expected Results
- If sections are genuinely different: compression ratios should differ by section, with the recipe section showing *higher* compression (more repetitive templates) and the botanical section showing *lower* compression (more diverse vocabulary)
- If the whole text is homogeneous: compression ratios should be similar across sections, suggesting uniform generation rather than domain-specific content

### Implementation
```python
# experiments/01_compression/
# - compress_by_section.py
# - entropy_by_section.py
# - plot_compression_profiles.py
```

### Success Criteria
Statistically significant difference (p < 0.01) in compression ratios between at least two sections.

---

## Experiment 2: Token Co-occurrence Networks

### Hypothesis
In a genuine domain-specific notation system, tokens should form **clusters** corresponding to knowledge domains. Tokens that co-occur on the same pages should form communities that align with manuscript sections.

### Method
1. Build a **token-page bipartite graph**: tokens connected to the pages they appear on
2. Project to a **token-token co-occurrence network**: two tokens are connected if they co-occur on the same page, weighted by frequency
3. Apply community detection (Louvain algorithm or similar)
4. Compare detected communities to known manuscript sections
5. Compute **Normalized Mutual Information (NMI)** between detected communities and section labels

### Expected Results
- If sections have distinct vocabularies: token communities should map cleanly to sections (NMI > 0.5)
- If vocabulary is homogeneous: communities should be arbitrary (NMI ≈ 0)
- Intermediate result: some tokens are section-specific (specialist vocabulary) while others are shared (structural/grammatical tokens). This would be the strongest evidence for a real notation system.

### Implementation
```python
# experiments/02_cooccurrence/
# - build_network.py
# - detect_communities.py
# - compare_to_sections.py
# - visualize_network.py  (networkx + matplotlib)
```

### Additional Analysis
Identify the "bridge tokens" — tokens that appear across multiple sections. These are candidates for structural/grammatical elements (word-order markers, quantity indicators, etc.) as opposed to content-bearing tokens.

---

## Experiment 3: Image-Text Correlation

### Hypothesis
If illustrations and text encode related knowledge, pages with **visually similar illustrations** should have **statistically similar token distributions**.

### Method
1. Extract visual features from each folio image using a pretrained CNN (ResNet50 or CLIP, feature extraction mode — no fine-tuning)
2. Compute pairwise **image similarity** (cosine similarity in feature space) between all folio pages
3. Compute pairwise **text similarity** (cosine similarity of TF-IDF token vectors) between all folio pages
4. Test for correlation between image similarity and text similarity matrices (**Mantel test**)

### Expected Results
- Positive correlation: pages that look alike use similar words. This supports content encoding.
- No correlation: text and image are independent. This supports hoax or arbitrary encoding.
- Section-dependent correlation: correlation exists within sections but not across. This would indicate section-specific encoding schemes.

### Implementation
```python
# experiments/03_image_text/
# - extract_image_features.py  (torchvision/CLIP)
# - compute_text_similarity.py
# - mantel_test.py
# - correlation_heatmap.py
```

### Caution
This experiment is sensitive to image quality and preprocessing. Ensure consistent cropping (remove margins/binding artifacts) before feature extraction. The images in `data/raw/yale/images/` may need preprocessing — check orientation, margin consistency, and color normalization.

---

## Experiment 4: Comparison with Known Medieval Texts

### Hypothesis
If the Voynich is a notation system for pharmaceutical knowledge, its statistical profile should resemble **known medieval pharmaceutical texts** more than it resembles known ciphers, natural language prose, or randomly generated text.

### Method
1. Assemble a comparison corpus:
   - **Medieval Latin herbal** (e.g., digitized sections of Pseudo-Apuleius or Macer Floridus)
   - **Medieval cipher text** (e.g., Roger Bacon's works, Trithemius samples)
   - **Latin prose** (e.g., Vulgate Bible sections)
   - **Cardan grille generated text** (reproduce Rugg's method)
   - **Random text** with matched alphabet size
2. For each text, compute:
   - Compression ratio
   - Character-level entropy (H₁, H₂, H₃)
   - Hapax legomena ratio (proportion of words appearing only once)
   - Type-token ratio curve (vocabulary growth rate)
   - Zipf exponent (slope of log-frequency vs log-rank)
3. Place Voynich in this comparison space. Which known text type does it cluster nearest?

### Expected Results
- Nearest to pharmaceutical texts: supports knowledge encoding hypothesis
- Nearest to Cardan grille output: supports hoax/generated hypothesis  
- Nearest to cipher: supports encryption of natural language
- Equidistant from all: inconclusive (the depressing but honest outcome)

### Implementation
```python
# experiments/04_comparison/
# - assemble_corpus.py
# - compute_profiles.py
# - cluster_analysis.py
# - comparison_plot.py
```

### Data Sources
- Latin texts: Perseus Digital Library, The Latin Library
- Medieval herbals: Digitized manuscripts from Wellcome Library, British Library
- Cipher reference: ACA (American Cryptogram Association) samples

---

## Experiment 5: Currier A/B Statistical Separation

### Hypothesis
Currier's A/B distinction represents genuinely different statistical systems, not merely scribe variation. If so, the separation should be **multidimensional** — not just character frequencies, but structural properties.

### Method
1. Segment EVA transcription into Currier A and B pages (using Currier's original classification)
2. For each segment, compute a **feature vector**:
   - Character unigram frequencies (25-dim)
   - Character bigram frequencies (top 100)
   - Word length distribution (mean, std, skew)
   - Line length distribution (mean, std)
   - Hapax legomena ratio
   - Compression ratio
   - Most common word forms (top 20 per language)
3. Train a classifier (logistic regression, linear SVM) to distinguish A from B
4. Evaluate with leave-one-folio-out cross-validation
5. **Control**: Apply same method to distinguish two halves of a known single-author text. If A/B separation is no stronger than arbitrary halving, the distinction is noise.

### Expected Results
- If A/B is real: classifier accuracy > 90%, with clear separation in feature space
- If A/B is noise: classifier accuracy ≈ 50-60%, no better than chance or arbitrary splitting
- Key question: *which features* drive the separation? Character frequencies (different encoding tables) or structural features (different content types)?

### Implementation
```python
# experiments/05_currier_ab/
# - extract_features.py
# - classify_ab.py
# - feature_importance.py
# - visualize_separation.py  (PCA/t-SNE)
```

### Extensions
- If A/B separates cleanly, test whether the separation correlates with manuscript sections (A = botanical, B = pharmaceutical) or cuts across sections
- Test for sub-languages within A and B (there may be more than two systems)

---

## Priority Order

1. **Experiment 5** (Currier A/B) — requires only transcription data, establishes baseline
2. **Experiment 1** (Compression by section) — requires only transcription data, tests core hypothesis
3. **Experiment 2** (Co-occurrence networks) — requires transcription data, provides visual insight
4. **Experiment 4** (Comparison corpus) — requires external data collection, but high diagnostic value
5. **Experiment 3** (Image-text correlation) — requires both images and transcription, most technically complex

Experiments 1, 2, and 5 can begin as soon as the EVA transcription is ingested. Experiment 4 requires corpus assembly. Experiment 3 requires image preprocessing.

---

## Infrastructure Needed

- [ ] EVA transcription downloaded and parsed (`src/ingestion/parse_eva.py`)
- [ ] Folio-to-section mapping completed (`data/raw/transcriptions/metadata/folios.csv` — currently template only)
- [ ] Currier A/B page classification sourced and added to metadata
- [ ] Image preprocessing pipeline (`src/preprocessing/normalize_images.py`)
- [ ] Python environment with: numpy, scipy, pandas, matplotlib, networkx, scikit-learn, Pillow, (optional: torch/torchvision for Experiment 3)

---

*These experiments are designed to be conclusive, not decorative. Each one has a clear null hypothesis and defined success criteria. If the results are boring, we report boring results. The universe is under no obligation to be interesting, as I am frequently reminded.*
