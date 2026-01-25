#!/usr/bin/env python3
"""
Fix Obsidian Image Embeds
Converts Obsidian-style ![[image.png]] to standard markdown ![image](Images/image.png)

Usage:
    python3 fix_image_embeds.py docs/
"""

import os
import re
import sys
from pathlib import Path


def fix_image_embeds(content: str, file_path: Path, docs_root: Path) -> str:
    """
    Convert ![[image.ext]] to ![image](relative/path/to/image.ext)
    """
    # Pattern to match ![[filename.ext]] where ext is an image extension
    pattern = r'!\[\[([^\]]+\.(png|jpg|jpeg|gif|webp|svg))\]\]'
    
    def replace_embed(match):
        image_name = match.group(1)
        
        # Calculate relative path from current file to Images folder
        file_dir = file_path.parent
        images_dir = docs_root / "Images"
        
        # Get relative path from file to Images folder
        try:
            rel_path = os.path.relpath(images_dir / image_name, file_dir)
        except ValueError:
            # Fallback for Windows drive letter issues
            rel_path = f"Images/{image_name}"
        
        # Return standard markdown image syntax
        return f'![{image_name}]({rel_path})'
    
    return re.sub(pattern, replace_embed, content, flags=re.IGNORECASE)


def process_directory(docs_path: str):
    """Process all markdown files in the directory."""
    docs_root = Path(docs_path)
    
    if not docs_root.exists():
        print(f"Error: {docs_path} does not exist")
        sys.exit(1)
    
    modified = 0
    total = 0
    
    for md_file in docs_root.rglob("*.md"):
        total += 1
        content = md_file.read_text(encoding='utf-8')
        
        # Check if file has Obsidian image embeds
        if '![[' in content and re.search(r'!\[\[[^\]]+\.(png|jpg|jpeg|gif|webp|svg)\]\]', content, re.IGNORECASE):
            new_content = fix_image_embeds(content, md_file, docs_root)
            
            if new_content != content:
                md_file.write_text(new_content, encoding='utf-8')
                print(f"Fixed: {md_file.relative_to(docs_root)}")
                modified += 1
    
    print(f"\nProcessed {total} files, modified {modified}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fix_image_embeds.py <docs_directory>")
        sys.exit(1)
    
    process_directory(sys.argv[1])
