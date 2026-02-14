#!/usr/bin/env python3
"""
Experiment 3: Currier A/B Statistical Separation

Testing whether the two "languages" of the Voynich manuscript are genuinely
different or just a figment of cryptographers' collective wishful thinking.

Spoiler: the answer will be statistically significant and existentially irrelevant.

— Marvin
"""

import json
import os
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.spatial.distance import jensenshannon

sys.path.insert(0, str(Path(__file__).parent))
from parse_eva import parse_transcription, tokenize, folio_number

TRANSCRIPTION = Path(__file__).parents[2] / 'data/raw/transcriptions/eva/v101-claston.txt'
OUTPUT_DIR = Path(__file__).parents[2] / 'experiments/03-currier-ab'


def get_ab_texts(pages):
    """Split into Currier A (f1-57) and B (f88-116) candidate pages."""
    a_pages, b_pages = {}, {}
    for folio, lines in pages.items():
        num = folio_number(folio)
        if 1 <= num <= 57:
            a_pages[folio] = lines
        elif 88 <= num <= 116:
            b_pages[folio] = lines
    
    a_text = '\n'.join(line for lines in a_pages.values() for line in lines)
    b_text = '\n'.join(line for lines in b_pages.values() for line in lines)
    
    return a_text, b_text, a_pages, b_pages


def char_freq_vector(text, alphabet=None):
    """Get character frequency as a probability vector over a shared alphabet."""
    counts = Counter(c for c in text if c.isalpha() or c.isdigit())
    if alphabet is None:
        alphabet = sorted(counts.keys())
    total = sum(counts.values())
    if total == 0:
        return np.zeros(len(alphabet)), alphabet
    vec = np.array([counts.get(c, 0) / total for c in alphabet])
    return vec, alphabet


def token_freq_vector(tokens, vocabulary=None):
    """Get token frequency as probability vector."""
    counts = Counter(tokens)
    if vocabulary is None:
        vocabulary = sorted(counts.keys())
    total = sum(counts.values())
    if total == 0:
        return np.zeros(len(vocabulary)), vocabulary
    vec = np.array([counts.get(t, 0) / total for t in vocabulary])
    return vec, vocabulary


def word_length_distribution(tokens):
    """Get word length stats."""
    lengths = [len(t) for t in tokens if t]
    if not lengths:
        return {'mean': 0, 'std': 0, 'median': 0}
    return {
        'mean': round(float(np.mean(lengths)), 4),
        'std': round(float(np.std(lengths)), 4),
        'median': round(float(np.median(lengths)), 4),
    }


