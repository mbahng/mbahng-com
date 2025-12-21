import subprocess
import json
import urllib.request
import xml.etree.ElementTree as ET
import re
import time

def get_arxiv_metadata(paper_id):
    clean_id = paper_id.split('v')[0]
    url = f"https://export.arxiv.org/api/query?id_list={clean_id}"
    print(f"    --> API Fetch: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            if entry is None or entry.find('atom:title', ns) is None: return None
            return {
                "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                "authors": [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)],
                "abstract": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
                "publishedDate": entry.find('atom:published', ns).text.split('T')[0]
            }
    except Exception as e:
        print(f"    [!] API Error: {e}")
        return None

def main():
    print("=== Metadata Enrichment Start ===")
    
    # CRITICAL: We check ALL issues (open and closed) because the previous workflow might have closed them.
    try:
        print("Fetching issues from GitHub...")
        res = subprocess.run(['gh', 'issue', 'list', '--label', 'stored-object', '--state', 'all', '--json', 'number,title,body', '--limit', '50'], 
                             capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
    except Exception as e:
        print(f"ERROR: Could not fetch issues: {e}")
        return

    print(f"Found {len(issues)} issues to check.")
    
    updates = 0
    for issue in issues:
        body = issue['body']
        if '```json' not in body: continue
        
        try:
            json_part = body.split('```json')[1].split('```')[0].strip()
            data = json.loads(json_part)
            
            title = data.get('title', '')
            is_arxiv = data.get('sourceId') == 'arxiv' or 'arxiv.org' in data.get('url', '')
            
            # Identify papers that need metadata
            if is_arxiv and (not title or title.lower() in ['untitled', '', 'none']):
                paper_id = data.get('paperId')
                if not paper_id:
                    match = re.search(r'(\d{4}\.\d{4,5})', data.get('url', ''))
                    if match: paper_id = match.group(1)
                
                if paper_id:
                    print(f"  - Enriching Issue #{issue['number']} (ID: {paper_id})")
                    meta = get_arxiv_metadata(paper_id)
                    if meta:
                        data.update(meta)
                        new_body = body.replace(json_part, json.dumps(data, indent=2))
                        subprocess.run(['gh', 'issue', 'edit', str(issue['number']), '--body', new_body], check=True)
                        print(f"    [+] Updated: {meta['title'][:50]}...")
                        updates += 1
                        time.sleep(1)
        except Exception as e:
            print(f"  [!] Skip Issue #{issue['number']}: {e}")

    print(f"=== Enrichment Finished. {updates} updated. ===")

if __name__ == "__main__":
    main()