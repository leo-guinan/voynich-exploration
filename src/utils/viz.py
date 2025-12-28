"""
Visualization utilities for Voynich research.
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from pathlib import Path


def plot_folio_grid(folio_images: list, titles: list = None, figsize=(20, 15)):
    """
    Plot a grid of folio images.
    
    Args:
        folio_images: List of PIL Images or image paths
        titles: List of titles (optional)
        figsize: Figure size tuple
    """
    n = len(folio_images)
    cols = min(3, n)
    rows = (n + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if n == 1:
        axes = [axes]
    elif rows == 1:
        axes = axes if isinstance(axes, np.ndarray) else [axes]
    else:
        axes = axes.flatten()
    
    for i, img in enumerate(folio_images):
        if i >= len(axes):
            break
        
        if isinstance(img, (str, Path)):
            img = Image.open(img)
        
        axes[i].imshow(img)
        if titles and i < len(titles):
            axes[i].set_title(titles[i], fontsize=12)
        axes[i].axis('off')
    
    # Hide unused subplots
    for i in range(len(folio_images), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    return fig


def plot_distribution(data, title="Distribution", xlabel="Value", ylabel="Frequency", bins=50):
    """
    Plot a distribution histogram.
    
    Args:
        data: Array-like data to plot
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        bins: Number of bins
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=bins, edgecolor='black', alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_zipf_curve(frequencies, title="Zipf Distribution"):
    """
    Plot a Zipf-like frequency curve (log-log).
    
    Args:
        frequencies: Sorted list of frequencies (descending)
        title: Plot title
    """
    ranks = range(1, len(frequencies) + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Linear scale
    ax1.plot(ranks, frequencies, 'o-', markersize=4)
    ax1.set_xlabel('Rank')
    ax1.set_ylabel('Frequency')
    ax1.set_title(f'{title} (Linear)')
    ax1.grid(True, alpha=0.3)
    
    # Log-log scale (Zipf)
    ax2.loglog(ranks, frequencies, 'o-', markersize=4)
    ax2.set_xlabel('Rank (log)')
    ax2.set_ylabel('Frequency (log)')
    ax2.set_title(f'{title} (Log-Log - Zipf Check)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

