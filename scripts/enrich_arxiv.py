import subprocess
import json
import urllib.request
import xml.etree.ElementTree as ET
import os

def get_arxiv_metadata(paper_id):
    # Handle versioned IDs (e.g., 2511.09744v1)
    clean_id = paper_id.split('v')[0]
    url = f"http://export.arxiv.org/api/query?id_list={clean_id}"
    try:
        with urllib.request.urlopen(url) as response:
            xml_data = response.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            
            # ArXiv API uses Atom format
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', ns)
            if entry is None: 
                print(f"No entry found for {clean_id}")
                return None
            
            title_node = entry.find('atom:title', ns)
            if title_node is None or title_node.text is None:
                return None
                
            title = title_node.text.strip().replace('\n', ' ')
            abstract = entry.find('atom:summary', ns).text.strip()
            authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
            published = entry.find('atom:published', ns).text.split('T')[0]
            
            return {
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "publishedDate": published
            }
    except Exception as e:
        print(f"Error fetching arXiv metadata for {paper_id}: {e}")
        return None

def main():
    print("Starting arXiv enrichment script...")
    
    # Get issues with label 'stored-object'
    try:
        res = subprocess.run(['gh', 'issue', 'list', '--label', 'stored-object', '--state', 'open', '--json', 'number,body', '--limit', '100'], 
                             capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
    except Exception as e:
        print(f"Error listing issues: {e}")
        return

    enriched_count = 0
    for issue in issues:
        body = issue['body']
        try:
            # gh-store saves data inside ```json blocks
            if '```json' in body:
                parts = body.split('```json')
                json_part = parts[1].split('```')[0].strip()
                data = json.loads(json_part)
            else:
                # Fallback: maybe the whole body is JSON?
                data = json.loads(body.strip())
                json_part = body.strip()
            
            # Check if it's an arxiv paper missing a title
            if data.get('sourceId') == 'arxiv' and (not data.get('title') or data.get('title') == 'Untitled'):
                paper_id = data.get('paperId')
                if not paper_id: continue
                
                print(f"Found untitled paper: {paper_id} (Issue #{issue['number']})")
                
                meta = get_arxiv_metadata(paper_id)
                if meta:
                    data.update(meta)
                    # Update issue body
                    new_json = json.dumps(data, indent=2)
                    
                    if '```json' in body:
                        new_body = body.replace(json_part, new_json)
                    else:
                        new_body = new_json
                    
                    subprocess.run(['gh', 'issue', 'edit', str(issue['number']), '--body', new_body], check=True)
                    print(f"Successfully enriched {paper_id}")
                    enriched_count += 1
                else:
                    print(f"Could not find metadata for {paper_id}")
                    
        except Exception as e:
            print(f"Error processing issue #{issue['number']}: {e}")

    print(f"Enrichment finished. {enriched_count} papers updated.")

if __name__ == "__main__":
    main()
