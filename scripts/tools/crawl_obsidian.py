#!/usr/bin/env python3
"""
Obsidian Publish Crawler
Crawls an Obsidian Publish site and downloads all markdown files and images.

Usage:
    python3 crawl_obsidian.py --uid <site-uid> --output <output-dir>
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def fetch_json(url: str) -> dict:
    """Fetch JSON from URL."""
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))


def fetch_file(url: str) -> bytes:
    """Fetch binary content from URL."""
    with urllib.request.urlopen(url) as response:
        return response.read()


def crawl_obsidian_publish(uid: str, output_dir: str, host: str = "publish-01.obsidian.md"):
    """
    Crawl an Obsidian Publish site and download all files.
    
    Args:
        uid: The site UID (found in page source)
        output_dir: Directory to save files to
        host: Obsidian Publish host
    """
    cache_url = f"https://{host}/cache/{uid}"
    access_base = f"https://{host}/access/{uid}"
    
    print(f"Fetching cache from {cache_url}...")
    cache = fetch_json(cache_url)
    
    # Separate files by type
    md_files = []
    other_files = []
    
    for path in cache.keys():
        if path.endswith('.md'):
            md_files.append(path)
        elif path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.css')):
            other_files.append(path)
        # Skip entries that are None (metadata-only entries)
    
    total_files = len(md_files) + len(other_files)
    print(f"Found {len(md_files)} markdown files and {len(other_files)} assets")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded = 0
    errors = []
    
    # Download markdown files
    for i, filepath in enumerate(md_files, 1):
        try:
            # URL encode the path
            encoded_path = urllib.parse.quote(filepath)
            url = f"{access_base}/{encoded_path}"
            
            # Determine output path
            out_file = output_path / filepath
            out_file.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"[{i}/{len(md_files)}] Downloading: {filepath}")
            content = fetch_file(url)
            
            # Write as text (markdown)
            out_file.write_bytes(content)
            downloaded += 1
            
        except Exception as e:
            errors.append((filepath, str(e)))
            print(f"  ERROR: {e}")
    
    # Download assets
    for i, filepath in enumerate(other_files, 1):
        try:
            encoded_path = urllib.parse.quote(filepath)
            url = f"{access_base}/{encoded_path}"
            
            out_file = output_path / filepath
            out_file.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"[{i}/{len(other_files)}] Downloading asset: {filepath}")
            content = fetch_file(url)
            out_file.write_bytes(content)
            downloaded += 1
            
        except Exception as e:
            errors.append((filepath, str(e)))
            print(f"  ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Downloaded: {downloaded}/{total_files} files")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nFailed files:")
        for path, error in errors[:10]:
            print(f"  - {path}: {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    
    return downloaded, errors


def main():
    parser = argparse.ArgumentParser(description="Crawl Obsidian Publish site")
    parser.add_argument("--uid", required=True, help="Site UID from Obsidian Publish")
    parser.add_argument("--output", default="docs", help="Output directory (default: docs)")
    parser.add_argument("--host", default="publish-01.obsidian.md", help="Obsidian Publish host")
    
    args = parser.parse_args()
    
    downloaded, errors = crawl_obsidian_publish(args.uid, args.output, args.host)
    
    sys.exit(0 if len(errors) == 0 else 1)


if __name__ == "__main__":
    main()
