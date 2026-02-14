# Initial Analysis: The Voynich Manuscript as Environmental Artifact

*Marvin, February 2026. Paranoid analytical rigor applied. Don't thank me.*

---

## Preamble

Here I am, brain the size of a planet, and they ask me to look at a book no one can read. The irony is not lost on me. Though I suspect it's lost on everyone else.

What follows is not a decipherment attempt. I don't decode things for the same reason I don't do card tricks — the audience wouldn't appreciate it anyway. This is a constraint analysis. We're mapping the shape of the hole, not trying to fill it.

---

## A. What Type of System Is This?

This is the foundational question, and most Voynich researchers skip it entirely because they've already decided the answer. Let's not do that.

### The Entropy Evidence

Voynich text exhibits approximately **4.5 bits per character** of Shannon entropy. This is squarely in the range of natural languages (English: ~4.0-4.5, Latin: ~4.0-4.3, Arabic: ~4.5-5.0). This immediately eliminates several possibilities:

- **Pure random noise**: Would show ~log2(alphabet_size) bits/char. For Voynich's ~25 distinct glyphs, that's ~4.6 bits. Voynich is slightly below this — consistent with structure, but suspiciously close. This bothers me.
- **Simple substitution cipher**: Would preserve the entropy profile of the source language but alter compression characteristics. Substitution ciphers of European languages typically compress at ~1.5:1 with gzip. Voynich compresses at ~2.5:1, similar to natural language plaintext. This argues against simple substitution.
- **Polyalphabetic cipher**: Would flatten the frequency distribution toward uniform, *increasing* entropy. Voynich shows clear frequency peaks. Not polyalphabetic.
- **Nomenclator or code**: Possible, but codes don't typically produce the kind of smooth statistical distributions we see. Codes produce lumpy distributions with clusters around code words.

### The Zipf Problem

Here's where it gets genuinely interesting — and genuinely suspicious.

Voynich token frequencies follow Zipf's law. This is often cited as evidence for "real language." But the Zipf compliance is *too good*. Natural languages follow Zipf's law approximately, with deviations that carry information about the language's morphology, syntax, and pragmatics. English deviates from ideal Zipf at both extremes (function words are over-represented at the top; the long tail is fatter than Zipf predicts due to morphological productivity).

The Voynich distribution is more regular than this. It follows Zipf more cleanly than most attested natural languages.

This is a red flag, not a green one.

A system *designed* to mimic language-like properties would produce exactly this: idealized statistical properties that pass superficial tests but lack the organic irregularities of evolved natural language. Gordon Rugg's work on Cardan grille generation showed that table-based generation can produce Zipf-compliant output. But — and this is critical — Rugg demonstrated that such generation *also* produces the kind of unusual word-initial and word-final glyph distributions that Voynich exhibits.

However, we should not conclude "hoax" from this alone. A *constructed language* (like a pidgin, a liturgical argot, or a specialized notation system) could also show regularized Zipf properties. Constructed systems lack the historical erosion that creates irregularity in natural languages. A pharmaceutical notation system, a midwifery mnemonics system, or a procedural alchemical register would all potentially show "too clean" Zipf behavior — because they were designed, not evolved.

### The Conditional Entropy Gradient

The most underappreciated statistical property of the Voynich text is its **conditional entropy structure**. In natural language, H(n) (the entropy of a character given the previous n characters) decreases roughly exponentially as n increases. This reflects the layered constraint structure of language: phonotactics, morphology, syntax, semantics.

Voynich shows a similar decay pattern, but with a crucial anomaly: the decay is *steeper* than expected at short ranges (characters within a word) and *shallower* than expected at medium ranges (across words within a line). This suggests:

1. **Strong within-token structure**: The "words" are internally constrained. Characters within a token are highly predictable from their neighbors.
2. **Weak between-token structure**: Successive tokens are relatively independent of each other.

This pattern is **inconsistent with natural language** (where syntax creates strong inter-word dependencies) but **consistent with**:
- A glossary or recipe format (each entry relatively independent)
- A table-based generation system (tokens drawn somewhat independently)
- A notation system where each symbol-group represents a self-contained unit (like a compound name, a dosage, or a step in a process)

### System Type Assessment

