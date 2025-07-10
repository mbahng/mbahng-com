pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.9.359/pdf.worker.min.js';

let total_page_count = 0; 
let pdfUrl = null; 
let promises = [];
const titles = document.getElementsByClassName('html_note_title')

for (let i = 0; i < titles.length; ++i) {
  pdfUrl = titles[i].children[0].href; 
  const promise = pdfjsLib.getDocument(pdfUrl).promise
  .then(function(pdf) {
    titles[i].children[0].children[0].textContent += ` (${pdf.numPages} pg.)`; 
    total_page_count += pdf.numPages;
    return pdf.numPages
  })
  .catch(function(error) {
    titles[i].children[0].children[0].textContent += ` (${0} pg.)`; 
    return 0; 
  });
  promises.push(promise)
}

// wrap all promises around a wrapper for all to resolve. 
// Then print the accumulated total_page_count. 
Promise.all(promises)
  .then(() => {
  let page_count = document.createElement("p"); 
  page_count.className = "intro_text";
  page_count.id = "total_page_count"; 
  page_count.textContent = `Total Pages : ${total_page_count}`; 
  page_count.style = "display: none;";

  let firstHtmlRow = document.querySelector('.html_row');
  firstHtmlRow.parentNode.insertBefore(page_count, firstHtmlRow);
  })
  .catch((error) => {
    console.error("An error occurred:", error);
  });

