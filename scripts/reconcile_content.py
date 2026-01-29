#!/usr/bin/env python3
import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote
import argparse

# Configuration
DOCS_DIR = os.path.abspath("docs")
BASE_URL = "https://eritora.wiki/"
SITEMAP_URL = "https://eritora.wiki/sitemap.xml"

def get_source_files(docs_dir):
    """Recursively find all .md files in docs_dir."""
    source_files = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md") and not file.startswith("."):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, docs_dir)
                source_files.append(rel_path)
    return source_files

def source_to_url(rel_path):
    """Convert a relative markdown path to an expected URL path."""
    # This is a heuristic for MkDocs. 
    # folder/file.md -> folder/file/
    # folder/index.md -> folder/
    
    parts = rel_path.split(os.sep)
    filename = parts[-1]
    
    if filename == "index.md":
        # folder/index.md -> folder/
        url_path = "/".join(parts[:-1])
    else:
        # folder/file.md -> folder/file/
        name_no_ext = os.path.splitext(filename)[0]
        url_path = "/".join(parts[:-1] + [name_no_ext])
        
    # Ensure it ends with / checks if not empty
    if url_path:
        url_path += "/"
    
    # Handle root index.md -> "" -> "" (gets joined with base)
    
    # URL encode parts? MkDocs usually slugifies. 
    # For now, let's assume simple files or match what sitemap has (usually encoded).
    # actually sitemap usually has encoded URLs.
    # We might need to fetch sitemap first to see format.
    
    return url_path

def get_sitemap_urls(sitemap_url):
    """Fetch and parse sitemap to get clear paths."""
    print(f"Fetching sitemap: {sitemap_url}")
    try:
        r = requests.get(sitemap_url)
        r.raise_for_status()
        
        # XML parsing
        root = ET.fromstring(r.content)
        # namespace usually http://www.sitemaps.org/schemas/sitemap/0.9
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = set()
        for url_tag in root.findall('ns:url', ns):
            loc = url_tag.find('ns:loc', ns).text
            # Normalize to relative path from base
            if loc.startswith(BASE_URL):
                rel = loc[len(BASE_URL):]
                urls.add(unquote(rel)) # Decode %20 etc to match file system names potentially
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return set()

def main():
    print(f"Scanning source files in {DOCS_DIR}...")
    source_files = get_source_files(DOCS_DIR)
    print(f"Found {len(source_files)} source markdown files.")
    
    print("Computing expected URLs...")
    expected_urls = {} # url -> source_path
    for src in source_files:
        url = source_to_url(src)
        expected_urls[url] = src
        
    sitemap_paths = get_sitemap_urls(SITEMAP_URL)
    print(f"Found {len(sitemap_paths)} URLs in sitemap.")
    
    # Compare
    # Check which expected URLs are NOT in sitemap
    orphans = []
    
    # Note: sitemap paths might handle spaces differently or be slugified.
    # MkDocs standard slugify usually lowercases and replaces spaces with dashes.
    # BUT eritora seems to preserve spaces/capitalization or use specific constraints.
    # Let's check for direct match first.
    
    for url, src in expected_urls.items():
        # Heuristic: try exact match, then try slugified match if needed
        if url not in sitemap_paths:
            # Maybe slugified? 
            # If our simple source_to_url assumption failed
            orphans.append({'source': src, 'expected_url': url})

    print("\n" + "="*30)
    print("ORPHANED CONTENT REPORT")
    print("="*30)
    
    if orphans:
        print(f"Found {len(orphans)} potential orphans (Source exists, but URL not in sitemap):")
        for o in orphans:
            print(f"[ORPHAN] {o['source']}  --> Expected: {o['expected_url']}")
    else:
        print("No orphaned content found! All source files appear to map to sitemap URLs.")

if __name__ == "__main__":
    main()
