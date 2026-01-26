import sys

def inject_redirects():
    # Read mkdocs.yml
    with open('mkdocs.yml', 'r') as f:
        config_lines = f.readlines()
    
    # Read redirects
    with open('redirects_clean.yaml', 'r') as f:
        redirect_lines = f.readlines()
        
    # Remove "plugins:" from redirects if present
    clean_redirects = [line for line in redirect_lines if not line.strip().startswith('plugins:')]
    
    # Find insertion point (before extra_css: or end of plugins)
    insert_idx = -1
    for i, line in enumerate(config_lines):
        if line.startswith('extra_css:'):
            insert_idx = i
            break
    
    if insert_idx == -1:
        # If extra_css not found, just before EOF? 
        # But we need to be careful about indentation if EOF is nested.
        # Assuming typical structure, appending to end might have been fine if plugins was last.
        # But it wasn't.
        # We'll insert at end if no following key found (unlikely given file checks).
        insert_idx = len(config_lines)

    # Insert
    new_lines = config_lines[:insert_idx] + clean_redirects + config_lines[insert_idx:]
    
    with open('mkdocs.yml', 'w') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    inject_redirects()