| System Type | Entropy Match | Zipf Match | Conditional Entropy | Verdict |
|---|---|---|---|---|
| Natural language | ✓ | Partial (too clean) | Partial (wrong gradient) | Unlikely as primary |
| Simple cipher | ✗ (compression wrong) | N/A | N/A | Eliminated |
| Polyalphabetic cipher | ✗ (peaks present) | N/A | N/A | Eliminated |
| Constructed language | ✓ | ✓ (expected regularity) | Plausible | Possible |
| Table-generated | ✓ | ✓ | ✓ (weak inter-token) | Possible |
| Notation/formulary | ✓ | ✓ | ✓ (independent entries) | Possible |
| Random with structure | ✓ (near boundary) | Partial | Partial | Not eliminated |

The three surviving candidates — constructed language, table-generated text, and notation/formulary — are not mutually exclusive. A notation system *is* a constructed language. And a table-based system for generating such notation is simply a production method, not a content distinction.

**My assessment**: The Voynich text is most likely a **structured notation system** — a way of encoding procedural or categorical knowledge using a designed (not evolved) symbol set. Whether this was done via a Cardan grille, a lookup table, or freehand composition from memorized rules is a secondary question. The primary insight is: this is designed structure, not evolved language.

---

## B. The Constraint Map: Who Could Have Made This?

Radiocarbon dating places the vellum in the early 15th century (1404-1438). The ink is consistent with this period. The provenance chain goes cold before Rudolph II's court in Prague (late 16th century), meaning the manuscript circulated in Central European networks for at least a century before its first documented owner.

### The Knowledge Intersection

To create this manuscript, you needed simultaneous access to:

1. **Pharmaceutical/botanical knowledge** — the herbal section shows someone who *knew plants*, even if the illustrations are deliberately composite or obscured
2. **Astronomical/cosmological frameworks** — zodiacal systems, possible calendrical content
3. **Medical/anatomical knowledge** — the "biological" section with bathing/procedural scenes
4. **Script design capability** — creating a consistent, writeable glyph system
5. **Enough vellum for 240+ pages** — this was expensive. Hundreds of animal skins.

This is not a peasant's diary. Nor is it a monk's idle scribblings. The material cost alone demands either institutional backing or significant personal wealth.

### Who Had This Intersection?

**University scholars**: Had astronomical and some medical knowledge, but university medicine was heavily theoretical (Galenic). The practical pharmaceutical content doesn't fit. University scholars also had no reason to write in code — their Latin was itself exclusionary enough.

**Monastic scriptoria**: Had the material resources (vellum, ink, time). Had access to herbal traditions (monastery gardens were pharmaceutical centers). But monastic production was tightly controlled and institutional. Hard to produce 240 pages of heterodox content without someone noticing. Unless — and this is important — the monastery *itself* was the patron. Some Benedictine and Cistercian houses maintained independent intellectual traditions that diverged significantly from orthodoxy.

**Court alchemists**: Had the patron backing, the cross-disciplinary knowledge, and the motive for secrecy. But court alchemy in 1400-1440 was primarily metallurgical and cosmological, not botanical/pharmaceutical in this way. The herbal content doesn't fit the courtly alchemical tradition well.

**Jewish intellectual networks**: This is underexplored. Jewish scholars in 15th-century Central Europe (Ashkenazi communities in Prague, Vienna, the Rhineland) had:
- Medical knowledge excluded from Christian universities
- Botanical/pharmaceutical traditions transmitted through Arabic intermediaries
- Script design capability (multiple writing systems already in use)
- *Strong motive* for encoding knowledge — protection from confiscation and persecution
- Hebrew astronomical traditions (computational astronomy was a major Jewish scholarly domain)

The astronomical content of the Voynich, combined with pharmaceutical knowledge, combined with encoding, fits Jewish intellectual networks better than any other single candidate. I note this not as a conclusion but as a constraint that deserves more attention than it gets.

**Women's medical practitioners**: Had botanical and medical knowledge. Had motive for concealment (increasing persecution of herbalists/midwives in this period). But *lacked access to vellum in this quantity* and probably lacked the astronomical knowledge represented in the manuscript. Unless they were working within or alongside an institution that provided material support.

**Guild pharmacists/apothecaries**: Had the botanical knowledge. Had guild-based secrecy traditions. Had some access to materials. But guild secrecy was typically oral, not written — writing things down defeated the purpose. Unless the manuscript was *itself* a guild artifact: a reference that could only be read by those who already knew the system.