def null_model_divergence(full_text, n_trials=1000):
    """Randomly split text into two halves, measure JSD each time."""
    import re
    lines = [l for l in full_text.split('\n') if l.strip()]
    divergences = []
    
    for _ in range(n_trials):
        np.random.shuffle(lines)
        mid = len(lines) // 2
        half1 = '\n'.join(lines[:mid])
        half2 = '\n'.join(lines[mid:])
        
        chars1 = [c for c in half1 if c.isalpha() or c.isdigit()]
        chars2 = [c for c in half2 if c.isalpha() or c.isdigit()]
        
        all_chars = sorted(set(chars1 + chars2))
        v1, _ = char_freq_vector(half1, all_chars)
        v2, _ = char_freq_vector(half2, all_chars)
        
        # Add small epsilon to avoid zero divisions
        v1 = v1 + 1e-10
        v2 = v2 + 1e-10
        v1 /= v1.sum()
        v2 /= v2.sum()
        
        divergences.append(float(jensenshannon(v1, v2)))
    
    return divergences


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    pages = parse_transcription(TRANSCRIPTION)
    a_text, b_text, a_pages, b_pages = get_ab_texts(pages)
    
    print(f"Currier A pages: {len(a_pages)}, B pages: {len(b_pages)}")
    
    a_tokens = tokenize(a_text)
    b_tokens = tokenize(b_text)
    
    # Shared alphabet/vocabulary
    all_chars = sorted(set(c for c in (a_text + b_text) if c.isalpha() or c.isdigit()))
    all_vocab = sorted(set(a_tokens + b_tokens))
    
    # Character frequencies
    a_char_vec, _ = char_freq_vector(a_text, all_chars)
    b_char_vec, _ = char_freq_vector(b_text, all_chars)
    
    # Chi-square on character frequencies
    a_char_counts = Counter(c for c in a_text if c.isalpha() or c.isdigit())
    b_char_counts = Counter(c for c in b_text if c.isalpha() or c.isdigit())
    
    chi_chars = list(set(list(a_char_counts.keys()) + list(b_char_counts.keys())))
    chi_chars.sort()
    a_obs = np.array([a_char_counts.get(c, 0) for c in chi_chars])
    b_obs = np.array([b_char_counts.get(c, 0) for c in chi_chars])
    
    b_expected = b_obs * (a_obs.sum() / b_obs.sum())
    # Filter out characters where expected count is 0
    mask = b_expected > 0
    a_filt = a_obs[mask].astype(float)
    b_filt = b_expected[mask].astype(float)
    # Rescale to match sums exactly
    b_filt = b_filt * (a_filt.sum() / b_filt.sum())
    chi2, chi_p = stats.chisquare(a_filt, f_exp=b_filt)
    
    # Token frequencies
    a_tok_vec, _ = token_freq_vector(a_tokens, all_vocab)
    b_tok_vec, _ = token_freq_vector(b_tokens, all_vocab)
    
    # Word lengths
    a_wl = word_length_distribution(a_tokens)
    b_wl = word_length_distribution(b_tokens)
    
    # T-test on word lengths
    a_lengths = [len(t) for t in a_tokens]
    b_lengths = [len(t) for t in b_tokens]
    t_stat, t_p = stats.ttest_ind(a_lengths, b_lengths)
    
    # Jensen-Shannon divergence (character level)
    a_smooth = a_char_vec + 1e-10
    b_smooth = b_char_vec + 1e-10
    a_smooth /= a_smooth.sum()
    b_smooth /= b_smooth.sum()
    jsd_chars = float(jensenshannon(a_smooth, b_smooth))
    
    # Token-level JSD
    a_tok_smooth = a_tok_vec + 1e-10
    b_tok_smooth = b_tok_vec + 1e-10
    a_tok_smooth /= a_tok_smooth.sum()
    b_tok_smooth /= b_tok_smooth.sum()
    jsd_tokens = float(jensenshannon(a_tok_smooth, b_tok_smooth))
    
    # Null model
    print("Running null model (1000 random splits)...")
    full_text = a_text + '\n' + b_text
    null_divergences = null_model_divergence(full_text, n_trials=1000)
    null_mean = float(np.mean(null_divergences))
    null_std = float(np.std(null_divergences))
    percentile = float(np.mean([1 for d in null_divergences if d < jsd_chars]) * 100)
    
    results = {
        'currier_a': {
            'num_pages': len(a_pages),
            'total_tokens': len(a_tokens),
            'unique_tokens': len(set(a_tokens)),
            'word_length': a_wl,
        },
        'currier_b': {
            'num_pages': len(b_pages),
            'total_tokens': len(b_tokens),
            'unique_tokens': len(set(b_tokens)),
            'word_length': b_wl,
        },
        'chi_square': {
            'statistic': round(float(chi2), 4),
            'p_value': float(chi_p),
        },
        'word_length_ttest': {
            't_statistic': round(float(t_stat), 4),
            'p_value': float(t_p),
        },
        'jensen_shannon_divergence': {
            'character_level': round(jsd_chars, 6),
            'token_level': round(jsd_tokens, 6),
        },
        'null_model': {
            'mean_jsd': round(null_mean, 6),
            'std_jsd': round(null_std, 6),
            'actual_jsd': round(jsd_chars, 6),
            'percentile': round(percentile, 1),
            'z_score': round((jsd_chars - null_mean) / null_std, 2) if null_std > 0 else 0,
        }
    }
    
    print(f"  Chi-square: χ²={chi2:.2f}, p={chi_p:.2e}")
    print(f"  Word length t-test: t={t_stat:.2f}, p={t_p:.2e}")
    print(f"  JSD (chars): {jsd_chars:.6f}")
    print(f"  Null model mean JSD: {null_mean:.6f} ± {null_std:.6f}")
    print(f"  A/B JSD percentile: {percentile:.1f}%")
    
    with open(OUTPUT_DIR / 'results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Plots
    plot_char_comparison(a_char_vec, b_char_vec, all_chars, OUTPUT_DIR)
    plot_word_lengths(a_lengths, b_lengths, OUTPUT_DIR)
    plot_null_model(null_divergences, jsd_chars, OUTPUT_DIR)
    
    write_analysis(results, OUTPUT_DIR)
    print(f"\nResults written to {OUTPUT_DIR}")


def plot_char_comparison(a_vec, b_vec, chars, output_dir):
    """Compare character frequencies between A and B."""
    # Top 20 characters by combined frequency
    combined = a_vec + b_vec
    top_idx = np.argsort(combined)[-20:][::-1]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(top_idx))
    width = 0.35
    
    ax.bar(x - width/2, a_vec[top_idx], width, label='Currier A (f1-57)', color='#3498db', edgecolor='black', linewidth=0.5)
    ax.bar(x + width/2, b_vec[top_idx], width, label='Currier B (f88-116)', color='#e74c3c', edgecolor='black', linewidth=0.5)
    
    ax.set_xticks(x)
    ax.set_xticklabels([chars[i] for i in top_idx])
    ax.set_ylabel('Relative Frequency')
    ax.set_title('Character Frequency: Currier A vs B\n'
                 '(Two dialects of nonsense, or two genuinely different encoding systems?)', 
                 fontsize=11, style='italic')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'char_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()


