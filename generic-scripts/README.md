# Generic Confluence Scripts

This directory contains standalone scripts that can be used from any repository to create and update Confluence pages. These scripts are designed to be simple to use and require minimal setup.

## Prerequisites

1. **Python 3.6+** installed
2. **requests** library: `pip install requests`
3. **Confluence API credentials** (see Setup below)

## Setup

### 1. Set Environment Variables

Set these environment variables before using the scripts:

```bash
export CONFLUENCE_DOMAIN='yoursite.atlassian.net'
export CONFLUENCE_EMAIL='your-email@example.com'
export CONFLUENCE_API_TOKEN='your-api-token'

# Optional: Set default space ID
export CONFLUENCE_SPACE_ID='123456'
```

Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens

### 2. Clone or Copy Scripts

You can either:
- Clone this entire repository
- Copy just the `generic-scripts` directory
- Download individual scripts as needed

## Available Scripts

### 1. create_confluence_page.py

Create new Confluence pages with support for Markdown, HTML, and various input methods.

#### Basic Usage

```bash
# Create page from Markdown file
python create_confluence_page.py --space-id 123456 --title "My Page" --file content.md

# Create page from HTML file
python create_confluence_page.py --space-id 123456 --title "My Page" --file content.html

# Create page with inline content
python create_confluence_page.py --space-id 123456 --title "My Page" --content "Hello World"

# Create page from stdin
echo "# Hello World" | python create_confluence_page.py --space-id 123456 --title "My Page"

# Create child page
python create_confluence_page.py --space-id 123456 --title "Child Page" --parent-id 789012 --file content.md
```

#### Options

- `--space-id`: Space ID where page will be created (overrides CONFLUENCE_SPACE_ID env var)
- `--title`: Page title (required)
- `--file`: Read content from file
- `--content`: Inline content
- `--parent-id`: Create as child of specified page
- `--format`: Content format (`storage`, `markdown`, `auto`)
- `--modern-editor`: Use modern editor (default: True)
- `--json`: Output result as JSON
- `--dry-run`: Show what would be created without creating

### 2. update_confluence_page.py

Update existing Confluence pages with new content or append/prepend to existing content.

#### Basic Usage

```bash
# Update page by ID
python update_confluence_page.py --page-id 123456 --file updated.md

# Update page title and content
python update_confluence_page.py --page-id 123456 --title "New Title" --file content.html

# Find page by title and update
python update_confluence_page.py --space-id 789 --find-title "My Page" --file content.md

# Append content to existing page
python update_confluence_page.py --page-id 123456 --append --content "Additional section"

# Prepend content
python update_confluence_page.py --page-id 123456 --prepend --file header.md

# Update from stdin
echo "# Updated Content" | python update_confluence_page.py --page-id 123456
```

#### Options

- `--page-id`: Page ID to update
- `--find-title`: Find page by title (requires `--space-id`)
- `--space-id`: Space ID for title search
- `--file`: Read content from file
- `--content`: Inline content
- `--title`: New page title (optional)
- `--append`: Append content instead of replacing
- `--prepend`: Prepend content instead of replacing
- `--format`: Content format (`storage`, `markdown`, `auto`)
- `--version-message`: Comment for version history
- `--json`: Output result as JSON
- `--dry-run`: Show what would be updated without updating

### 3. markdown_to_storage.py

Convert Markdown files to Confluence storage format. Useful for previewing conversions or pre-processing.

#### Basic Usage

```bash
# Convert file
python markdown_to_storage.py input.md > output.html

# Convert from stdin
echo "# Hello World" | python markdown_to_storage.py

# Save to file
python markdown_to_storage.py input.md -o output.html

# Show supported syntax
python markdown_to_storage.py --show-syntax
```

#### Supported Markdown

- Headers (h1-h6)
- Bold, italic, bold+italic
- Inline code and code blocks with syntax highlighting
- Links and images
- Ordered and unordered lists (nested)
- Tables
- Blockquotes
- Horizontal rules
- Task lists
- Special Confluence panels (info, warning, note, success)

## Integration Examples

