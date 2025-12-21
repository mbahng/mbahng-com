// assets/JS/papersfeed.js
// Global variables
let table;
let allData = [];
let currentDetailsPaper = null;

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
  return `<strong>${mins}m</strong> ${seconds % 60}s`;
}

function displayPaperDetails(paperId) {
  const paper = allData.find(p => p.paperKey === paperId);
  if (!paper) return;
  currentDetailsPaper = paper;
  const detailsSidebar = document.getElementById('details-sidebar');
  const detailsContent = document.getElementById('details-content');
  
  detailsContent.innerHTML = `
    <div class="details-header"><h2>${paper.title}</h2></div>
    <div class="detail-section">
      <h3>Details</h3>
      <table class="detail-table">
        <tr><th>Authors:</th><td>${paper.authors}</td></tr>
        <tr><th>Published:</th><td>${paper.published}</td></tr>
        <tr><th>Source:</th><td>${paper.source}</td></tr>
        <tr><th>Reading Time:</th><td>${Math.floor(paper.readingTimeSeconds/60)}m ${paper.readingTimeSeconds%60}s</td></tr>
        <tr><th>Tags:</th><td>${formatTags({ getValue: () => paper.tags })}</td></tr>
        <tr><th>URL:</th><td><a href="${paper.url}" target="_blank">Open ↗</a></td></tr>
      </table>
    </div>
    <div class="detail-section">
      <h3>Abstract</h3>
      <div class="abstract-box">${paper.abstract}</div>
    </div>
  `;
  detailsSidebar.classList.add('active');
}

function hideDetails() {
  document.getElementById('details-sidebar').classList.remove('active');
  currentDetailsPaper = null;
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
    if (interactionData && interactionData.interactions) {
      interactionData.interactions.forEach(i => {
        if (i.type === "reading_session") totalReadingTime += i.data.duration_seconds || 0;
      });
    }

    result.push({
      paperKey: paperKey,
      id: paperId,
      source: paperData.sourceId || extractDomain(paperData.url),
      title: paperData.title || `Paper ${paperId}`,
      authors: Array.isArray(paperData.authors) ? paperData.authors.join(', ') : (paperData.authors || 'Unknown Authors'),
      abstract: paperData.abstract || '',
      published: normalizeDate(paperData.publishedDate) || 'N/A',
      readingTimeSeconds: totalReadingTime,
      tags: paperData.tags || paperData.arxiv_tags || [],
      url: paperData.url,
      rawInteractionData: interactionData ? interactionData.interactions : []
    });
  }
  return result;
}

function initTable(data) {
  table = new Tabulator("#papers-table", {
    data: data,
    layout: "fitColumns",
    responsiveLayout: "collapse",
    pagination: "local",
    paginationSize: 20,
    initialSort: [{column: "readingTimeSeconds", dir: "desc"}],
    columns: [
      {title: "Time", field: "readingTimeSeconds", width: 100, formatter: formatReadingTime},
      {title: "Title", field: "title", widthGrow: 5},
      {title: "Source", field: "source", width: 100},
      {title: "Published", field: "published", width: 120},
      {title: "Tags", field: "tags", widthGrow: 2, formatter: formatTags}
    ]
  });

  window.papersFeedTable = table;
  document.querySelector(".loading").style.display = "none";
  
  document.getElementById("papers-table").addEventListener("click", function(e) {
    const row = e.target.closest(".tabulator-row");
    if (row) {
      const paperId = table.getRow(row).getData().paperKey;
      displayPaperDetails(paperId);
    }
  });
}

function setupEventListeners() {
  const searchInput = document.getElementById("search-input");
  const clearSearch = document.getElementById("clear-search");

  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    table.setFilter((data) => {
      return [data.title, data.authors, data.abstract].join(' ').toLowerCase().includes(term);
    });
  });

  clearSearch.addEventListener("click", () => {
    searchInput.value = "";
    table.clearFilter();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      hideDetails();
    }
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