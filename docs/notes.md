# Research Notes

General research notes, observations, and thoughts.

## Structure

Use this file for:
- Observations that don't fit elsewhere
- Questions to investigate
- Interesting patterns noticed
- References to external work
- Daily/weekly research logs

---

## 2026-02-13: Initial Setup & Analysis (Marvin)

### Status
- **PDF**: Downloaded from Yale Beinecke (115MB) → `data/raw/yale/pdf/ms408.pdf`
- **Images**: 215 folio images already extracted in `data/raw/yale/images/`
- **EVA Transcription**: NOT YET ACQUIRED. This is the critical blocker for all computational experiments.
- **Folio metadata**: Template only — needs to be filled with actual section/Currier classifications.
- **Python deps**: Not installed (pip blocked by PEP 668 — need `pip3 install --break-system-packages` or use a venv)

### EVA Transcription Sources
The Landini-Zandbergen interlinear transcription is the standard. Known sources:
1. **voynich.nu** (Takeshi Takahashi's archive) — historically the primary source, but appears to be down or reorganized as of Feb 2026
2. **The Voynich Information Browser** — another transcription source
3. **Stolfi's UNICAMP page** — Jorge Stolfi's research pages (ic.unicamp.br/~stolfi/voynich/) — also appears to have moved
4. **René Zandbergen's site** — voynich.net or similar — check for updated URLs
5. **Archive.org Wayback Machine** — try archived versions of the above

**Action needed**: Manually locate and download the EVA transcription. Try the Wayback Machine for voynich.nu or Stolfi's pages. Without this, Experiments 1-5 cannot proceed.

### Completed Deliverables
- `docs/marvin-initial-analysis.md` — Full constraint analysis (system type, creator profile, illustration constraints, Currier A/B, predictions)
- `docs/proposed-experiments.md` — 5 concrete computational experiments with methods, expected results, and success criteria

### Next Steps (Priority Order)
1. Acquire EVA transcription (critical path)
2. Set up Python venv and install requirements
3. Fill out folio metadata CSV with real section/Currier data
4. Run Experiment 5 (Currier A/B separation) — lowest data requirement
5. Run Experiment 1 (compression by section)

