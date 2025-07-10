# Confluence Tool

A comprehensive toolkit for working with the Confluence Cloud REST API v2, featuring organized documentation, Python scripts, and utilities for common operations.

## Overview

This repository provides:
- **Complete API Documentation** - AI-optimized reference for all Confluence v2 endpoints
- **Python Client Library** - Full-featured client with pagination, error handling, and rate limiting
- **Practical Scripts** - Ready-to-use utilities for common Confluence tasks
- **Postman Collection** - Import `confcloud.2.postman.json` for API testing

## Quick Start

### 1. Set Up Authentication

Run the interactive setup script:
```bash
./setup_env.sh
```

This will create a `.env` file with your credentials. Alternatively, you can:

```bash
# Copy and edit the example file
cp .env.example .env
# Edit .env with your values
```

Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens

For detailed setup and testing instructions, see [TESTING.md](TESTING.md)

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Basic Usage

```python
from scripts.confluence_client import ConfluenceClient

# Initialize client
client = ConfluenceClient(
    domain="your-domain.atlassian.net",
    email="your-email@example.com", 
    api_token="your-api-token"
)

# Create a page (with modern editor support)
page = client.create_page_modern_editor(
    space_id=123456,
    title="My New Page",
    content="<h1>Hello World</h1><p>Created via API!</p>"
)

# Or use legacy editor method
page = client.create_page(
    space_id=123456,
    title="My New Page",
    content="<h1>Hello World</h1><p>Created via API!</p>"
)

# Search pages
results = client.search_pages("space = DEMO AND title ~ 'API'")
```

## Repository Structure

```
confluence-tool/
├── docs/
│   ├── api-reference/          # Comprehensive API documentation
│   │   ├── overview.md         # API overview and authentication
│   │   ├── core/               # Core content APIs
│   │   │   ├── pages.md        # Page operations
│   │   │   ├── blog-posts.md   # Blog post operations
│   │   │   ├── attachments.md  # File attachments
│   │   │   └── comments.md     # Comments and discussions
│   │   ├── content/            # Advanced content types
│   │   │   ├── whiteboards.md  # Whiteboard operations
│   │   │   └── databases.md    # Database operations
│   │   └── space/              # Space management
│   │       ├── spaces.md       # Space operations
│   │       └── permissions.md  # Permission management
│   └── guides/                 # How-to guides
├── scripts/
│   ├── confluence_client.py    # Main Python client library
│   ├── test_connection.py      # Test your API connection
│   ├── test_formatting.py      # Create a test page with formatting
│   ├── examples/               # Example scripts
│   │   ├── page_operations.py  # Page CRUD examples
│   │   └── content_migration.py # Migration utilities
│   └── utilities/              # Advanced utilities
│       ├── bulk_operations.py  # Bulk content operations
│       └── space_admin.py      # Space administration
├── .env.example                # Environment variable template
├── setup_env.sh               # Interactive setup script
├── TESTING.md                 # Testing guide
└── confcloud.2.postman.json   # Postman collection

```

## Script Documentation

### Core Client (`scripts/confluence_client.py`)

The main Python client provides a comprehensive interface to the Confluence API:

```python
# Page operations
create_page(space_id, title, content, parent_id=None)
create_page_modern_editor(space_id, title, content, parent_id=None)  # Enables modern editor
get_page(page_id, expand=['body.storage'])
update_page(page_id, title, content, version)
delete_page(page_id)
search_pages(cql_query, limit=None)

# Blog posts
create_blog_post(space_id, title, content)
get_blog_post(post_id)

# Attachments
upload_attachment(page_id, file_path, comment=None)
get_attachments(page_id)
download_attachment(attachment_id, save_path)

# Spaces
get_spaces(limit=None)
get_space(space_id)
create_space(key, name, description=None)

# Comments
add_comment(page_id, content, parent_id=None)
get_comments(page_id)

# Labels
add_labels(page_id, labels)
get_labels(page_id)
```

### Example Scripts

#### Page Operations (`scripts/examples/page_operations.py`)

Demonstrates common page operations:
- Creating simple pages and hierarchies
- Adding tables, macros, and rich content
- Updating and labeling pages
- Searching with CQL queries

```bash
python scripts/examples/page_operations.py
```

#### Content Migration (`scripts/examples/content_migration.py`)

Tools for migrating content:
- Migrate entire spaces between instances
- Export spaces to JSON backup
- Import content from JSON
- Preserve page hierarchies and attachments

```bash
python scripts/examples/content_migration.py
```

### Utility Scripts

#### Bulk Operations (`scripts/utilities/bulk_operations.py`)

Perform operations on multiple pages:
- Create pages from CSV files
- Bulk update content
- Find and replace across spaces
- Archive old pages
- Generate index pages
- Export to Markdown

