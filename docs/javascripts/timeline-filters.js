(function () {
  "use strict";

  const timeline = document.querySelector('table[data-timeline="course"]');
  if (!timeline) return;

  // Create filter UI
  const filterContainer = document.createElement('div');
  filterContainer.className = 'timeline-filter-container';
  filterContainer.innerHTML = `
    <div class="timeline-filter-item">
      <label class="timeline-switch">
        <input type="checkbox" id="filter-due-soon">
        <span class="timeline-switch-slider"></span>
      </label>
      <label for="filter-due-soon" class="timeline-filter-label">Due Soon</label>
    </div>
  `;

  const agendaTitle = document.getElementById('agenda-title');
  if (agendaTitle) {
    agendaTitle.after(filterContainer);
    filterContainer.classList.add('timeline-filter-container--inline');
  } else {
    timeline.parentNode.insertBefore(filterContainer, timeline);
  }

  const dueSoonCheckbox = document.getElementById('filter-due-soon');
  const tbody = timeline.querySelector('tbody');
  const originalRows = Array.from(tbody.querySelectorAll('tr'));

  function parseISODate(iso) {
    if (!iso || typeof iso !== "string") return null;
    const m = iso.trim().match(/^([0-9]{4})-([0-9]{2})-([0-9]{2})$/);
    if (!m) return null;
    return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  }

  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  function applyFilters() {
    const showDueSoonOnly = dueSoonCheckbox.checked;
    
    if (showDueSoonOnly) {
      // Filter to only upcoming items
      const visibleRows = originalRows.filter(row => {
        if (!row.classList.contains('timeline-item-row')) return false;
        const dueStr = row.getAttribute('data-due');
        const dueDate = parseISODate(dueStr);
        return dueDate && dueDate.getTime() > today.getTime();
      });

      // Sort by due date (asc) then Code (asc)
      visibleRows.sort((a, b) => {
        const dateA = parseISODate(a.getAttribute('data-due'));
        const dateB = parseISODate(b.getAttribute('data-due'));
        
        if (dateA.getTime() !== dateB.getTime()) {
          return dateA.getTime() - dateB.getTime();
        }
        
        const codeA = a.querySelector('td:first-child').textContent.trim();
        const codeB = b.querySelector('td:first-child').textContent.trim();
        return codeA.localeCompare(codeB);
      });

      // Hide all original rows
      originalRows.forEach(row => row.style.display = 'none');
      
      // Show and reorder visible rows
      visibleRows.forEach(row => {
        row.style.display = '';
        tbody.appendChild(row);
      });
    } else {
      // Restore original order and visibility
      originalRows.forEach(row => {
        row.style.display = '';
        tbody.appendChild(row);
      });
    }
  }

  dueSoonCheckbox.addEventListener('change', applyFilters);
})();
