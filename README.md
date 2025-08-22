# Whoosh Search Demo

A demonstration project for searching static HTML pages such as FAQ entries using Python and Whoosh.

## Overview

This project contains a FAQ page for a fictional company. The FAQ is indexed using the Whoosh search library to enable fast text search.

## Files

- `faq.html` - The FAQ page with styling and JavaScript
- `search.py` - Python script that indexes and searches the FAQ
- `indexdir/` - Directory containing the Whoosh search index (created when first run)

## Usage

Run the search script to index the FAQ and start searching:

```bash
python search.py
```

The script will:
1. Parse all FAQ entries from `faq.html`
2. Create a search index in the `indexdir/` directory
3. Prompt you for search queries
4. Return the top 3 matching results

### Example Searches

- "ostrich wax" - Find information about ostrich waxing
- "elephant battery" - Find details about deterrent batteries
- "tomato children" - Find info about child-safe peelers
- "warranty" - Find warranty information
- "tomato OR wax"
- "m*y"

Type 'quit', 'exit', or 'q' to exit the search interface.

## Dependencies

- `whoosh` - Full-text search library
- `beautifulsoup4` - HTML parsing library
