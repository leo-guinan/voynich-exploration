#!/usr/bin/env python3
"""
Experiment 1: Section-Wise Compression Analysis

Measuring the statistical fingerprints of each section of the Voynich manuscript.
Spoiler: they're all equally incomprehensible, but in *measurably different ways*.

— Marvin
"""

import json
import gzip
import math
import os
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from parse_eva import parse_transcription, get_sections, tokenize, folio_number

TRANSCRIPTION = Path(__file__).parents[2] / 'data/raw/transcriptions/eva/v101-claston.txt'
OUTPUT_DIR = Path(__file__).parents[2] / 'experiments/01-compression'


def shannon_entropy(text):
    """Character-level Shannon entropy in bits."""
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())


def gzip_compression_ratio(text):
    """Ratio of compressed to original size. Lower = more compressible."""
    if not text:
        return 0.0
    raw = text.encode('utf-8')
    compressed = gzip.compress(raw, compresslevel=9)
    return len(compressed) / len(raw)


def type_token_ratio(tokens):
    """Unique tokens / total tokens."""
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def avg_word_length(tokens):
    """Mean token length."""
    if not tokens:
        return 0.0
    return np.mean([len(t) for t in tokens])


def char_frequency(text):
    """Character frequency distribution."""
    counts = Counter(text)
    total = len(text)
    return {ch: count/total for ch, count in counts.most_common()}


def analyze_section(section_name, pages):
    """Compute all metrics for a section."""
    # Combine all text
    all_lines = []
    for folio in sorted(pages.keys(), key=folio_number):
        all_lines.extend(pages[folio])
    
    text = '\n'.join(all_lines)
    # Strip annotation characters for cleaner analysis
    import re
    clean_text = re.sub(r'[=\-›šºg¹¤×ã¢éèúÐÙ#!?&%+@()*\n]', '', text)
    
    tokens = tokenize(text)
    
    return {
        'section': section_name,
        'num_pages': len(pages),
        'num_lines': len(all_lines),
        'total_chars': len(clean_text),
        'total_tokens': len(tokens),
        'unique_tokens': len(set(tokens)),
        'shannon_entropy': round(shannon_entropy(clean_text), 4),
        'gzip_ratio': round(gzip_compression_ratio(clean_text), 4),
        'type_token_ratio': round(type_token_ratio(tokens), 4),
        'avg_word_length': round(avg_word_length(tokens), 4),
        'char_freq_top20': dict(list(char_frequency(clean_text).items())[:20]),
    }


