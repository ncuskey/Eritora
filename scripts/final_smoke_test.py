#!/usr/bin/env python3
import subprocess
import sys
import time

def run_step(description, command):
    print(f"[{description}] Running...")
    start = time.time()
    try:
        # Run command and capture output
        result = subprocess.run(
            command, 
            shell=True, 
            check=False, 
            capture_output=True, 
            text=True
        )
        duration = time.time() - start
        
        if result.returncode == 0:
            print(f"✅ PASS ({duration:.2f}s)")
            return True, result.stdout
        else:
            print(f"❌ FAIL ({duration:.2f}s)")
            print("--- Output ---")
            print(result.stdout)
            print("--- Error ---")
            print(result.stderr)
            return False, result.stderr
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False, str(e)

def main():
    print("==================================================")
    print("      ERITORA WIKI - FINAL SMOKE TEST (v1.3)      ")
    print("==================================================")
    
    steps = [
        ("Source Compatibility", ".venv/bin/python scripts/reconcile_content.py"),
        ("Source Integrity    ", ".venv/bin/python scripts/validate_source.py"),
        ("Redirects Check     ", ".venv/bin/python scripts/verify_redirects.py --limit 20"),
        ("Search Index Check  ", ".venv/bin/python scripts/verify_search.py"),
        ("Asset Audit         ", ".venv/bin/python scripts/audit_assets.py"),
    ]
    
    failures = []
    
    for desc, cmd in steps:
        success, output = run_step(desc, cmd)
        if not success:
            failures.append(desc)
            
    print("\n==================================================")
    if not failures:
        print("🟢 VERDICT: GO FOR LAUNCH (All checks passed)")
        sys.exit(0)
    else:
        print(f"🔴 VERDICT: NO-GO ({len(failures)} failures)")
        for f in failures:
            print(f"   - {f.strip()}")
        sys.exit(1)

if __name__ == "__main__":
    main()
