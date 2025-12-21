import subprocess
import json
import urllib.request
import xml.etree.ElementTree as ET
import re
import time

def get_arxiv_metadata(paper_id):
    clean_id = paper_id.split('v')[0]
    # Use HTTPS and export subdomain
    url = f"https://export.arxiv.org/api/query?id_list={clean_id}"
    
    print(f"  --> Fetching from: {url}")
    
    # ArXiv sometimes blocks default python user-agents
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            
            if entry is None or entry.find('atom:title', ns) is None:
                print(f"  [!] No valid entry found in XML for {clean_id}")
                return None
            
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
            published = entry.find('atom:published', ns).text.split('T')[0]
            
            print(f"  [+] Found: {title}")
            return {
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "publishedDate": published
            }
    except Exception as e:
        print(f"  [!] Error: {e}")
        return None

def main():
    print("Starting arXiv metadata enrichment...")
    try:
        res = subprocess.run(['gh', 'issue', 'list', '--label', 'stored-object', '--state', 'open', '--json', 'number,body'], 
                             capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
    except Exception as e:
        print(f"Critical error listing issues: {e}")
        return

    print(f"Checking {len(issues)} stored objects...")
    
    updates_made = 0
    for issue in issues:
        body = issue['body']
        try:
            if '```json' not in body: continue
            json_part = body.split('```json')[1].split('```')[0].strip()
            data = json.loads(json_part)
            
            # Check if it's an arXiv paper missing metadata
            is_arxiv = data.get('sourceId') == 'arxiv' or 'arxiv.org' in data.get('url', '')
            needs_fix = is_arxiv and (not data.get('title') or data.get('title').lower() in ['untitled', ''])

            if needs_fix:
                paper_id = data.get('paperId')
                if not paper_id:
                    match = re.search(r'(\d{4}\.\d{4,5})', data.get('url', ''))
                    if match: paper_id = match.group(1)
                
                if paper_id:
                    print(f"Fixing Issue #{issue['number']} (ID: {paper_id})...")
                    meta = get_arxiv_metadata(paper_id)
                    if meta:
                        data.update(meta)
                        new_body = body.replace(json_part, json.dumps(data, indent=2))
                        subprocess.run(['gh', 'issue', 'edit', str(issue['number']), '--body', new_body], check=True)
                        updates_made += 1
                        time.sleep(1) # Be nice to the API
        except Exception as e:
            print(f"Error processing issue #{issue['number']}: {e}")

    print(f"Enrichment complete. {updates_made} issues updated.")

if __name__ == "__main__":
    main()
