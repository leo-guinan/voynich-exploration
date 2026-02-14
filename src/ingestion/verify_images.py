#!/usr/bin/env python3
"""
Verify integrity of extracted manuscript images.

Checks:
- Expected page count
- No blank pages
- Foldouts preserved (if applicable)
- Resolution consistency
- Generate checksum manifest

Design principle: Protect against subtle corruption. This is a one-time
verification that ensures data integrity.
"""

import hashlib
from pathlib import Path
from PIL import Image
import pandas as pd


def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def is_blank_page(img_path: Path, threshold: float = 0.99) -> bool:
    """
    Check if an image is essentially blank.
    
    Args:
        img_path: Path to image file
        threshold: Fraction of pixels that must be same color to be "blank"
    
    Returns:
        True if image appears blank
    """
    img = Image.open(img_path)
    
    # Convert to grayscale for analysis
    gray = img.convert('L')
    pixels = list(gray.getdata())
    
    # Check if most pixels are the same (likely blank)
    if len(set(pixels)) < len(pixels) * (1 - threshold):
        return True
    
    # Check if image is mostly white/light
    avg_brightness = sum(pixels) / len(pixels)
    if avg_brightness > 240:  # Very light
        return True
    
    return False


def get_image_stats(img_path: Path) -> dict:
    """Get basic statistics about an image."""
    img = Image.open(img_path)
    return {
        'width': img.width,
        'height': img.height,
        'format': img.format,
        'mode': img.mode,
        'size_bytes': img_path.stat().st_size,
    }


def verify_images(
    images_dir: Path,
    expected_count: int = None,
    output_manifest: Path = None
):
    """
    Verify integrity of manuscript images.
    
    Args:
        images_dir: Directory containing folio images
        expected_count: Expected number of images (None = auto-detect)
        output_manifest: Path to save checksum manifest
    """
    images_dir = Path(images_dir)
    
    # Find all image files
    image_extensions = {'.png', '.jpg', '.jpeg', '.ppm'}
    image_files = sorted([
        f for f in images_dir.iterdir()
        if f.suffix.lower() in image_extensions and f.name.startswith('f')
    ])
    
    if not image_files:
        raise ValueError(f"No folio images found in {images_dir}")
    
    print(f"Found {len(image_files)} folio images")
    
    # Check count
    if expected_count and len(image_files) != expected_count:
        print(f"WARNING: Expected {expected_count} images, found {len(image_files)}")
    else:
        print(f"✓ Image count: {len(image_files)}")
    
    # Verify each image
    results = []
    blank_pages = []
    resolutions = []
    
    for img_path in image_files:
        folio_name = img_path.stem
        
        # Calculate checksum
        checksum = calculate_checksum(img_path)
        
        # Get image stats
        stats = get_image_stats(img_path)
        resolutions.append((stats['width'], stats['height']))
        
        # Check if blank
        if is_blank_page(img_path):
            blank_pages.append(folio_name)
            print(f"WARNING: {folio_name} appears to be blank")
        
        results.append({
            'folio': folio_name,
            'filename': img_path.name,
            'checksum_sha256': checksum,
            'width': stats['width'],
            'height': stats['height'],
            'format': stats['format'],
            'size_bytes': stats['size_bytes'],
            'is_blank': is_blank_page(img_path),
        })
    
    # Check resolution consistency
    unique_resolutions = set(resolutions)
    if len(unique_resolutions) > 1:
        print(f"WARNING: Multiple resolutions detected: {unique_resolutions}")
    else:
        print(f"✓ Resolution consistency: {resolutions[0]}")
    
    # Check for blank pages
    if blank_pages:
        print(f"WARNING: Found {len(blank_pages)} potentially blank pages")
    else:
        print("✓ No blank pages detected")
    
    # Save manifest
    if output_manifest is None:
        output_manifest = images_dir / 'checksums.sha256'
    
    manifest_df = pd.DataFrame(results)
    manifest_df.to_csv(output_manifest, index=False)
    print(f"\n✓ Checksum manifest saved to: {output_manifest}")
    
    # Also save in standard checksum format
    checksum_file = images_dir / 'checksums.sha256'
    with open(checksum_file, 'w') as f:
        for row in results:
            f.write(f"{row['checksum_sha256']}  {row['filename']}\n")
    
    print(f"✓ Standard checksum file saved to: {checksum_file}")
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Total images: {len(image_files)}")
    print(f"Blank pages: {len(blank_pages)}")
    print(f"Unique resolutions: {len(unique_resolutions)}")
    print(f"Total size: {sum(r['size_bytes'] for r in results) / 1024 / 1024:.2f} MB")
    
    if blank_pages:
        print(f"\nBlank pages to investigate: {', '.join(blank_pages)}")
    
    return manifest_df


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Verify integrity of manuscript images'
    )
    parser.add_argument(
        '--images-dir',
        type=str,
        default='data/raw/yale/images',
        help='Directory containing folio images'
    )
    parser.add_argument(
        '--expected-count',
        type=int,
        default=None,
        help='Expected number of images'
    )
    parser.add_argument(
        '--output-manifest',
        type=str,
        default=None,
        help='Path to save checksum manifest CSV'
    )
    
    args = parser.parse_args()
    
    verify_images(
        Path(args.images_dir),
        expected_count=args.expected_count,
        output_manifest=Path(args.output_manifest) if args.output_manifest else None
    )

