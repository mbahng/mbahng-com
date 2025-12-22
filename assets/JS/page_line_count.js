fetch('assets/json/page_counts.json')
  .then(response => response.json())
  .then(data => {
    const titles = document.getElementsByClassName('html_note_title');
    
    for (let i = 0; i < titles.length; ++i) {
      const link = titles[i].children[0];
      const href = link.getAttribute('href');
      
      if (data[href] !== undefined) {
        if (link.children.length > 0) {
             link.children[0].textContent += ` [${data[href]} pg]`;
        } else {
             link.textContent += ` [${data[href]} pg]`;
        }
      }
    }
  })
  .catch(error => console.error('Error loading page counts:', error));

