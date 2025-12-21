import subprocess
import json
import urllib.request
import xml.etree.ElementTree as ET
import re
import time

def get_arxiv_metadata(paper_id):
    clean_id = paper_id.split('v')[0]
    url = f"https://export.arxiv.org/api/query?id_list={clean_id}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            entry = root.find('atom:entry', ns)
            if entry is None or entry.find('atom:title', ns) is None: return None
            
            # Fetch tags (categories)
            primary_cat = entry.find('arxiv:primary_category', ns)
            tags = [cat.get('term') for cat in entry.findall('atom:category', ns)]
            
            return {
                "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                "authors": [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)],
                "abstract": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
                "publishedDate": entry.find('atom:published', ns).text.split('T')[0],
                "tags": tags,
                "arxiv_tags": tags # Set both for compatibility
            }
    except: return None

def main():
    print("=== ArXiv Enrichment: Tag Support Enabled ===")
    try:
        res = subprocess.run(['gh', 'issue', 'list', '--label', 'stored-object', '--state', 'all', '--json', 'number,body'], 
                             capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
    except: return

    updates = 0
    for issue in issues:
        body = issue.get('body', '').strip()
        if not body.startswith('{'): continue
            
        try:
            data = json.loads(body)
            if 'interactions' in data and 'url' not in data: continue

            paper_id = data.get('paperId')
            title = data.get('title', '')
            tags = data.get('tags', [])
            
            # Extract ID from URL if missing
            if not paper_id and 'url' in data:
                match = re.search(r'(\d{4}\.\d{4,5})', data['url'])
                if match: paper_id = match.group(1)

            # Enrich if Title or Tags are missing
            needs_enrichment = paper_id and (not title or title.lower() in ['untitled', ''] or not tags)

            if needs_enrichment:
                print(f"Enriching Issue #{issue['number']} (ID: {paper_id})...")
                meta = get_arxiv_metadata(paper_id)
                if meta:
                    data.update(meta)
                    subprocess.run(['gh', 'issue', 'edit', str(issue['number']), '--body', json.dumps(data, indent=2)], check=True)
                    print(f"  [SUCCESS] Tags found: {', '.join(meta['tags'])}")
                    updates += 1
                    time.sleep(1)
        except: continue

    print(f"=== Enrichment Finished. {updates} updated. ===")

if __name__ == "__main__": 
    main()