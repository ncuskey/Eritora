import requests
import re
import sys
from concurrent.futures import ThreadPoolExecutor

SITEMAP_URL = "https://eritora.wiki/sitemap.xml"
BASE_URL = "https://eritora.wiki/"

EXTRA_URLS = [
    "https://eritora.wiki/St.%20Timothy's%20Cathedral/",
    "https://eritora.wiki/adventuring-academy/",
    "https://eritora.wiki/7.%20Items/adventuring-academy/" 
]

def check_url(args):
    url, homepage_size = args
    try:
        # Use simple GET to check content length and effective URL
        r = requests.get(url, timeout=10, allow_redirects=True)
        size = len(r.content)
        
        # Check if it served the homepage (Soft 404)
        is_homepage = (size == homepage_size)
        
        if r.status_code != 200:
            print(f"[FAIL] {url} - Status {r.status_code}")
        elif url != BASE_URL and is_homepage:
            print(f"[SOFT 404] {url} - Served Homepage (Size {size})")
        else:
            # print(f"[OK] {url}")
            pass
            
    except Exception as e:
        print(f"[ERROR] {url} - {e}")

def main():
    print(f"Fetching Homepage Baseline: {BASE_URL}")
    try:
        r_home = requests.get(BASE_URL)
        homepage_size = len(r_home.content)
        print(f"Homepage Size: {homepage_size} bytes")
    except Exception as e:
        print(f"Failed to fetch homepage: {e}")
        return

    print(f"Fetching sitemap: {SITEMAP_URL}")
    try:
        r = requests.get(SITEMAP_URL)
        urls = re.findall(r'<loc>(.*?)</loc>', r.text)
        print(f"Found {len(urls)} Canonical URLs.")
    except Exception as e:
        print(f"Failed to fetch sitemap: {e}")
        urls = []

    all_urls = urls + EXTRA_URLS
    print(f"Validating {len(all_urls)} URLs...")

    with ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(check_url, [(u, homepage_size) for u in all_urls]))
    
    print("Validation Complete.")

if __name__ == "__main__":
    main()
