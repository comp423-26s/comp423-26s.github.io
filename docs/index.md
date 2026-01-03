---
title: Course Dashboard
hide:
  - navigation
---

# CS Intro to Engineering Dashboard

Welcome to the course home. Below is a live view of recent and upcoming modules.

## 📅 Timeline

<table>
  <thead>
    <tr>
      <th>Date</th>
      <th>Type</th>
      <th>Module</th>
      <th>Threads</th>
    </tr>
  </thead>
  <tbody>
  {% for item in get_recent_and_upcoming() %}
    <tr>
      <td>{{ item.date }}</td>
      <td><strong>{{ item.type }}</strong></td>
      <td><a href="{{ item.url | relative_url }}">{{ item.title }}</a></td>
      <td>{{ item.threads | format_threads }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>

## 🧠 Course Concepts
This course is built around several core threads. Click a thread to see all related materials.

* **Ethics**: Focus on responsible engineering...
* **Systems**: Understanding complex interactions...
