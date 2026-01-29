#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
import argparse
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from collections import deque

class SiteAuditor:
    def __init__(self, start_url, max_pages=None, concurrency=10):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.concurrency = concurrency
        
        self.visited = set()
        self.queue = deque([start_url])
        self.broken_links = []
        self.assets_issues = []
        self.external_links = {} # url -> status
        
        self.lock = threading.Lock()
        self.processed_count = 0
        
        # User-Agent to avoid being blocked
        self.headers = {
            'User-Agent': 'EritoraWikiAuditor/1.0'
        }

    def is_internal(self, url):
        return urlparse(url).netloc == self.domain

    def normalize_url(self, url):
        # Remove fragment for crawling purposes, but keep for validation logic if needed later
        url, _ = urldefrag(url)
        return url

    def check_link(self, url):
        try:
            r = requests.head(url, headers=self.headers, timeout=5, allow_redirects=True)
            # Some servers don't like HEAD, fallback to GET
            if r.status_code == 405:
                 r = requests.get(url, headers=self.headers, timeout=5, stream=True)
            return r.status_code
        except Exception as e:
            return str(e)

    def process_page(self, url):
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            if r.status_code != 200:
                with self.lock:
                    self.broken_links.append({'source': 'N/A', 'target': url, 'status': r.status_code})
                return

            soup = BeautifulSoup(r.content, 'html.parser')
            
            # Find all links
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(url, href)
                links.append(full_url)

            # Find all assets (images, scripts, css)
            assets = []
            for img in soup.find_all('img', src=True):
                assets.append(urljoin(url, img['src']))
            for script in soup.find_all('script', src=True):
                assets.append(urljoin(url, script['src']))
            for link in soup.find_all('link', href=True):
                assets.append(urljoin(url, link['href']))

            # Validate Assets
            for asset in assets:
                status = self.check_link(asset)
                if status != 200:
                    with self.lock:
                        self.assets_issues.append({'page': url, 'asset': asset, 'status': status})

            # Process Links
            for link in links:
                normalized = self.normalize_url(link)
                
                if self.is_internal(normalized):
                    with self.lock:
                        if normalized not in self.visited:
                            self.visited.add(normalized)
                            self.queue.append(normalized)
                else:
                    # External link check
                    with self.lock:
                         if link not in self.external_links:
                             self.external_links[link] = None # Mark as seen to avoid duplicate checks in this run if optimizing
                    
                    # For this pass, let's just check it if we haven't
                    # (In a real heavy crawler we might batch these differently)
                    status = self.check_link(link)
                    if status != 200:
                         with self.lock:
                             self.broken_links.append({'source': url, 'target': link, 'status': status})

        except Exception as e:
            print(f"Error processing {url}: {e}")

    def run(self):
        print(f"Starting audit of {self.start_url}")
        self.visited.add(self.normalize_url(self.start_url))
        
        with ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            while self.queue or self.processed_count < (self.max_pages or float('inf')):
                # Simple BFS with thread pool
                futures = []
                while self.queue and len(futures) < self.concurrency * 2:
                     if self.max_pages and self.processed_count >= self.max_pages:
                         break
                     url = self.queue.popleft()
                     self.processed_count += 1
                     futures.append(executor.submit(self.process_page, url))
                
                if not futures and not self.queue:
                    break
                
                # Wait for this batch
                for f in futures:
                    f.result()
                    
                if self.max_pages and self.processed_count >= self.max_pages:
                    break

        self.report()

    def report(self):
        print("\n" + "="*50)
        print("AUDIT REPORT")
        print("="*50)
        print(f"Pages Scanned: {self.processed_count}")
        print(f"Broken Links Found: {len(self.broken_links)}")
        print(f"Asset Issues Found: {len(self.assets_issues)}")
        print("-" * 30)
        
        if self.broken_links:
            print("\nBROKEN LINKS:")
            for item in self.broken_links:
                print(f"  [{item['status']}] {item['target']} (from {item.get('source', 'unknown')})")
        
        if self.assets_issues:
            print("\nASSET ISSUES:")
            for item in self.assets_issues:
                print(f"  [{item['status']}] {item['asset']} (on {item['page']})")
        
        print("\n" + "="*50)

def main():
    parser = argparse.ArgumentParser(description='Audit a website for broken links and missing assets.')
    parser.add_argument('--url', default='https://eritora.wiki', help='Base URL to start crawling')
    parser.add_argument('--max-pages', type=int, help='Maximum pages to crawl')
    parser.add_argument('--concurrency', type=int, default=10, help='Number of concurrent threads')
    
    args = parser.parse_args()
    
    auditor = SiteAuditor(args.url, args.max_pages, args.concurrency)
    auditor.run()

if __name__ == "__main__":
    main()
