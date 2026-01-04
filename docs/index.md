---
title: Course Dashboard
hide:
  - navigation
---

# CS Intro to Engineering Dashboard

Welcome to the course home. Below is a live view of recent and upcoming modules.

## 📅 Timeline

<table data-timeline="course">
  <thead>
    <tr>
      <th scope="col">Code</th>
      <th scope="col">Module</th>
      <th scope="col">Due</th>
      <th scope="col">Threads</th>
    </tr>
  </thead>
  <tbody>
  {% set ns = namespace(prev_date=None) %}
  {% for item in get_recent_and_upcoming() %}
    {% if ns.prev_date != item.date %}
    <tr class="timeline-date-row">
      <td colspan="4" class="timeline-date-cell">{{ item.date | format_timeline_date }}</td>
    </tr>
    {% set ns.prev_date = item.date %}
    {% endif %}
    <tr class="timeline-item-row"{% if item.due %} data-due="{{ item.due }}"{% endif %}>
      <td><strong>{{ item.code }}</strong></td>
      <td><a href="{{ item.url | relative_url }}">{{ item.title }}</a></td>
      <td class="timeline-due">{% if item.due %}{{ item.due | format_due_date }}{% endif %}</td>
      <td>{{ item.threads | format_threads }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>

## 🧠 Course Concepts
This course is built around several core threads. Click a thread to see all related materials.

* **Ethics**: Focus on responsible engineering...
* **Systems**: Understanding complex interactions...
