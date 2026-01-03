(function () {
  "use strict";

  // Self-gate: only run where the Timeline table exists.
  const timeline = document.querySelector('table[data-timeline="course"]');
  if (!timeline) return;

  function parseISODate(iso) {
    // Expect YYYY-MM-DD
    if (!iso || typeof iso !== "string") return null;
    const m = iso.trim().match(/^([0-9]{4})-([0-9]{2})-([0-9]{2})$/);
    if (!m) return null;
    const year = Number(m[1]);
    const monthIndex = Number(m[2]) - 1;
    const day = Number(m[3]);
    if (!Number.isFinite(year) || !Number.isFinite(monthIndex) || !Number.isFinite(day)) return null;
    return new Date(year, monthIndex, day);
  }

  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  const rows = timeline.querySelectorAll('tr.timeline-item-row[data-due]');
  for (const row of rows) {
    const dueStr = row.getAttribute("data-due");
    const dueDate = parseISODate(dueStr);
    if (!dueDate) continue;

    // "Still in the future" => strictly after today.
    if (dueDate.getTime() > today.getTime()) {
      row.classList.add("timeline-item-row--due-upcoming");
    }
  }
})();
