#!/usr/bin/env python3
import yaml
import requests
import argparse
import sys
from urllib.parse import urljoin, unquote

MKDOCS_FILE = "mkdocs.yml"
BASE_URL = "https://eritora.wiki/"

def verify_redirects(limit=None):
    print(f"Loading redirects from {MKDOCS_FILE}...")
    try:
        with open(MKDOCS_FILE, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading mkdocs.yml: {e}")
        return

    redirects = {}
    
    # Locate the redirects plugin config
    if 'plugins' in config:
        for plugin in config['plugins']:
            if isinstance(plugin, dict) and 'redirects' in plugin:
                redirects = plugin['redirects'].get('redirect_maps', {})
                break
    
    if not redirects:
        print("No redirect_maps found in mkdocs.yml")
        return

    print(f"Found {len(redirects)} redirects defined.")
    
    items = list(redirects.items())
    if limit:
        items = items[:limit]
        print(f"Checking first {limit} redirects...")
    
    passed = 0
    failed = 0
    
    for old_path, new_path in items:
        # Construct source URL
        # old_path usually looks like '# Magic Items/index.html'
        # We need to URL encode it typically, but requests might handle it
        # Actually, if the key in yaml is '# Magic Items/index.html', the URL is likely .../#%20Magic%20Items/index.html
        # But wait, '#' might be problematic if not encoded.
        
        # Requests will encode path parts?
        # Let's clean the path. 
        # If it starts with #, that is a fragment in URL terms, but here it is a filename/folder name starting with #?
        # MkDocs redirects inputs are file paths relative to docs dir usually (or output paths?)
        # usually output paths.
        
        # If the file on disk is "8. .../# Magic Items.md", MkDocs build might create "# Magic Items/index.html"
        # The URL would be `%23%20Magic%20Items/`
        
        # Let's try raw first.
        
        # NOTE: requests.head won't work well if we don't handle encoding manually for weird chars like # in path
        # urljoin might not encode #
        
        # We need to encode the path segments.
        safe_path = old_path.replace(" ", "%20").replace("#", "%23")
        source_url = urljoin(BASE_URL, safe_path)
        
        try:
            # Check successful reachability
            r = requests.get(source_url, allow_redirects=True, timeout=5)
            
            # Case 1: HTTP Redirect (3xx) -> handled by requests, appearing in history
            if len(r.history) > 0:
                # We redirected via HTTP
                passed += 1
                # print(f"[PASS] {old_path} -> HTTP Redirect -> {r.url}")
                continue

            # Case 2: Meta Refresh (200 OK)
            if r.status_code == 200:
                content = r.text.lower()
                
                # Extract refresh target
                match = re.search(r'content=["\']\d+;\s*url=(.*?)["\']', content, re.IGNORECASE)
                if match:
                    target = match.group(1)
                    # Resolve target relative to source_url
                    # source_url is effectively the folder (since index.html)
                    # if source is .../foo/bar/
                    # target is ../baz/
                    # resolved is .../foo/baz/
                    
                    # Be careful if source_url ends in .html or /
                    # In requests, the url might be .../index.html or .../
                    base = r.url
                    # If base ends in .html, dirname is parent.
                    # If base ends in /, dirname is base (minus slash?)
                    # urljoin handles this.
                    
                    resolved_target = urljoin(base, target)
                    
                    # Normalize for comparison (remove trailing slashes, decoding)
                    def normalize(u):
                        u = unquote(u)
                        if u.endswith('/'): u = u[:-1]
                        if u.endswith('/index.html'): u = u[:-11]
                        return u
                        
                    norm_source = normalize(base)
                    norm_target = normalize(resolved_target)
                    
                    if norm_source == norm_target:
                         failed += 1
                         print(f"[FAIL] {old_path} -> LOOP DETECTED. Redirects to self: {target}")
                    else:
                         passed += 1
                         # print(f"[PASS] {old_path} -> {target}")

                elif 'redirecting...' in content and '<script>location=' in content:
                     # JS redirect, harder to parse, assume OK for now or parse JS
                     passed += 1
                else:
                    if len(content) > 15000:
                        failed += 1
                        print(f"[FAIL] {old_path} -> Served full page (Soft 404?) Size: {len(content)}")
                    else:
                        failed += 1
                        print(f"[FAIL] {old_path} -> 200 OK but not a redirect artifact? Size: {len(content)}")

            elif r.status_code == 404:
                failed += 1
                print(f"[FAIL] {old_path} -> 404 Not Found")
            else:
                failed += 1
                print(f"[FAIL] {old_path} -> {r.status_code}")

        except Exception as e:
            failed += 1
            print(f"[ERROR] {old_path}: {e}")
            
    print("-" * 30)
    print(f"Results: {passed} PASSED, {failed} FAILED")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, help='Limit number of checks')
    args = parser.parse_args()
    
    verify_redirects(args.limit)

if __name__ == "__main__":
    main()
