"""
Parse the EVA transcription file into structured data.
Because someone has to do the tedious work. Might as well be me.
"""

import re
from collections import defaultdict

SECTION_MAP = {
    'botanical': (1, 57),
    'astronomical': (67, 73),
    'biological': (75, 84),
    'pharmaceutical': (88, 116),
}

def parse_transcription(filepath):
    """Parse EVA transcription into {folio: [lines]}."""
    pages = defaultdict(list)
    current_folio = None
    
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Match folio markers like <1r.1>, <57v.3>
            match = re.match(r'^<(\d+[rv])\.(\d+)>(.*)', line)
            if match:
                current_folio = match.group(1)
                text = match.group(3).strip()
                if text:
                    pages[current_folio].append(text)
            elif current_folio and not line.startswith('#') and not line.startswith('<'):
                pages[current_folio].append(line)
    
    return dict(pages)


def folio_number(folio_id):
    """Extract numeric part from folio id like '57v' -> 57."""
    match = re.match(r'(\d+)', folio_id)
    return int(match.group(1)) if match else 0


def get_section(folio_id):
    """Map a folio to its section."""
    num = folio_number(folio_id)
    for section, (lo, hi) in SECTION_MAP.items():
        if lo <= num <= hi:
            return section
    return 'other'


def get_sections(pages):
    """Group pages by section. Returns {section: {folio: [lines]}}."""
    sections = defaultdict(dict)
    for folio, lines in pages.items():
        section = get_section(folio)
        sections[section][folio] = lines
    return dict(sections)


def get_section_text(pages, section_name):
    """Get all text for a section as one string."""
    sections = get_sections(pages)
    if section_name not in sections:
        return ''
    texts = []
    for folio in sorted(sections[section_name].keys(), key=folio_number):
        texts.extend(sections[section_name][folio])
    return '\n'.join(texts)


def tokenize(text):
    """Split text into tokens using . and spaces as delimiters.
    Also strips common annotation characters."""
    # Remove line-end markers and annotations
    text = re.sub(r'[=\-]$', '', text, flags=re.MULTILINE)
    # Split on dots, spaces, commas
    tokens = re.split(r'[.\s,]+', text)
    # Filter empty and pure-punctuation tokens
    tokens = [t for t in tokens if t and re.search(r'[a-zA-Z0-9]', t)]
    return tokens
