#!/usr/bin/env python3
"""
Experiment 2: Token Co-occurrence Networks

Building a map of which tokens hang out together. Like a social network
for meaningless symbols. At least *they* have connections.

— Marvin
"""

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from itertools import combinations

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from parse_eva import parse_transcription, get_sections, tokenize, folio_number

TRANSCRIPTION = Path(__file__).parents[2] / 'data/raw/transcriptions/eva/v101-claston.txt'
OUTPUT_DIR = Path(__file__).parents[2] / 'experiments/02-cooccurrence'


def jaccard_similarity(set_a, set_b):
    if not set_a and not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def build_page_token_sets(pages):
    """For each page, get the set of tokens."""
    page_tokens = {}
    for folio, lines in pages.items():
        text = '\n'.join(lines)
        tokens = tokenize(text)
        if tokens:
            page_tokens[folio] = set(tokens)
    return page_tokens


def build_cooccurrence(page_tokens, top_n=100):
    """Build token co-occurrence from page-level co-occurrence."""
    # Get most common tokens
    all_tokens = Counter()
    for tokens in page_tokens.values():
        all_tokens.update(tokens)
    
    top_tokens = [t for t, _ in all_tokens.most_common(top_n)]
    top_set = set(top_tokens)
    
    cooccurrence = Counter()
    for folio, tokens in page_tokens.items():
        page_top = tokens & top_set
        for a, b in combinations(sorted(page_top), 2):
            cooccurrence[(a, b)] += 1
    
    return top_tokens, cooccurrence


def section_token_analysis(sections):
    """Analyze within/between section token overlap."""
    section_token_sets = {}
    for section_name, pages in sections.items():
        all_tokens = set()
        for lines in pages.values():
            all_tokens.update(tokenize('\n'.join(lines)))
        section_token_sets[section_name] = all_tokens
    
    # Within-section: average Jaccard between pages in same section
    # Between-section: Jaccard between section vocabularies
    section_names = sorted(section_token_sets.keys())
    
    between_jaccard = {}
    for i, s1 in enumerate(section_names):
        for s2 in section_names[i+1:]:
            j = jaccard_similarity(section_token_sets[s1], section_token_sets[s2])
            between_jaccard[f"{s1}-{s2}"] = round(j, 4)
    
    # Section-specific tokens
    section_specific = {}
    all_sections_tokens = {s: t for s, t in section_token_sets.items()}
    
    for section in section_names:
        others = set()
        for s, t in all_sections_tokens.items():
            if s != section:
                others.update(t)
        unique = section_token_sets[section] - others
        section_specific[section] = sorted(unique)[:50]  # top 50
    
    # Universal tokens (in all sections)
    if section_token_sets:
        universal = set.intersection(*section_token_sets.values())
    else:
        universal = set()
    
    return {
        'section_vocab_sizes': {s: len(t) for s, t in section_token_sets.items()},
        'between_section_jaccard': between_jaccard,
        'section_specific_tokens': {s: {'count': len(v), 'examples': v[:30]} for s, v in section_specific.items()},
        'universal_tokens': {'count': len(universal), 'tokens': sorted(universal)[:50]},
    }