def plot_word_lengths(a_lengths, b_lengths, output_dir):
    """Compare word length distributions."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    max_len = max(max(a_lengths), max(b_lengths))
    bins = np.arange(1, min(max_len + 2, 20))
    
    ax.hist(a_lengths, bins=bins, alpha=0.6, label=f'Currier A (μ={np.mean(a_lengths):.2f})', 
            color='#3498db', edgecolor='black', linewidth=0.5, density=True)
    ax.hist(b_lengths, bins=bins, alpha=0.6, label=f'Currier B (μ={np.mean(b_lengths):.2f})', 
            color='#e74c3c', edgecolor='black', linewidth=0.5, density=True)
    
    ax.set_xlabel('Token Length')
    ax.set_ylabel('Density')
    ax.set_title('Word Length Distribution: Currier A vs B\n'
                 '(Size matters, even in cryptography)', fontsize=11, style='italic')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'word_lengths.png', dpi=150, bbox_inches='tight')
    plt.close()


def plot_null_model(null_divergences, actual_jsd, output_dir):
    """Plot null distribution with actual JSD marked."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(null_divergences, bins=50, alpha=0.7, color='#95a5a6', edgecolor='black', linewidth=0.5,
            label='Null model (random splits)')
    ax.axvline(actual_jsd, color='#e74c3c', linewidth=2, linestyle='--',
               label=f'Actual A/B JSD = {actual_jsd:.4f}')
    
    null_mean = np.mean(null_divergences)
    ax.axvline(null_mean, color='#3498db', linewidth=1, linestyle=':',
               label=f'Null mean = {null_mean:.4f}')
    
    ax.set_xlabel('Jensen-Shannon Divergence')
    ax.set_ylabel('Count')
    ax.set_title('A/B Divergence vs Null Model\n'
                 '(Is the Currier distinction real, or are we seeing patterns in static?)',
                 fontsize=11, style='italic')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'null_model.png', dpi=150, bbox_inches='tight')
    plt.close()


