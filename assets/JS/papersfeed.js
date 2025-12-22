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
    
    const sessionsByDay = new Map();
    
    if (interactionData && interactionData.interactions) {
      interactionData.interactions.forEach(i => {
        if (i.type === "reading_session") {
          const date = new Date(i.timestamp);
          const dateKey = date.toISOString().split('T')[0]; 
          
          if (!sessionsByDay.has(dateKey)) {
            sessionsByDay.set(dateKey, {
              dateISO: dateKey,
              actualLatestTimestamp: new Date(i.timestamp),
              duration: 0
            });
          }
          
          const dayData = sessionsByDay.get(dateKey);
          dayData.duration += (i.data.duration_seconds || 0);
          if (new Date(i.timestamp) > dayData.actualLatestTimestamp) {
            dayData.actualLatestTimestamp = new Date(i.timestamp);
          }
        }
      });
    }

    const commonMeta = {
      paperKey: paperKey,
      id: paperId,
      source: paperData.sourceId || extractDomain(paperData.url),
      title: paperData.title || `Paper ${paperId}`,
      authors: Array.isArray(paperData.authors) ? paperData.authors.join(', ') : (paperData.authors || 'Unknown Authors'),
      abstract: (paperData.abstract || 'No abstract available.').replace(/\r?\n|\r/g, " ").replace(/\s+/g, " ").trim(),
      published: normalizeDate(paperData.publishedDate) || 'N/A',
      tags: paperData.tags || paperData.arxiv_tags || [],
      url: paperData.url
    };

    if (sessionsByDay.size === 0) {
      const createdDate = new Date(paperRaw.meta.created_at);
      const dateKey = createdDate.toISOString().split('T')[0];
      result.push({
        ...commonMeta,
        readingTimeSeconds: 0,
        lastRead: createdDate.getTime(), // Use numeric timestamp
        groupDate: dateKey,
      });
    } else {
      sessionsByDay.forEach((dayInfo, dateKey) => {
        result.push({
          ...commonMeta,
          readingTimeSeconds: dayInfo.duration,
          lastRead: dayInfo.actualLatestTimestamp.getTime(), // Use numeric timestamp
          groupDate: dateKey
        });
      });
    }
  }
  
  // MANUAL SORT: Ensure data is strictly chronological before table init
  result.sort((a, b) => b.lastRead - a.lastRead);
  
  return result;
}

function initTable(data) {
  table = new Tabulator("#papers-table", {
    data: data,
    layout: "fitColumns",
    height: false,
    pagination: false,
    
    // Grouping Config
    groupBy: "groupDate", 
    groupHeader: function(value){
        const date = new Date(value + "T12:00:00"); 
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    },
    groupStartOpen: true,
    groupToggleElement: false,
    groupDir: "desc", // Keep this

    // Row Sorting
    initialSort: [
      {column: "lastRead", dir: "desc"}
    ],
    
    columns: [
      {title: "Time Read", field: "readingTimeSeconds", width: 120, formatter: formatReadingTime},
      {title: "Title", field: "title", widthGrow: 5},
      {title: "Source", field: "source", width: 100},
      {title: "Published", field: "published", width: 120},
      {title: "Tags", field: "tags", widthGrow: 2, formatter: formatTags},
      {title: "lastRead", field: "lastRead", visible: false, sorter:"number"}, // Changed from datetime to number
      {title: "groupDate", field: "groupDate", visible: false, sorter:"string"}
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
          <div class="detail-abstract" style="max-width: 80%; overflow-x: hidden;">
            <p style="max-width: 100%; word-break: break-word; white-space: normal;">${data.abstract}</p>
          </div>
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