```python
from scripts.utilities.bulk_operations import BulkOperations

bulk = BulkOperations(client)

# Create pages from CSV
bulk.create_pages_from_csv('pages.csv', space_id=123456)

# Find and replace
bulk.find_and_replace_content('DEMO', 'old text', 'new text')

# Archive old content
bulk.archive_old_pages('DEMO', days_old=365)
```

#### Space Administration (`scripts/utilities/space_admin.py`)

Administrative tools for spaces:
- Create project spaces with standard structure
- Clone space structures
- Audit content and find issues
- Generate comprehensive reports
- Backup configurations

```python
from scripts.utilities.space_admin import SpaceAdmin

admin = SpaceAdmin(client)

# Create project space
space = admin.create_project_space(
    "New Project",
    "Project description",
    ["team@example.com"]
)

# Audit space
audit = admin.audit_space_content(space_id)

# Generate report
admin.generate_space_report(space_id, "report.html")
```

## API Documentation

The `docs/api-reference/` directory contains comprehensive documentation for all Confluence v2 API endpoints, optimized for AI consumption:

- **[Overview](docs/api-reference/overview.md)** - Authentication, base URL, common patterns
- **[Pages API](docs/api-reference/core/pages.md)** - Complete page operations reference
- **[Blog Posts API](docs/api-reference/core/blog-posts.md)** - Blog content management
- **[Attachments API](docs/api-reference/core/attachments.md)** - File upload and management
- **[Comments API](docs/api-reference/core/comments.md)** - Comment threads and inline comments
- **[Spaces API](docs/api-reference/space/spaces.md)** - Space creation and management
- **[Permissions API](docs/api-reference/space/permissions.md)** - Access control
- **[Whiteboards API](docs/api-reference/content/whiteboards.md)** - Visual collaboration
- **[Databases API](docs/api-reference/content/databases.md)** - Structured data
- **[v2 API Changes](docs/api-reference/v2-changes.md)** - Important changes from v1
- **[v2 API Limitations](docs/api-reference/v2-limitations.md)** - Critical limitations to be aware of

Each documentation file includes:
- Complete endpoint listings
- Request/response examples
- Query parameters and expansions
- Error handling patterns
- Best practices
- Code examples in multiple languages

## Common Use Cases

### 1. Automated Documentation

```python
# Create documentation structure
parent = client.create_page(space_id, "API Documentation", "<h1>API Docs</h1>")

for endpoint in api_endpoints:
    client.create_page(
        space_id=space_id,
        title=endpoint['name'],
        content=generate_docs(endpoint),
        parent_id=parent['id']
    )
```

### 2. Content Templates

```python
# Create page from template
template = client.get_page(template_id)
new_page = client.create_page(
    space_id=space_id,
    title=f"Weekly Report - {date.today()}",
    content=template['body']['storage']['value'].replace('{{DATE}}', str(date.today()))
)
```

### 3. Backup and Restore

```python
# Backup space
migrator = ContentMigrator(client)
migrator.export_space_to_json(space_id, "backup.json")

# Restore to new space
migrator.import_from_json("backup.json", new_space_id)
```

### 4. Bulk Updates

```python
# Update all pages with old branding
bulk = BulkOperations(client)
bulk.find_and_replace_content(
    space_key='DOCS',
    find_text='OldCompany',
    replace_text='NewCompany',
    dry_run=False
)
```

## Best Practices

1. **Authentication**
   - Use API tokens, not passwords
   - Store credentials in environment variables
   - Never commit credentials to git

2. **Rate Limiting**
   - The client handles rate limits automatically
   - Default limit: 10 requests/second per user
   - Implements exponential backoff on 429 errors

3. **Pagination**
   - Use the client's `_paginate()` method for large result sets
   - Default page size: 25 items
   - Maximum page size: 250 items

4. **Error Handling**
   - Check HTTP status codes
   - Log errors for debugging
   - Implement retries for transient failures

5. **Performance**
   - Use bulk operations when possible
   - Cache frequently accessed data
   - Minimize API calls with proper expansions

## Environment Variables

```bash
# Required
CONFLUENCE_DOMAIN=your-domain.atlassian.net
CONFLUENCE_EMAIL=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token

# Optional
CONFLUENCE_SPACE_ID=123456
CONFLUENCE_SPACE_KEY=DEMO
```

## Troubleshooting

### Authentication Errors
- Verify your API token is valid
- Check the domain name (include `.atlassian.net`)
- Ensure your user has necessary permissions

### Rate Limiting
- The client automatically handles rate limits
- For bulk operations, consider using concurrent workers
- Monitor the `X-RateLimit-*` response headers

### Content Formatting
- Use Confluence storage format for content
- HTML must be well-formed
- Special characters need proper encoding

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE.md for details

## Support

For API issues: https://support.atlassian.com/
For this toolkit: Create an issue on GitHub