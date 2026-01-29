#!/usr/bin/env python3
import yaml
import os
import re
import requests
import sys
from urllib.parse import urlparse, unquote

MKDOCS_FILE = "mkdocs.yml"
DOCS_DIR = "docs" # Base directory for relative paths in mkdocs

def check_file_exists(path, description):
    if os.path.isfile(path):
        # print(f"[OK] {description}: {path}")
        return True
    else:
        print(f"[FAIL] {description} missing: {path}")
        return False

def check_url_reachability(url):
    try:
        r = requests.head(url, timeout=5)
        if r.status_code == 200:
            return True
        # Try GET if HEAD fails (some servers block HEAD)
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return True
        print(f"[FAIL] Remote asset unreachable: {url} (Status {r.status_code})")
        return False
    except Exception as e:
        print(f"[FAIL] Remote asset check error for {url}: {e}")
        return False

def audit_css_content(css_path):
    print(f"Scanning {css_path} for assets...")
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex for url(...)
        # url('...'), url("..."), url(...)
        urls = re.findall(r'url\((.*?)\)', content)
        
        failures = 0
        for u in urls:
            u = u.strip(' \'"')
            if u.startswith('data:'):
                continue
            
            if u.startswith('http://') or u.startswith('https://'):
                if not check_url_reachability(u):
                    failures += 1
            else:
                # Local asset
                # CSS paths are relative to the CSS file location usually in browsers.
                # If css is in docs/stylesheets/extra.css and url is ../assets/foo.png
                # Resolved path is docs/assets/foo.png
                
                css_dir = os.path.dirname(css_path)
                # handle query strings/fragments
                u_clean = u.split('?')[0].split('#')[0]
                
                # Check for absolute path (relative to site root?)
                # In mkdocs, usually relative to css file.
                
                asset_path = os.path.normpath(os.path.join(css_dir, u_clean))
                if not os.path.isfile(asset_path):
                     print(f"[FAIL] Missing asset referenced in {css_path}: {u} -> resolved to {asset_path}")
                     failures += 1
                     
        return failures
    except Exception as e:
        print(f"[ERROR] Reading {css_path}: {e}")
        return 1

def main():
    print(f"Loading configuration from {MKDOCS_FILE}...")
    try:
        with open(MKDOCS_FILE, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading mkdocs.yml: {e}")
        sys.exit(1)

    failures = 0

    # 1. Check extra_css
    if 'extra_css' in config:
        print(f"Found {len(config['extra_css'])} extra_css files.")
        for css in config['extra_css']:
            # mkdocs `extra_css` paths are relative to `docs_dir` (default 'docs')
            path = os.path.join(DOCS_DIR, css)
            if check_file_exists(path, "CSS File"):
                f = audit_css_content(path)
                failures += f
            else:
                failures += 1
    else:
        print("No extra_css defined.")

    # 2. Check extra_javascript
    if 'extra_javascript' in config:
        print(f"Found {len(config['extra_javascript'])} extra_javascript files.")
        for js in config['extra_javascript']:
            path = os.path.join(DOCS_DIR, js)
            if not check_file_exists(path, "JS File"):
                failures += 1
    else:
        print("No extra_javascript defined.")

    # 3. Check Logo/Favicon if defined
    theme = config.get('theme', {})
    if 'logo' in theme:
        logo = theme['logo']
        # logo is usually in docs dir
        path = os.path.join(DOCS_DIR, logo)
        if not check_file_exists(path, "Theme Logo"):
            failures += 1
    
    if 'favicon' in theme:
        fav = theme['favicon']
        path = os.path.join(DOCS_DIR, fav)
        if not check_file_exists(path, "Theme Favicon"):
            failures += 1

    print("-" * 30)
    if failures == 0:
        print("ASSET AUDIT PASSED")
        sys.exit(0)
    else:
        print(f"ASSET AUDIT FAILED with {failures} errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
