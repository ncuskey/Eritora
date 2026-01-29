#!/usr/bin/env python3
import os
import re
from urllib.parse import unquote

DOCS_DIR = os.path.abspath("docs")

def find_references(content):
    """Find all [text](link) and ![alt](src) references, handling nested parentheses."""
    refs = []
    
    # We'll scan manually to handle nested parens
    # Find all '](', then parse forward
    
    # This is a basic state machine approach
    # 0: looking for '[', 1: inside [], 2: looking for '(', 3: inside ()
    
    # Actually, simpler: find `](` indices
    # But we need to make sure the `]` was a closing bracket for a link text.
    
    # Let's use a iterator
    i = 0
    n = len(content)
    while i < n:
        # Check for start of link text
        if content[i] == '[':
            # fast forward to matching ']'
            depth = 1
            j = i + 1
            while j < n and depth > 0:
                if content[j] == '[': depth += 1
                elif content[j] == ']': depth -= 1
                j += 1
            
            if depth == 0 and j < n and content[j] == '(':
                # found ](, now find matching )
                start_link = j + 1
                depth_paren = 1
                k = start_link
                while k < n and depth_paren > 0:
                    if content[k] == '(': depth_paren += 1
                    elif content[k] == ')': depth_paren -= 1
                    k += 1
                
                if depth_paren == 0:
                    link = content[start_link:k-1]
                    refs.append(link)
                    i = k
                    continue
        
        # Also handle images ![
        if content[i] == '!' and i+1 < n and content[i+1] == '[':
             # Just skip the '!', the loop will hit '[' next
             i += 1
             continue
             
        i += 1
            
    return refs

def resolve_path(source_file, ref):
    """Resolve a relative reference to an absolute filesystem path."""
    # Ignore external links
    if ref.startswith(('http://', 'https://', 'ftp://', 'mailto:')):
        return None
        
    # Ignore anchors only
    if ref.startswith('#'):
        return None
        
    # Strip anchor from ref
    ref_path = ref.split('#')[0]
    if not ref_path:
        return None
        
    # Decode %20
    ref_path = unquote(ref_path)
    
    source_dir = os.path.dirname(source_file)
    
    # MkDocs specific: absolute paths start from docs_dir implied?
    # Usually mkdocs standard is relative to current file.
    # If starts with /, it's usually relative to site root.
    
    if ref_path.startswith('/'):
        # Relative to docs root
        abs_target = os.path.join(DOCS_DIR, ref_path.lstrip('/'))
    else:
        # Relative to current file
        abs_target = os.path.join(source_dir, ref_path)
        
    return os.path.normpath(abs_target)

def check_target_exists(path):
    # It might be a file, or a directory (if index.md implied?)
    # MkDocs links often point to .md files, but sometimes to folders implying index.md
    
    if os.path.exists(path):
        return True, "Found"
        
    # Check if it was a link to a directory implying index.md
    if os.path.isdir(path):
        index_path = os.path.join(path, "index.md")
        if os.path.exists(index_path):
            return True, "Found index"
            
    # Check if it was a link to .html but we have .md
    # (some people write [link](foo.html) in MD knowing it builds to HTML)
    if path.endswith('.html'):
        md_path = path[:-5] + ".md"
        if os.path.exists(md_path):
            return True, "Found MD for HTML"
            
    return False, "Missing"

def main():
    print(f"Validating source integrity in {DOCS_DIR}...")
    
    broken_links = []
    
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                source_path = os.path.join(root, file)
                rel_source = os.path.relpath(source_path, DOCS_DIR)
                
                try:
                    with open(source_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    refs = find_references(content)
                    
                    for ref in refs:
                        target = resolve_path(source_path, ref)
                        if target:
                            exists, reason = check_target_exists(target)
                            if not exists:
                                broken_links.append({
                                    'source': rel_source,
                                    'link': ref,
                                    'resolved': target
                                })
                                
                except Exception as e:
                    print(f"Error reading {rel_source}: {e}")

    print("\n" + "="*30)
    print("SOURCE INTEGRITY REPORT")
    print("="*30)
    
    if broken_links:
        print(f"Found {len(broken_links)} broken internal references:\n")
        count = 0
        for b in broken_links:
            count += 1
            if count > 50:
                print(f"... and {len(broken_links) - 50} more.")
                break
            print(f"[BROKEN] {b['source']} points to '{b['link']}'")
            # print(f"         (Resolved: {b['resolved']})")
    else:
        print("No broken internal links found in source files!")

if __name__ == "__main__":
    main()
