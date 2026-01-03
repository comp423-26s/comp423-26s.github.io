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
      <th>Threads</th>
      <th>Code</th>
      <th>Module</th>
      <th>Due</th>
    </tr>
  </thead>
  <tbody>
  {% set ns = namespace(prev_date=None) %}
  {% for item in get_recent_and_upcoming() %}
    {% if ns.prev_date != item.date %}
    <tr class="timeline-date-row">
      <th colspan="4">{{ item.date | format_timeline_date }}</th>
    </tr>
    {% set ns.prev_date = item.date %}
    {% endif %}
    <tr class="timeline-item-row"{% if item.due %} data-due="{{ item.due }}"{% endif %}>
      <td>{{ item.threads | format_threads }}</td>
      <td><strong>{{ item.code }}</strong></td>
      <td><a href="{{ item.url | relative_url }}">{{ item.title }}</a></td>
      <td class="timeline-due">{% if item.due %}{{ item.due }}{% endif %}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>

## 🧠 Course Concepts
This course is built around several core threads. Click a thread to see all related materials.

* **Ethics**: Focus on responsible engineering...
* **Systems**: Understanding complex interactions...