### From a Makefile

```makefile
# Variables
CONFLUENCE_SPACE_ID := 123456
DOC_TITLE := "API Documentation"

# Create documentation page
publish-docs:
    python path/to/create_confluence_page.py \
        --space-id $(CONFLUENCE_SPACE_ID) \
        --title $(DOC_TITLE) \
        --file docs/api.md

# Update existing documentation
update-docs:
    python path/to/update_confluence_page.py \
        --space-id $(CONFLUENCE_SPACE_ID) \
        --find-title $(DOC_TITLE) \
        --file docs/api.md
```

### From a Shell Script

```bash
#!/bin/bash

# Generate documentation
generate_docs.py > docs.md

# Publish to Confluence
python /path/to/create_confluence_page.py \
    --space-id $CONFLUENCE_SPACE_ID \
    --title "Build $(date +%Y-%m-%d)" \
    --file docs.md \
    --json > result.json

# Check if successful
if [ $? -eq 0 ]; then
    echo "Documentation published successfully"
    PAGE_URL=$(jq -r .url result.json)
    echo "View at: $PAGE_URL"
else
    echo "Failed to publish documentation"
    exit 1
fi
```

### From Python

```python
import subprocess
import json

def publish_to_confluence(title, content, space_id):
    """Publish content to Confluence."""
    result = subprocess.run([
        'python', 'path/to/create_confluence_page.py',
        '--space-id', str(space_id),
        '--title', title,
        '--content', content,
        '--json'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        raise Exception(f"Failed to create page: {result.stderr}")

# Usage
page_info = publish_to_confluence(
    "Automated Report",
    "# Report\n\nGenerated automatically.",
    123456
)
print(f"Created page: {page_info['url']}")
```

### From GitHub Actions

```yaml
name: Publish Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: pip install requests
      
      - name: Publish to Confluence
        env:
          CONFLUENCE_DOMAIN: ${{ secrets.CONFLUENCE_DOMAIN }}
          CONFLUENCE_EMAIL: ${{ secrets.CONFLUENCE_EMAIL }}
          CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
          CONFLUENCE_SPACE_ID: ${{ secrets.CONFLUENCE_SPACE_ID }}
        run: |
          python scripts/create_confluence_page.py \
            --title "Documentation - ${{ github.sha }}" \
            --file docs/README.md
```

## Advanced Usage

### Handling Errors

All scripts return exit code 0 on success and 1 on failure. Use `--json` flag for structured output:

```bash
# Check result in bash
if python create_confluence_page.py --space-id 123 --title "Test" --content "Hello" --json > result.json; then
    echo "Success! Page URL: $(jq -r .url result.json)"
else
    echo "Failed: $(jq -r .error result.json)"
fi
```

### Markdown Conversion

The scripts automatically detect and convert Markdown files (`.md` or `.markdown` extensions). For explicit control:

```bash
# Force markdown conversion
python create_confluence_page.py --format markdown --file content.txt

# Prevent conversion (treat as HTML)
python create_confluence_page.py --format storage --file content.md
```

### Dry Run Mode

Test your commands without making changes:

```bash
# See what would be created
python create_confluence_page.py --space-id 123 --title "Test" --file content.md --dry-run

# See what would be updated
python update_confluence_page.py --page-id 456 --file new.md --dry-run
```

## Troubleshooting

### Authentication Errors

1. Verify your API token is valid
2. Check the domain includes `.atlassian.net`
3. Ensure your user has permissions in the space

### Page Not Found

- For updates: Verify the page ID is correct
- For title search: Ensure exact title match and correct space ID

### Content Formatting Issues

- Use `markdown_to_storage.py` to preview conversions
- Check for unsupported HTML in storage format
- Ensure proper escaping of special characters

### Rate Limiting

The scripts handle rate limiting automatically with retries and backoff.

## Support

For issues specific to these scripts, please check:
1. Error messages (use `--json` for detailed errors)
2. Environment variables are set correctly
3. Network connectivity to Confluence
4. API permissions for your user

For Confluence API issues: https://support.atlassian.com/