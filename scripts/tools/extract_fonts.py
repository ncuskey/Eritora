#!/usr/bin/env python3
"""
Extract Draconis font from publish.css base64 data.

Usage:
    python3 extract_fonts.py docs/publish.css docs/assets/fonts/
"""

import base64
import re
import sys
from pathlib import Path


def extract_fonts(css_path: str, output_dir: str):
    """Extract base64-encoded fonts from CSS."""
    css_content = Path(css_path).read_text(encoding='utf-8')
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Pattern to match @font-face blocks
    font_face_pattern = r'@font-face\s*\{([^}]+)\}'
    
    font_faces = re.findall(font_face_pattern, css_content, re.DOTALL)
    
    fonts_extracted = 0
    
    for i, face in enumerate(font_faces):
        # Determine font variant
        weight = 'normal'
        style = 'normal'
        
        if 'font-weight: bold' in face:
            weight = 'bold'
        if 'font-style: italic' in face:
            style = 'italic'
        
        # Determine filename
        if weight == 'bold':
            base_name = 'draconis-bold'
        elif style == 'italic':
            base_name = 'draconis-italic'
        else:
            base_name = 'draconis'
        
        # Extract woff2 data
        woff2_match = re.search(r"url\('data:font/woff2;charset=utf-8;base64,([^']+)'\)", face)
        if woff2_match:
            woff2_data = base64.b64decode(woff2_match.group(1))
            woff2_path = output_path / f"{base_name}.woff2"
            woff2_path.write_bytes(woff2_data)
            print(f"Extracted: {woff2_path}")
            fonts_extracted += 1
        
        # Extract woff data
        woff_match = re.search(r"url\('data:font/woff;charset=utf-8;base64,([^']+)'\)", face)
        if woff_match:
            woff_data = base64.b64decode(woff_match.group(1))
            woff_path = output_path / f"{base_name}.woff"
            woff_path.write_bytes(woff_data)
            print(f"Extracted: {woff_path}")
            fonts_extracted += 1
    
    print(f"\nTotal fonts extracted: {fonts_extracted}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 extract_fonts.py <css_file> <output_dir>")
        sys.exit(1)
    
    extract_fonts(sys.argv[1], sys.argv[2])
