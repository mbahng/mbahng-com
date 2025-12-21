import subprocess
import json
import urllib.request
import xml.etree.ElementTree as ET
import re

def get_arxiv_metadata(paper_id):
    # Standardize ID
    clean_id = paper_id.split('v')[0]
    url = f"http://export.arxiv.org/api/query?id_list={clean_id}"
    try:
        with urllib.request.urlopen(url) as response:
            xml_data = response.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            if entry is None: return None
            
            title_node = entry.find('atom:title', ns)
            if title_node is None or title_node.text is None: return None
                
            return {
                "title": title_node.text.strip().replace('\n', ' '),
                "authors": [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)],
                "abstract": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
                "publishedDate": entry.find('atom:published', ns).text.split('T')[0]
            }
    except: return None

def main():
    print("Scanning for papers needing metadata enrichment...")
    try:
        res = subprocess.run(['gh', 'issue', 'list', '--label', 'stored-object', '--state', 'open', '--json', 'number,body'], 
                             capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
    except: return

    for issue in issues:
        body = issue['body']
        try:
            if '```json' not in body: continue
            json_part = body.split('```json')[1].split('```')[0].strip()
            data = json.loads(json_part)
            
            # Identify arXiv papers
            is_arxiv = data.get('sourceId') == 'arxiv' or 'arxiv.org' in data.get('url', '')
            
            # Check if metadata is missing (Title, Authors, or Abstract)
            needs_enrichment = is_arxiv and (
                not data.get('title') or 
                data.get('title').lower() in ['untitled', 'processing...', ''] or
                not data.get('authors') or
                not data.get('abstract')
            )

            if needs_enrichment:
                # Try to extract paper ID from URL if missing
                paper_id = data.get('paperId')
                if not paper_id:
                    match = re.search(r'(\d{4}\.\d{4,5})', data.get('url', ''))
                    if match: paper_id = match.group(1)
                
                if not paper_id: continue
                
                print(f"Enriching Issue #{issue['number']} (ID: {paper_id})...")
                meta = get_arxiv_metadata(paper_id)
                
                if meta:
                    data.update(meta)
                    new_body = body.replace(json_part, json.dumps(data, indent=2))
                    subprocess.run(['gh', 'issue', 'edit', str(issue['number']), '--body', new_body], check=True)
                    print(f"Done.")
        except: continue

if __name__ == "__main__":
    main()