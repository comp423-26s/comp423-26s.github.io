---
title: Foundations of Software Engineering
hide:
  - navigation
---

# Agenda {: #agenda-title}

<table data-timeline="course">
  <thead>
    <tr>
      <th scope="col">Topic</th>
      <th scope="col">Due</th>
      <th scope="col">Threads</th>
    </tr>
  </thead>
  <tbody>
  {% set ns = namespace(prev_date=None) %}
  {% for item in get_recent_and_upcoming() %}
    {% if ns.prev_date != item.date %}
    <tr class="timeline-date-row">
      <td colspan="3" class="timeline-date-cell">{{ item.date | format_timeline_date }}</td>
    </tr>
    {% set ns.prev_date = item.date %}
    {% endif %}
    <tr class="timeline-item-row" data-date="{{ item.date }}"{% if item.due %} data-due="{{ item.due }}"{% endif %}>
      <td>
        <strong>{{ item.code }}</strong>
        <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
        {% if item.links %}
        <span class="timeline-links-container">({% for link in item.links %}<a href="{{ link.url }}" target="_blank" title="{{ link.title }}" class="timeline-link">{{ link.title }}</a>{% if not loop.last %}, {% endif %}{% endfor %})</span>
        {% endif %}
      </td>
      <td class="timeline-due">{% if item.due %}{{ item.due | format_due_date }}{% endif %}</td>
      <td>{{ item.threads | format_threads }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>