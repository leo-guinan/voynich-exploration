# Quick Start Guide

## Initial Setup

### 1. Install Dependencies

**System dependencies:**
```bash
# macOS
brew install poppler

# Linux
sudo apt-get install poppler-utils

# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
```

**Python dependencies:**
```bash
# Using conda (recommended)
conda env create -f environment/environment.yml
conda activate voynich

# Or using pip
pip install -r environment/requirements.txt
```

### 2. Extract Images from PDF

```bash
# Extract images (lossless)
pdfimages -all data/raw/yale/pdf/ms408.pdf data/raw/yale/images/page

# Convert to PNG
mogrify -format png data/raw/yale/images/*.ppm

# Rename to canonical folio names
python src/ingestion/pdf_to_images.py

# Verify integrity
python src/ingestion/verify_images.py
```

### 3. Set Up Metadata

Edit `data/raw/transcriptions/metadata/folios.csv` with actual folio metadata:
- folio: Canonical name (e.g., f001r, f001v)
- side: r (recto) or v (verso)
- section: botanical, astronomical, biological, pharmaceutical, recipes
- currier: A or B
- image_type: Type of illustration

### 4. Run Initial Analysis

Start Jupyter:
```bash
jupyter notebook
```

Run notebooks in order:
1. `00_exploration.ipynb` - Visual sanity checks
2. `01_layout_analysis.ipynb` - Layout statistics
3. `02_token_stats.ipynb` - Token frequency analysis
4. `03_compression.ipynb` - Compression baseline

## Next Steps

1. **Get EVA transcriptions**: Download from Voynich.nu and place in `data/raw/transcriptions/eva/`
2. **Document assumptions**: Update `docs/assumptions.md` as you work
3. **Track eliminated hypotheses**: Update `docs/eliminated_hypotheses.md` when you disprove something
4. **Take notes**: Use `docs/notes.md` for observations

## Design Principles (Remember!)

- **Images are first-class**: The manuscript images are authoritative
- **No flattening early**: Preserve all intermediate representations
- **Reversible transformations**: Every step should be undoable
- **Pristine dataset**: You should be able to delete all analysis code and still have complete data
- **Scientific archive**: This is research, not a competition

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

You're not trying to break the Voynich. You're trying to classify what type of system it is.

