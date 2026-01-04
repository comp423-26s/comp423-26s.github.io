(function () {
  "use strict";

  const timeline = document.querySelector('table[data-timeline="course"]');
  if (!timeline) return;

  // --- 1. Setup UI Components ---

  // Create Filter UI (Due Soon)
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

  // Create Tabs UI
  const tabsContainer = document.createElement('div');
  tabsContainer.className = 'timeline-tabs';
  tabsContainer.innerHTML = `
    <button class="timeline-tab active" data-tab="upcoming">Now</button>
    <button class="timeline-tab" data-tab="past">Past</button>
  `;
  timeline.parentNode.insertBefore(tabsContainer, timeline);

  // --- 2. Data Parsing & State ---

  const dueSoonCheckbox = document.getElementById('filter-due-soon');
  const tbody = timeline.querySelector('tbody');
  
  function parseISODate(iso) {
    if (!iso || typeof iso !== "string") return null;
    const m = iso.trim().match(/^([0-9]{4})-([0-9]{2})-([0-9]{2})$/);
    if (!m) return null;
    return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  }

  // Capture all item rows.
  const rawRows = Array.from(tbody.querySelectorAll('tr.timeline-item-row'));
  const items = rawRows.map(row => {
    const dateStr = row.getAttribute('data-date');
    const dueStr = row.getAttribute('data-due');
    const date = parseISODate(dateStr);
    const due = parseISODate(dueStr);
    const code = row.querySelector('td:first-child strong').textContent.trim();
    
    return {
      element: row,
      date: date,
      due: due,
      code: code
    };
  });

  // Hide original date rows permanently
  const originalDateRows = Array.from(tbody.querySelectorAll('tr.timeline-date-row'));
  originalDateRows.forEach(r => r.style.display = 'none');

  // Date Logic
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  const lastItemDate = items.length > 0 
    ? new Date(Math.max(...items.map(i => i.date.getTime())))
    : new Date(0);
  const isCourseOver = today > lastItemDate;

  const dayOfWeek = today.getDay(); // 0 (Sun) to 6 (Sat)
  // Calculate days since Monday. If today is Sunday (0), it's 6 days since Monday.
  // If today is Monday (1), it's 0 days.
  const daysSinceMonday = (dayOfWeek + 6) % 7;
  const mostRecentMonday = new Date(today);
  mostRecentMonday.setDate(today.getDate() - daysSinceMonday);

  const hasPastItems = items.some(item => item.date && item.date < mostRecentMonday);
  if (!hasPastItems) {
    const pastTab = tabsContainer.querySelector('[data-tab="past"]');
    if (pastTab) pastTab.style.display = 'none';
  }

  // State
  let currentTab = 'upcoming';

  // --- 3. Rendering Logic ---

  function render() {
    let visibleItems = [];

    // 1. Filter Logic
    if (isCourseOver) {
      visibleItems = [...items];
      tabsContainer.style.display = 'none';
      filterContainer.style.display = 'none';
    } else if (dueSoonCheckbox.checked) {
      // "Due Soon" mode: Show ALL items due in the future, ignoring tabs
      visibleItems = items.filter(item => item.due && item.due > today);
      tabsContainer.style.display = 'none';
    } else {
      // Normal mode: Filter by Tab
      tabsContainer.style.display = hasPastItems ? '' : 'none'; // Revert to CSS default (flex)
      filterContainer.style.display = '';
      if (currentTab === 'upcoming') {
        visibleItems = items.filter(item => item.date && item.date >= mostRecentMonday);
      } else {
        visibleItems = items.filter(item => item.date && item.date < mostRecentMonday);
      }
    }

    // 2. Sort Logic
    if (isCourseOver) {
      // Course Over: Chronological (Asc)
      visibleItems.sort((a, b) => {
        if (a.date.getTime() !== b.date.getTime()) return a.date.getTime() - b.date.getTime();
        return a.code.localeCompare(b.code);
      });
    } else if (dueSoonCheckbox.checked) {
      // Sort by Due Date (Ascending)
      visibleItems.sort((a, b) => {
         if (a.due && b.due && a.due.getTime() !== b.due.getTime()) return a.due.getTime() - b.due.getTime();
         return a.code.localeCompare(b.code);
      });
    } else if (currentTab === 'upcoming') {
      // Upcoming: Chronological (Asc)
      visibleItems.sort((a, b) => {
        if (a.date.getTime() !== b.date.getTime()) return a.date.getTime() - b.date.getTime();
        return a.code.localeCompare(b.code);
      });
    } else {
      // Past: Reverse chronological (Desc)
      visibleItems.sort((a, b) => {
        return b.date.getTime() - a.date.getTime();
      });
    }

    // 3. Render to DOM
    items.forEach(item => item.element.remove());
    tbody.innerHTML = '';

    let lastDateStr = '';
    
    const createHeader = (date) => {
      const tr = document.createElement('tr');
      tr.className = 'timeline-date-row';
      const td = document.createElement('td');
      td.colSpan = 3;
      td.className = 'timeline-date-cell';
      
      const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
      const dayName = days[date.getDay()];
      const month = date.getMonth() + 1;
      const dayOfMonth = date.getDate();
      
      td.textContent = `${dayName} ${month}/${dayOfMonth}`;
      tr.appendChild(td);
      return tr;
    };

    visibleItems.forEach(item => {
      if (!dueSoonCheckbox.checked) {
        const itemDateStr = item.date.toISOString().split('T')[0];
        if (itemDateStr !== lastDateStr) {
          tbody.appendChild(createHeader(item.date));
          lastDateStr = itemDateStr;
        }
      }
      
      item.element.style.display = '';
      tbody.appendChild(item.element);
    });
    
    if (visibleItems.length === 0) {
       const tr = document.createElement('tr');
       const td = document.createElement('td');
       td.colSpan = 3;
       td.style.textAlign = 'center';
       td.style.padding = '2rem';
       td.style.color = 'var(--md-default-fg-color--light)';
       td.textContent = 'No items found.';
       tr.appendChild(td);
       tbody.appendChild(tr);
    }
  }

  // --- 4. Event Listeners ---

  dueSoonCheckbox.addEventListener('change', () => {
    render();
  });

  tabsContainer.addEventListener('click', (e) => {
    if (e.target.classList.contains('timeline-tab')) {
      currentTab = e.target.getAttribute('data-tab');
      updateTabUI();
      render();
    }
  });

  function updateTabUI() {
    const tabs = tabsContainer.querySelectorAll('.timeline-tab');
    tabs.forEach(tab => {
      if (tab.getAttribute('data-tab') === currentTab) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });
  }

  render();
})();
