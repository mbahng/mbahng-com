import json
import os
from bs4 import BeautifulSoup
from pypdf import PdfReader

def count_pages():
    base_dir = os.getcwd()
    index_path = os.path.join(base_dir, 'index.html')
    output_path = os.path.join(base_dir, 'assets/json/page_counts.json')
    
    # Read index.html
    with open(index_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    page_counts = {}
    total_pages = 0
    
    # Find all note links
    # Selector based on the JS: document.getElementsByClassName('html_note_title')
    note_titles = soup.find_all(class_='html_note_title')
    
    print(f"Found {len(note_titles)} note titles.")
    
    for title in note_titles:
        link = title.find('a')
        if not link or not link.has_attr('href'):
            continue
            
        href = link['href']
        
        # We only care about PDFs
        if not href.lower().endswith('.pdf'):
            continue
            
        # The hrefs in index.html are relative to the root (e.g., Natural_Sciences/...)
        # Construct absolute path
        file_path = os.path.join(base_dir, href)
        
        if os.path.exists(file_path):
            try:
                reader = PdfReader(file_path)
                num_pages = len(reader.pages)
                page_counts[href] = num_pages
                total_pages += num_pages
                print(f"Processed {href}: {num_pages} pages")
            except Exception as e:
                print(f"Error reading {href}: {e}")
                page_counts[href] = 0
        else:
            print(f"File not found: {href}")
            page_counts[href] = 0
            
    # Add total count
    page_counts['total_page_count'] = total_pages
    print(f"Total pages: {total_pages}")
    
    # Write to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(page_counts, f, indent=4)
        
    print(f"Wrote page counts to {output_path}")

if __name__ == "__main__":
    count_pages()
