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
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            if entry is None: return None
            return {
                "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                "authors": [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)],
                "abstract": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
                "publishedDate": entry.find('atom:published', ns).text.split('T')[0]
            }
    except: return None

def main():
    print("=== ArXiv Enrichment: Extreme Debug Mode ===")
    try:
        res = subprocess.run(['gh', 'issue', 'list', '--label', 'stored-object', '--state', 'all', '--json', 'number,body', '--limit', '20'], 
                             capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
    except Exception as e:
        print(f"FAILED TO FETCH ISSUES: {e}")
        return

    print(f"Total issues found: {len(issues)}")
    
    updates = 0
    for issue in issues:
        num = issue['number']
        body = issue.get('body', '')
        
        print(f"\n--- Checking Issue #{num} ---")
        print(f"Body Preview (100 chars): {repr(body[:100])}")
        
        if '```json' not in body:
            print(f"  [!] No ```json block found in Issue #{num}. Skipping.")
            continue
            
        try:
            json_part = body.split('```json')[1].split('```')[0].strip()
            data = json.loads(json_part)
            
            paper_id = data.get('paperId', 'N/A')
            title = data.get('title', '')
            source = data.get('sourceId', '')
            
            print(f"  Data -> ID: {paper_id} | Title: '{title}' | Source: {source}")

            is_arxiv = source == 'arxiv' or 'arxiv.org' in data.get('url', '')
            if not is_arxiv:
                print("  [SKIP] Not an arXiv paper.")
                continue

            if title and title.lower() not in ['untitled', '', 'none']:
                print("  [SKIP] Title already present.")
                continue

            # Need fix
            if paper_id == 'N/A':
                match = re.search(r'(\d{4}\.\d{4,5})', data.get('url', ''))
                if match: paper_id = match.group(1)
            
            if paper_id != 'N/A':
                print(f"  [ACTION] Fetching metadata for {paper_id}...")
                meta = get_arxiv_metadata(paper_id)
                if meta:
                    data.update(meta)
                    new_body = body.replace(json_part, json.dumps(data, indent=2))
                    subprocess.run(['gh', 'issue', 'edit', str(num), '--body', new_body], check=True)
                    print(f"  [SUCCESS] Updated Issue #{num}")
                    updates += 1
                    time.sleep(1)
                else:
                    print("  [FAILURE] arXiv API returned no data.")
        except Exception as e:
            print(f"  [ERROR] Failed to process Issue #{num}: {e}")

    print(f"\n=== Enrichment Finished. {updates} updated. ===")

if __name__ == "__main__": 
    main()