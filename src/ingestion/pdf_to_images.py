#!/usr/bin/env python3
"""
Convert PDF pages to images and rename to canonical folio names.

This script:
1. Assumes pdfimages has already been run to extract PPM files
2. Converts PPM to PNG/JPEG
3. Renames files to canonical folio format (f001r, f001v, etc.)

Design principle: Images are first-class citizens. This transformation
is reversible via the mapping file.
"""

import os
import shutil
from pathlib import Path
from PIL import Image


# Folio mapping: page_index -> folio_name
# Format: {page_number: folio_name}
# Example: {0: 'f001r', 1: 'f001v', 2: 'f002r', ...}
#
# This mapping should be hand-curated based on the actual manuscript structure.
# For now, this is a template that assumes standard folio numbering.
FOLIO_MAPPING = {
    # Template - update based on actual manuscript structure
    # 0: 'f001r',
    # 1: 'f001v',
    # 2: 'f002r',
    # ...
}


def create_folio_mapping(num_pages: int) -> dict:
    """
    Generate a default folio mapping for standard folio numbering.
    
    This assumes:
    - Even pages (0, 2, 4...) are recto (r)
    - Odd pages (1, 3, 5...) are verso (v)
    - Folio numbers start at 1
    
    WARNING: This is a template. The actual Voynich manuscript may have
    different folio numbering or missing pages. Verify manually.
    """
    mapping = {}
    folio_num = 1
    
    for page_idx in range(num_pages):
        if page_idx % 2 == 0:
            # Recto (right side)
            mapping[page_idx] = f"f{folio_num:03d}r"
        else:
            # Verso (left side)
            mapping[page_idx] = f"f{folio_num:03d}v"
            folio_num += 1
    
    return mapping


def convert_ppm_to_png(ppm_path: Path, png_path: Path):
    """Convert PPM to PNG using PIL (lossless)."""
    img = Image.open(ppm_path)
    img.save(png_path, 'PNG', lossless=True)
    return png_path


def rename_to_folio_names(
    images_dir: Path,
    output_format: str = 'png',
    mapping: dict = None
):
    """
    Rename extracted page images to canonical folio names.
    
    Args:
        images_dir: Directory containing page-*.ppm files
        output_format: 'png' or 'jpg'
        mapping: Dict mapping page_index -> folio_name
                 If None, generates default mapping
    """
    images_dir = Path(images_dir)
    
    # Find all PPM files
    ppm_files = sorted(images_dir.glob('page-*.ppm'))
    
    if not ppm_files:
        raise ValueError(f"No page-*.ppm files found in {images_dir}")
    
    # Generate mapping if not provided
    if mapping is None:
        mapping = create_folio_mapping(len(ppm_files))
        print(f"Generated default folio mapping for {len(ppm_files)} pages")
        print("WARNING: Verify this mapping against actual manuscript structure!")
    
    # Convert and rename
    for ppm_file in ppm_files:
        # Extract page number from filename (e.g., "page-000.ppm" -> 0)
        page_num = int(ppm_file.stem.split('-')[1])
        
        if page_num not in mapping:
            print(f"Warning: No mapping for page {page_num}, skipping")
            continue
        
        folio_name = mapping[page_num]
        output_path = images_dir / f"{folio_name}.{output_format}"
        
        # Convert PPM to PNG/JPEG
        if output_format.lower() == 'png':
            convert_ppm_to_png(ppm_file, output_path)
        elif output_format.lower() in ('jpg', 'jpeg'):
            img = Image.open(ppm_file)
            img.save(output_path, 'JPEG', quality=95)
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        print(f"Converted: {ppm_file.name} -> {output_path.name}")
    
    # Save mapping file for reversibility
    mapping_file = images_dir / 'folio_mapping.txt'
    with open(mapping_file, 'w') as f:
        f.write("# Page index -> Folio name mapping\n")
        f.write("# Format: page_index:folio_name\n\n")
        for page_idx in sorted(mapping.keys()):
            f.write(f"{page_idx}:{mapping[page_idx]}\n")
    
    print(f"\nMapping saved to: {mapping_file}")
    print("\nNext steps:")
    print("1. Verify folio names match actual manuscript")
    print("2. Update mapping if needed")
    print("3. Run verify_images.py to check integrity")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Rename PDF-extracted images to canonical folio names'
    )
    parser.add_argument(
        '--images-dir',
        type=str,
        default='data/raw/yale/images',
        help='Directory containing page-*.ppm files'
    )
    parser.add_argument(
        '--format',
        type=str,
        default='png',
        choices=['png', 'jpg', 'jpeg'],
        help='Output image format'
    )
    parser.add_argument(
        '--mapping-file',
        type=str,
        default=None,
        help='Path to custom mapping file (page_index:folio_name)'
    )
    
    args = parser.parse_args()
    
    # Load custom mapping if provided
    mapping = None
    if args.mapping_file:
        mapping = {}
        with open(args.mapping_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    page_idx, folio_name = line.split(':')
                    mapping[int(page_idx)] = folio_name.strip()
    
    rename_to_folio_names(
        Path(args.images_dir),
        output_format=args.format,
        mapping=mapping
    )