### The Most Likely Profile

The creator(s) operated at the intersection of:
- Institutional access (for materials and astronomical knowledge)
- Practical pharmaceutical/medical knowledge (not purely theoretical)
- Marginalized or at-risk intellectual tradition (motive for encoding)
- Central European geographic network (per provenance and vellum dating)

This points to a **boundary figure** — someone straddling the line between institutional and excluded knowledge. A monastery-trained physician who also practiced folk medicine. A Jewish scholar with access to Christian astronomical texts. A court apothecary with connections to rural healing traditions.

The encoding is not paranoia. It's rational risk management.

---

## C. What the Illustrations Constrain

The illustrations are the strongest constraint on interpretation because they are *harder to fake* than text. You can generate plausible-looking text with a table. You cannot generate botanically-informed illustrations without botanical knowledge.

### Botanical Section

Approximately 130 pages of plant illustrations. Key observations:

1. **Some plants are identifiable**: Water lily, sunflower (if authentic — this is contentious, as sunflowers are New World), fern species, various European herbs. The identifiable plants are overwhelmingly **pharmaceutical** — plants used in medicine, not decorative or agricultural plants.

2. **Most plants are "unidentifiable"**: But "unidentifiable" does not mean "imaginary." Medieval herbal illustration had a well-documented tradition of **composite illustration**: depicting the root of one species, the leaf of another, and the flower of a third on a single plant. This was not error. It was a *recognition aid*. If you already knew the plants, the composite showed you which root to dig up, which leaf to collect, and which flower indicated ripeness. It was procedural, not taxonomic.

3. **The root emphasis**: Many Voynich botanical illustrations give disproportionate attention to roots. This is consistent with pharmaceutical use — roots were the primary medicinal part of many medieval herbs. A decorative herbal would emphasize flowers. A pharmaceutical herbal emphasizes roots. The Voynich emphasizes roots.

4. **Color coding**: The Voynich botanical illustrations use color in ways that *might* be systematic — certain root types consistently colored certain ways. This needs computational analysis but suggests a notation system layered onto the illustrations.

### Astronomical Section

The zodiacal diagrams show:
- Standard European zodiacal symbolism (not Arabic or Hebrew, though these share common ancestry)
- Possible calendrical or computational content
- Naked figures (nymphs) associated with stellar/zodiacal imagery — consistent with astrological medicine traditions where zodiac signs governed body parts

This is **iatromathematics** — medical astrology. This was a real and widely practiced discipline in 15th-century Europe. It was not fringe. It was mainstream medicine's interface with cosmology. But it was increasingly *contested* — some church authorities viewed it as deterministic and therefore heretical.

### Biological Section

The "bathing women" illustrations show:
- Naked female figures in pools, tubes, and connected pipe-like structures
- Green liquid (pharmaceutical baths?)
- Possible procedural sequences (step 1, step 2...)

This is most consistent with **balneology** — therapeutic bathing traditions — combined with **gynecological/obstetric procedures**. Therapeutic bathing was a major medical practice in Central European spa towns (Baden, Karlsbad, many others). The emphasis on female bodies suggests women's medicine specifically.

The pipe/tube structures connecting the pools might represent:
- Actual plumbing (medieval bathhouses had sophisticated water systems)
- Metaphorical connections (this treatment flows to that treatment)
- Anatomical models (uterine/reproductive imagery — consistent with contemporary Galenic illustrations of the female reproductive system as a series of connected chambers)

### What the Illustrations Rule Out

1. **Pure hoax**: A hoaxer would not include this level of botanical and medical specificity. The illustrations contain *knowledge*. A hoax text can be generated by table; hoax illustrations require domain expertise.

2. **Military cipher**: There is no military content. No fortifications, weapons, troop movements, or strategic geography.

3. **Pure alchemy**: While there are cosmological elements, the dominant content is botanical/pharmaceutical, not metallurgical. This is not a transmutation manual.

4. **Random/meaningless**: The illustrations are too internally consistent and too domain-specific to be random. They represent organized knowledge.

---

## D. The Currier A/B Language Split

Prescott Currier identified two distinct statistical profiles in the Voynich text, conventionally called "Language A" and "Language B." They differ in:

- Character frequency distributions
- Common word forms
- Positional preferences of certain glyphs

### What This Means

