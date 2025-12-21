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
    print("=== Metadata Enrichment Debug Mode ===")
    try:
        res = subprocess.run(['gh', 'issue', 'list', '--label', 'stored-object', '--state', 'all', '--json', 'number,title,body', '--limit', '50'], 
                             capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
    except Exception as e:
        print(f"ERROR: Could not fetch issues: {e}")
        return

    print(f"Checking {len(issues)} issues...")
    
    updates = 0
    for issue in issues:
        body = issue['body']
        if '```json' not in body:
            continue
        
        try:
            json_part = body.split('```json')[1].split('```')[0].strip()
            data = json.loads(json_part)
            
            # DEBUG LOG
            paper_id = data.get('paperId', 'N/A')
            current_title = data.get('title', 'N/A')
            source = data.get('sourceId', 'N/A')
            print(f"Processing Issue #{issue['number']} | ID: {paper_id} | Title: '{current_title}' | Source: {source}")

            is_arxiv = source == 'arxiv' or 'arxiv.org' in data.get('url', '')
            
            # Broadened check for "Untitled"
            needs_fix = is_arxiv and (
                not current_title or 
                current_title.strip() == "" or 
                current_title.lower() in ['untitled', 'none', 'n/a', 'paper ' + paper_id]
            )

            if needs_fix:
                if paper_id == 'N/A':
                    match = re.search(r'(\d{4}\.\d{4,5})', data.get('url', ''))
                    if match: paper_id = match.group(1)
                
                if paper_id != 'N/A':
                    print(f"  [ACTION] Enriching {paper_id}...")
                    meta = get_arxiv_metadata(paper_id)
                    if meta:
                        data.update(meta)
                        new_body = body.replace(json_part, json.dumps(data, indent=2))
                        subprocess.run(['gh', 'issue', 'edit', str(issue['number']), '--body', new_body], check=True)
                        print(f"  [SUCCESS] Updated to: {meta['title'][:40]}")
                        updates += 1
                        time.sleep(1)
                    else:
                        print(f"  [FAILURE] Metadata not found on arXiv API.")
            else:
                if not is_arxiv:
                    print("  [SKIP] Not an arXiv paper.")
                else:
                    print("  [SKIP] Title already populated.")

        except Exception as e:
            print(f"  [!] Error parsing JSON in Issue #{issue['number']}: {e}")

    print(f"=== Finished. {updates} updated. ===")

if __name__ == "__main__": 
    main()
