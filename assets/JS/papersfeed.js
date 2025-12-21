// assets/JS/papersfeed.js
// Global variables
let table;
let allData = [];

// Utility function to normalize dates using Chrono
function normalizeDate(dateString) {
  if (!dateString) return null;
  try {
    const parsedDate = chrono.parseDate(dateString);
    if (parsedDate) return parsedDate.toISOString().split('T')[0];
    const fallbackDate = new Date(dateString);
    if (!isNaN(fallbackDate.getTime())) return fallbackDate.toISOString().split('T')[0];
    return dateString;
  } catch (error) { return dateString; }
}

// Simple text formatters
function formatTags(cell) {
  const tags = cell.getValue();
  if (!tags || !Array.isArray(tags)) return '';
  return tags.map(tag => `<span class="tag">${tag}</span>`).join(' ');
}

function formatReadingTime(cell) {
  const seconds = cell.getValue();
  if (!seconds) return '0';
  const mins = Math.floor(seconds / 60);
  return `${mins}m ${seconds % 60}s`;
}

function extractDomain(url) {
  try {
    const domain = new URL(url).hostname.replace('www.', '');
    return domain.split('.')[0];
  } catch (e) { return 'link'; }
}

function processComplexData(data) {
  const result = [];
  const objects = data.objects;
  const paperKeys = Object.keys(objects).filter(key => key.startsWith("paper:"));
  
  for (const paperKey of paperKeys) {
    const paperId = paperKey.split(':')[1];
    const paperRaw = objects[paperKey];
    const paperData = paperRaw.data;
    const interactionKey = `interactions:${paperId}`;
    const interactionData = objects[interactionKey] ? objects[interactionKey].data : null;
    
    let totalReadingTime = 0;
    let lastReadDate = null;
    
    if (interactionData && interactionData.interactions) {
      interactionData.interactions.forEach(i => {
        if (i.type === "reading_session") {
          totalReadingTime += i.data.duration_seconds || 0;
          const sessionDate = new Date(i.timestamp);
          if (!lastReadDate || sessionDate > lastReadDate) {
            lastReadDate = sessionDate;
          }
        }
      });
    }

    const finalLastRead = lastReadDate || new Date(paperRaw.meta.updated_at);
    const dateOptions = { year: 'numeric', month: 'long', day: 'numeric' };
    const dateString = finalLastRead.toLocaleDateString('en-US', dateOptions);

    // Clean abstract: Remove all newlines and multiple spaces
    const cleanAbstract = (paperData.abstract || 'No abstract available.')
      .replace(/\r?\n|\r/g, " ")
      .replace(/\s+/g, " ")
      .trim();

    result.push({
      paperKey: paperKey,
      id: paperId,
      source: paperData.sourceId || extractDomain(paperData.url),
      title: paperData.title || `Paper ${paperId}`,
      authors: Array.isArray(paperData.authors) ? paperData.authors.join(', ') : (paperData.authors || 'Unknown Authors'),
      abstract: cleanAbstract,
      published: normalizeDate(paperData.publishedDate) || 'N/A',
      readingTimeSeconds: totalReadingTime,
      lastRead: finalLastRead,
      lastReadString: dateString,
      tags: paperData.tags || paperData.arxiv_tags || [],
      url: paperData.url
    });
  }
  return result;
}

function initTable(data) {
  table = new Tabulator("#papers-table", {
    data: data,
    layout: "fitColumns",
    height: false,
    pagination: false,
    groupBy: "lastReadString",
    groupHeader: function(value){ return value; },
    groupStartOpen: true,
    groupToggleElement: false,
    initialSort: [{column: "lastRead", dir: "desc"}],
    columns: [
      {title: "Time Read", field: "readingTimeSeconds", width: 120, formatter: formatReadingTime},
      {title: "Title", field: "title", widthGrow: 5},
      {title: "Source", field: "source", width: 100},
      {title: "Published", field: "published", width: 120},
      {title: "Tags", field: "tags", widthGrow: 2, formatter: formatTags},
      {title: "lastRead", field: "lastRead", visible: false},
      {title: "lastReadString", field: "lastReadString", visible: false}
    ],
    rowFormatter: function(row) {
      const element = row.getElement();
      const data = row.getData();
      
      const existing = element.querySelector(".detail-view");
      if(existing) existing.remove();

      const detailHolder = document.createElement("div");
      detailHolder.className = "detail-view";
      detailHolder.innerHTML = `
        <div class="detail-content">
          <div class="detail-header-block">
            <a href="${data.url}" target="_blank" class="detail-title-link">
              <h3 class="detail-title">${data.title}</h3>
            </a>
            <div class="detail-authors">${data.authors}</div>
          </div>
          <div class="detail-abstract"><p>${data.abstract}</p></div>
        </div>
      `;
      
      detailHolder.addEventListener("click", (e) => e.stopPropagation());
      element.appendChild(detailHolder);
      
      element.addEventListener("click", function() {
        const isOpen = element.classList.contains("row-open");
        document.querySelectorAll('.tabulator-row.row-open').forEach(el => {
          if (el !== element) el.classList.remove('row-open');
        });
        
        if (isOpen) {
          element.classList.remove("row-open");
        } else {
          element.classList.add("row-open");
          // Re-render MathJax for the newly shown abstract
          if (window.MathJax && window.MathJax.typesetPromise) {
            window.MathJax.typesetPromise([detailHolder]);
          }
        }
      });
    }
  });

  window.papersFeedTable = table;
  document.querySelector(".loading").style.display = "none";
}

function setupEventListeners() {
  const searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    table.setFilter((data) => {
      return [data.title, data.authors, data.abstract].join(' ').toLowerCase().includes(term);
    });
  });
}

document.addEventListener("DOMContentLoaded", function() {
  fetch(`assets/json/gh-store-snapshot.json?v=${Date.now()}`)
    .then(res => res.json())
    .then(data => {
      allData = processComplexData(data);
      initTable(allData);
      setupEventListeners();
    })
    .catch(err => {
      document.querySelector(".loading").innerHTML = "Error loading data.";
    });
});