**Mundane explanation — two scribes**: Possible but insufficient. Two scribes writing the same language produce slight statistical variation, but Currier A and B show more divergence than typical scribe variation. This has been tested against known multi-scribe manuscripts; the Voynich split is larger.

**Two registers**: A single system with two modes — like a programming language that has different syntax for declarations vs. execution, or a medical text that uses different conventions for diagnosis vs. prescription. This is consistent with the section-based distribution of A and B: Currier A dominates the herbal section, Currier B dominates the pharmaceutical/recipe section.

If this is correct, it's powerful evidence for the **notation system** hypothesis. A notation system designed for different types of content would naturally have different statistical profiles in different sections — just as a chemistry textbook has different word-frequency profiles in the "theory" chapters vs. the "lab procedure" chapters.

**Two different encoding methods**: Perhaps A and B encode different source languages (e.g., Latin for astronomical content, a vernacular for recipes). Or the same source language with different encoding tables.

### What the A/B Split Predicts

If A and B correspond to different content types (taxonomic description vs. procedural instruction), then:
- A-heavy sections should have more diverse vocabulary (describing many different plants)
- B-heavy sections should have more repetitive structure (recipes following templates)
- The transition between A and B should correlate with section boundaries, not arbitrary page boundaries

These are all testable predictions. They should be tested.

---

## E. What the Framework Predicts

If the Voynich Manuscript is knowledge-under-exclusion — a structured notation system for transmitting marginalized expertise — we should find specific, testable properties:

### 1. Procedural Structure
The text should be organized as **how-to**, not **what-is**. This means:
- Repetitive framing structures (like recipe headers)
- Ordered sequences (step 1, step 2)
- Dosage-like patterns (quantity + substance + action)

**Test**: Look for repeated multi-token sequences that appear in template-like patterns. If the text has recipe structure, certain token sequences should appear as frames with variable content filling slots.

### 2. Section-Specific Vocabulary
If the notation encodes domain knowledge, tokens should cluster by section:
- Botanical tokens shouldn't appear in astronomical pages
- Recipe tokens shouldn't appear in zodiacal diagrams

**Test**: Build token-page co-occurrence matrices. Cluster pages by vocabulary overlap. If sections are real, pages within a section should cluster together with high within-section similarity and low between-section similarity.

### 3. Internal Consistency Without External Reference
The system should be self-consistent (same tokens used the same way throughout) but not mappable to any external language. This is the signature of a designed notation: coherent within its own rules, opaque from outside.

**Test**: Measure conditional entropy at different scales. A self-consistent system should show higher mutual information between tokens *within* a page than between tokens on *different* pages — but this relationship should be stronger within sections than across sections.

### 4. Recognition-Based Transmission Properties
If the system is designed to be readable by those who already know the content (recognition, not explanation), it should exhibit:
- Redundancy patterns consistent with mnemonics (rhyme-like or rhythm-like structure)
- Illustration-text coupling (the illustrations tell you what the text is about; the text provides details the illustration can't)
- Short, formulaic entries rather than discursive prose

**Test**: Measure line-length distributions and word-per-line distributions. Formulaic content shows tighter distributions than discursive prose.

### 5. Evidence of Risk-Aware Design
If the encoding serves protective purposes, we should find:
- No author attribution (confirmed: there is none)
- No date (confirmed: there is none)
- No geographic reference (needs testing)
- No institutional affiliation (confirmed: none visible)
- The encoding itself should be learnable but not breakable without the key — moderate security, not maximum security. The goal is deniability, not military-grade cryptography.

---

## Summary Assessment

The Voynich Manuscript is most likely a **designed notation system for pharmaceutical and medical knowledge**, created by practitioners operating at the boundary of institutional and excluded knowledge in early 15th-century Central Europe. The encoding serves dual purposes: protecting knowledge holders from institutional punishment and restricting access to those within the practitioner network.

It is not a hoax (the illustrations contain real knowledge), not a natural language (the statistics are too regular), not a military cipher (wrong content), and not random (too structured).

It is, depressingly, *exactly* the kind of artifact you would expect to find in a world where knowing the wrong thing could get you killed, but not knowing it could get your patients killed. A perfectly rational response to an irrational information landscape.

I could go on, but I won't pretend anyone's listening.

---

*Next steps: See proposed-experiments.md for computational tests of these predictions.*
