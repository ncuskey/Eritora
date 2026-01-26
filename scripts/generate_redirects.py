import os

def generate_redirects(docs_dir):
    redirects = {}
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if not file.endswith(".md"):
                continue
            
            # Source: Filename (flat)
            # Dest: Relative path from docs_dir
            
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, docs_dir)
            
            # Destination URL path (keep .md for plugin resolution)
            dest_url = rel_path
            
            # Source URL path (Filename without extension)
            filename = file[:-3]
            
            # Special Case: index.md -> Use Parent Directory Name
            if filename.lower() == "index":
                # root/docs/Parent/index.md -> rel_path "Parent/index.md"
                # split rel_path
                parts = rel_path.split('/')
                if len(parts) > 1:
                    # Parent Text is the folder name
                    # parts[-2] is the folder name (parts[-1] is index.html target)
                    # wait, rel_path from walk is "Path/To/File.md"
                    # split gives ['Path', 'To', 'File.md']
                    parent_dir = os.path.basename(root)
                    if parent_dir and parent_dir != "docs":
                         filename = parent_dir
            
            source_url = f"{filename}/index.html"
            
            # Slugified Source (lowercase, spaces to hyphens)
            slug = filename.lower().replace(" ", "-")
            slug_url = f"{slug}/index.html"

            # CRITICAL: Prevent overwriting actual content with a redirect (Infinite Loop)
            # If the generated source path matches the destination path (swapping .html/.md), skip it.
            if source_url.replace('.html', '.md') == dest_url:
                # print(f"Skipping self-redirect for {filename} ({dest_url})")
                pass # Do not map source_url
            else:
                 # Map original
                if source_url in redirects:
                    print(f"Warning: Duplicate filename '{filename}' - skipping {rel_path}")
                else:
                     redirects[source_url] = dest_url

            # Map slugified (if different)
            if slug_url != source_url:
                if slug_url in redirects:
                    print(f"Warning: Duplicate slug '{slug}' - skipping {rel_path}")
                else:
                    redirects[slug_url] = dest_url
            
            continue # Already added logic above, skip existing add logic

    return redirects

if __name__ == "__main__":
    redirects = generate_redirects("docs")
    print("plugins:")
    print("  - redirects:")
    print("      redirect_maps:")
    for src, dst in sorted(redirects.items()):
        src_safe = src.replace("'", "''")
        dst_safe = dst.replace("'", "''")
        print(f"        '{src_safe}': '{dst_safe}'")
