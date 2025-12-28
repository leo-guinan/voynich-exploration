"""
I/O utilities for Voynich research.

Design principle: All I/O operations should be reversible and preserve
data integrity.
"""

from pathlib import Path
import pandas as pd
from PIL import Image


def load_folio_metadata(metadata_dir: Path) -> pd.DataFrame:
    """
    Load folio metadata CSV.
    
    Args:
        metadata_dir: Path to metadata directory
    
    Returns:
        DataFrame with folio metadata
    """
    metadata_file = metadata_dir / 'folios.csv'
    
    if not metadata_file.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {metadata_file}\n"
            "Create data/raw/transcriptions/metadata/folios.csv"
        )
    
    return pd.read_csv(metadata_file, comment='#')


def load_folio_image(images_dir: Path, folio_name: str) -> Image.Image:
    """
    Load a folio image by name.
    
    Args:
        images_dir: Directory containing folio images
        folio_name: Folio name (e.g., 'f001r')
    
    Returns:
        PIL Image object
    """
    # Try PNG first, then JPEG
    for ext in ['.png', '.jpg', '.jpeg']:
        img_path = images_dir / f"{folio_name}{ext}"
        if img_path.exists():
            return Image.open(img_path)
    
    raise FileNotFoundError(f"Image not found for folio: {folio_name}")


def save_derived_data(data: pd.DataFrame, output_path: Path, **kwargs):
    """
    Save derived data with metadata.
    
    Args:
        data: DataFrame to save
        output_path: Output file path
        **kwargs: Additional arguments to pass to to_csv
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    data.to_csv(output_path, index=False, **kwargs)
    print(f"Saved derived data to: {output_path}")


def load_eva_transcriptions(eva_dir: Path) -> pd.DataFrame:
    """
    Load EVA transcriptions.
    
    Args:
        eva_dir: Directory containing EVA transcription files
    
    Returns:
        DataFrame with transcriptions
    """
    # TODO: Implement based on actual EVA file format
    # Expected format: folio, line_number, text
    raise NotImplementedError("EVA transcription loading not yet implemented")


def verify_data_integrity(data_dir: Path):
    """
    Verify integrity of raw data directory.
    
    Checks:
    - Required directories exist
    - Expected files are present
    - No corruption (via checksums if available)
    """
    data_dir = Path(data_dir)
    
    required_dirs = [
        'raw/yale/pdf',
        'raw/yale/images',
        'raw/transcriptions/metadata',
    ]
    
    missing = []
    for dir_path in required_dirs:
        full_path = data_dir / dir_path
        if not full_path.exists():
            missing.append(str(full_path))
    
    if missing:
        raise FileNotFoundError(
            f"Missing required directories:\n" + "\n".join(missing)
        )
    
    # Check for PDF
    pdf_path = data_dir / 'raw/yale/pdf/ms408.pdf'
    if not pdf_path.exists():
        raise FileNotFoundError(f"Manuscript PDF not found: {pdf_path}")
    
    print("✓ Data integrity check passed")