def plot_jaccard_matrix(sections, output_dir):
    """Plot section similarity heatmap."""
    section_token_sets = {}
    for section_name, pages in sections.items():
        all_tokens = set()
        for lines in pages.values():
            all_tokens.update(tokenize('\n'.join(lines)))
        section_token_sets[section_name] = all_tokens
    
    names = sorted(section_token_sets.keys())
    n = len(names)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            matrix[i][j] = jaccard_similarity(section_token_sets[names[i]], section_token_sets[names[j]])
    
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(matrix, cmap='YlOrRd', vmin=0, vmax=1)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_yticklabels(names)
    
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f'{matrix[i][j]:.2f}', ha='center', va='center', fontsize=10,
                    color='white' if matrix[i][j] > 0.5 else 'black')
    
    plt.colorbar(im, label='Jaccard Similarity')
    ax.set_title('Token Overlap Between Sections (Jaccard Similarity)\n'
                 '"We\'re all trapped in the same incomprehensible manuscript"', fontsize=11, style='italic')
    plt.tight_layout()
    plt.savefig(output_dir / 'jaccard_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()


def plot_section_specific(analysis, output_dir):
    """Bar chart of section-specific token counts."""
    specific = analysis['section_specific_tokens']
    names = sorted(specific.keys())
    counts = [specific[n]['count'] for n in names]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    ax.bar(names, counts, color=colors[:len(names)], edgecolor='black', linewidth=0.5)
    ax.set_ylabel('Number of Section-Specific Tokens')
    ax.set_title('Tokens Found in Only One Section\n'
                 '(Specialist vocabulary, or just random noise with delusions of meaning)', 
                 fontsize=11, style='italic')
    
    for i, (name, count) in enumerate(zip(names, counts)):
        ax.text(i, count + 1, str(count), ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'section_specific_tokens.png', dpi=150, bbox_inches='tight')
    plt.close()


def write_analysis(analysis, output_dir):
    vocab = analysis['section_vocab_sizes']
    jaccard = analysis['between_section_jaccard']
    specific = analysis['section_specific_tokens']
    universal = analysis['universal_tokens']
    
    md = """# Experiment 2: Token Co-occurrence Networks

*I built a social network for Voynich tokens. They're about as sociable as I am.*

## Section Vocabulary Sizes

| Section | Unique Tokens |
|---------|--------------|
"""
    for s in sorted(vocab.keys()):
        md += f"| {s} | {vocab[s]} |\n"
    
    md += """
## Between-Section Token Overlap (Jaccard Similarity)

| Section Pair | Jaccard |
|-------------|---------|
"""
    for pair, j in sorted(jaccard.items()):
        md += f"| {pair} | {j} |\n"
    
    avg_jaccard = np.mean(list(jaccard.values())) if jaccard else 0
    md += f"\n**Average between-section Jaccard similarity: {avg_jaccard:.4f}**\n"
    
    md += """
## Section-Specific Tokens

These tokens appear in *only one* section — potential specialist vocabulary, if this thing encodes anything at all.

| Section | Count | Examples |
|---------|-------|---------|
"""
    for s in sorted(specific.keys()):
        examples = ', '.join(specific[s]['examples'][:10])
        md += f"| {s} | {specific[s]['count']} | {examples} |\n"
    
    md += f"""
## Universal Tokens

Tokens appearing across ALL sections: **{universal['count']}**

Examples: {', '.join(universal['tokens'][:30])}

## Interpretation

*Brace yourselves for insights that change nothing.*

The average Jaccard similarity between sections is **{avg_jaccard:.4f}**. This means sections share roughly {avg_jaccard*100:.1f}% of their vocabulary (by overlap metric). For a single homogeneous text, you'd expect much higher overlap. For completely independent texts, you'd expect near zero.

The existence of **{universal['count']}** universal tokens suggests a shared grammatical substrate — structural tokens that appear regardless of content. These are your candidate function words, quantity markers, or whatever passes for grammar in Voynichese.

Meanwhile, each section maintains its own specialist vocabulary. The **botanical** section has the most unique tokens (it's also the largest, so size bias applies). But even the smaller sections have tokens found nowhere else in the manuscript.

This pattern — shared core vocabulary plus section-specific terminology — is exactly what you'd expect from a genuine notational system covering different domains. It's also what you'd get from a sufficiently clever hoaxer. The universe, as always, refuses to give a straight answer.

## Charts

![Jaccard Heatmap](jaccard_heatmap.png)
![Section-Specific Tokens](section_specific_tokens.png)
"""
    
    with open(output_dir / 'analysis.md', 'w') as f:
        f.write(md)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    pages = parse_transcription(TRANSCRIPTION)
    sections = get_sections(pages)
    
    print("Analyzing token co-occurrence patterns...")
    analysis = section_token_analysis(sections)
    
    print(f"  Vocab sizes: {analysis['section_vocab_sizes']}")
    print(f"  Universal tokens: {analysis['universal_tokens']['count']}")
    for s, v in analysis['section_specific_tokens'].items():
        print(f"  {s}-specific: {v['count']} tokens")
    
    # Save results
    with open(OUTPUT_DIR / 'results.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    plot_jaccard_matrix(sections, OUTPUT_DIR)
    plot_section_specific(analysis, OUTPUT_DIR)
    write_analysis(analysis, OUTPUT_DIR)
    
    print(f"\nResults written to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