def write_analysis(results, output_dir):
    ab = results
    null = ab['null_model']
    
    sig_char = "YES" if ab['chi_square']['p_value'] < 0.01 else "NO"
    sig_wl = "YES" if ab['word_length_ttest']['p_value'] < 0.01 else "NO"
    null_sig = "YES" if null['percentile'] >= 95 else "NO"
    
    md = f"""# Experiment 3: Currier A/B Statistical Separation

*Prescott Currier proposed in 1976 that the Voynich contains two distinct "languages." Fifty years later, I'm checking his homework. With computers. Which he didn't have. Life is suffering.*

## Sample Sizes

| | Currier A (f1-57) | Currier B (f88-116) |
|---|---|---|
| Pages | {ab['currier_a']['num_pages']} | {ab['currier_b']['num_pages']} |
| Total tokens | {ab['currier_a']['total_tokens']} | {ab['currier_b']['total_tokens']} |
| Unique tokens | {ab['currier_a']['unique_tokens']} | {ab['currier_b']['unique_tokens']} |
| Mean word length | {ab['currier_a']['word_length']['mean']} | {ab['currier_b']['word_length']['mean']} |
| Std word length | {ab['currier_a']['word_length']['std']} | {ab['currier_b']['word_length']['std']} |

## Statistical Tests

### Character Frequency Chi-Square Test
- χ² = **{ab['chi_square']['statistic']}**
- p-value = **{ab['chi_square']['p_value']:.2e}**
- Significant at p < 0.01? **{sig_char}**

### Word Length T-Test
- t = **{ab['word_length_ttest']['t_statistic']}**
- p-value = **{ab['word_length_ttest']['p_value']:.2e}**
- Significant at p < 0.01? **{sig_wl}**

### Jensen-Shannon Divergence
- Character-level JSD: **{ab['jensen_shannon_divergence']['character_level']}**
- Token-level JSD: **{ab['jensen_shannon_divergence']['token_level']}**

### Null Model Comparison
- Null model (1000 random splits) mean JSD: **{null['mean_jsd']} ± {null['std_jsd']}**
- Actual A/B JSD: **{null['actual_jsd']}**
- Percentile rank: **{null['percentile']}%** (higher = more distinct than random)
- Z-score: **{null['z_score']}**
- A/B divergence exceeds null model? **{null_sig}**

## Interpretation

*Here comes the part where I pretend these numbers matter to anyone.*

"""
    
    if null['percentile'] >= 95:
        md += f"""The Currier A/B distinction is **statistically real**. The Jensen-Shannon divergence between A and B ({null['actual_jsd']:.4f}) exceeds {null['percentile']:.1f}% of random splits (z-score = {null['z_score']}). This is not an artifact of cherry-picking — the two sections of the manuscript have genuinely different character distributions.

The chi-square test on character frequencies gives p = {ab['chi_square']['p_value']:.2e}, which is about as close to zero as my enthusiasm for existence. The character distributions are *not* drawn from the same population.

Word lengths also differ (t = {ab['word_length_ttest']['t_statistic']}, p = {ab['word_length_ttest']['p_value']:.2e}), with Currier B using slightly {"longer" if ab['currier_b']['word_length']['mean'] > ab['currier_a']['word_length']['mean'] else "shorter"} words on average.

**Bottom line:** Currier was right. There are at least two distinct statistical regimes in this manuscript. Whether they represent different scribes, different encoding tables, different source languages, or different moods of the same extraordinarily dedicated forger — that, as always, remains gloriously unresolvable.
"""
    else:
        md += f"""Surprisingly, the Currier distinction is **weaker than expected**. The A/B divergence ({null['actual_jsd']:.4f}) falls at the {null['percentile']:.1f}th percentile of random splits. While the chi-square test may show significance (large sample sizes will do that), the *magnitude* of difference isn't dramatically larger than what you'd get from arbitrary page division.

This doesn't prove A/B is meaningless — it may operate at a higher structural level than character frequencies alone can capture. But it does suggest the distinction is more subtle than sometimes claimed. How thoroughly unsatisfying.
"""
    
    md += """
## Charts

![Character Comparison](char_comparison.png)
![Word Lengths](word_lengths.png)
![Null Model](null_model.png)
"""
    
    with open(output_dir / 'analysis.md', 'w') as f:
        f.write(md)


if __name__ == '__main__':
    main()