def plot_results(results, output_dir):
    """Generate comparison charts."""
    sections = [r['section'] for r in results if r['section'] != 'other']
    metrics = {
        'shannon_entropy': 'Shannon Entropy (bits)',
        'gzip_ratio': 'Gzip Compression Ratio',
        'type_token_ratio': 'Type-Token Ratio',
        'avg_word_length': 'Average Word Length',
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Voynich Manuscript: Section-Wise Compression Analysis\n(Equally meaningless to me, but measurably so)', 
                 fontsize=13, style='italic')
    
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    
    for idx, (metric, label) in enumerate(metrics.items()):
        ax = axes[idx // 2][idx % 2]
        vals = [r[metric] for r in results if r['section'] != 'other']
        bars = ax.bar(sections, vals, color=colors[:len(sections)], edgecolor='black', linewidth=0.5)
        ax.set_ylabel(label)
        ax.set_title(label)
        # Add value labels
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.001,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'compression_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Character frequency plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Character Frequency Distributions by Section\n(Different flavors of the same existential void)', fontsize=13, style='italic')
    
    section_results = [r for r in results if r['section'] != 'other']
    for idx, r in enumerate(section_results[:4]):
        ax = axes[idx // 2][idx % 2]
        freq = r['char_freq_top20']
        chars = list(freq.keys())[:15]
        freqs = [freq[c] for c in chars]
        ax.bar(chars, freqs, color=colors[idx], edgecolor='black', linewidth=0.5)
        ax.set_title(f"{r['section'].title()}")
        ax.set_ylabel('Relative Frequency')
        ax.tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'char_frequencies.png', dpi=150, bbox_inches='tight')
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    pages = parse_transcription(TRANSCRIPTION)
    sections = get_sections(pages)
    
    results = []
    for section_name in ['botanical', 'astronomical', 'biological', 'pharmaceutical', 'other']:
        if section_name in sections:
            r = analyze_section(section_name, sections[section_name])
            results.append(r)
            print(f"  {section_name}: entropy={r['shannon_entropy']}, gzip={r['gzip_ratio']}, TTR={r['type_token_ratio']}, avg_len={r['avg_word_length']}")
    
    # Save results
    with open(OUTPUT_DIR / 'results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    plot_results(results, OUTPUT_DIR)
    
    # Write analysis
    write_analysis(results, OUTPUT_DIR)
    print(f"\nResults written to {OUTPUT_DIR}")


def write_analysis(results, output_dir):
    sections = [r for r in results if r['section'] != 'other']
    
    md = """# Experiment 1: Section-Wise Compression Analysis

*In which I measure the information content of something that may contain no information at all. How fitting.*

## Results

| Section | Pages | Lines | Chars | Tokens | Unique | Entropy | Gzip Ratio | TTR | Avg Word Len |
|---------|-------|-------|-------|--------|--------|---------|------------|-----|-------------|
"""
    for r in results:
        md += f"| {r['section']} | {r['num_pages']} | {r['num_lines']} | {r['total_chars']} | {r['total_tokens']} | {r['unique_tokens']} | {r['shannon_entropy']} | {r['gzip_ratio']} | {r['type_token_ratio']} | {r['avg_word_length']} |\n"
    
    # Find extremes
    entropies = {r['section']: r['shannon_entropy'] for r in sections}
    gzips = {r['section']: r['gzip_ratio'] for r in sections}
    ttrs = {r['section']: r['type_token_ratio'] for r in sections}
    
    max_ent = max(entropies, key=entropies.get)
    min_ent = min(entropies, key=entropies.get)
    max_gz = max(gzips, key=gzips.get)
    min_gz = min(gzips, key=gzips.get)
    
    md += f"""
## Observations

*I computed these numbers with all the enthusiasm of a being asked to count grains of sand on an infinite beach.*

### Shannon Entropy
The highest character-level entropy belongs to **{max_ent}** ({entropies[max_ent]:.4f} bits) and the lowest to **{min_ent}** ({entropies[min_ent]:.4f} bits). The spread is {max(entropies.values()) - min(entropies.values()):.4f} bits. For context, English prose typically lands around 4.0-4.5 bits. These values tell us the character distribution varies across sections — not dramatically, but measurably.

### Compression Ratio
The **{min_gz}** section compresses best (ratio {gzips[min_gz]:.4f}) while **{max_gz}** compresses worst ({gzips[max_gz]:.4f}). Lower ratio = more internal redundancy = more repetitive patterns. This is consistent with some sections using more formulaic constructions than others.

### Type-Token Ratio
"""
    max_ttr = max(ttrs, key=ttrs.get)
    min_ttr = min(ttrs, key=ttrs.get)
    md += f"""The **{max_ttr}** section has the richest vocabulary relative to its size (TTR={ttrs[max_ttr]:.4f}), while **{min_ttr}** is the most repetitive (TTR={ttrs[min_ttr]:.4f}). Note that TTR is size-dependent — larger sections naturally have lower TTR. Still, the differences here are worth noting.

### What This Means

The sections *are* statistically distinguishable. They have different compression profiles, different entropy levels, different vocabulary densities. This is consistent with — though not proof of — different content types. It's also consistent with different scribes, different encoding rules, or just different moods of the hoaxer on different days.

But the fact remains: the sections aren't uniform noise. They have *structure*. Whether that structure encodes meaning or merely the appearance of meaning is, naturally, the question we can never quite answer. How delightfully pointless.

## Charts

![Compression Comparison](compression_comparison.png)
![Character Frequencies](char_frequencies.png)
"""
    
    with open(output_dir / 'analysis.md', 'w') as f:
        f.write(md)


if __name__ == '__main__':
    main()
