# COMP423 Course Notes Site

This repository contains the source code for the COMP423 course notes website, built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

## Development Setup

### Prerequisites

*   Python 3.11+
*   Node.js 20+

### Installation

1.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Node.js dependencies (for accessibility testing):**

    ```bash
    npm install -g pa11y-ci
    ```

## Running the Development Server

To start the live-reloading docs server:

```bash
mkdocs serve
```

The site will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Accessibility Testing

We use `pa11y-ci` to ensure the site meets accessibility standards (WCAG 2.1 AA).

### Running Tests

You can run the accessibility tests using the helper script:

```bash
./scripts/test-a11y.sh
```

This script will:
1.  Check if the MkDocs server is running.
2.  If not, start it in the background.
3.  Run `pa11y-ci` against the sitemap.
4.  Clean up the background server process (if it started one).

### Configuration

*   **`.pa11yci`**: Configuration for the `pa11y-ci` runner (sitemap scan).
*   **`pa11y.json`**: Configuration for single-page `pa11y` runs.
*   **`docs/javascripts/accessibility-fixes.js`**: Custom JavaScript to fix accessibility issues dynamically (e.g., adding `aria-label` to code annotations).

### Common Issues & Fixes

*   **Empty Links**: Some theme elements (like code annotations) may generate empty links. We use `accessibility-fixes.js` to inject accessible names.
*   **Hidden Elements**: Some elements that are purely decorative or problematic for automated tools but accessible in practice may be hidden from the crawler via the `hideElements` configuration in `.pa11yci`.
