# Confluence Pages API Reference

## Overview

The Confluence Pages API provides comprehensive functionality for creating, reading, updating, and deleting pages in Confluence spaces. Pages are the primary content units in Confluence and can contain rich text, images, macros, and attachments.

### Use Cases
- Automated documentation generation
- Content migration between spaces or instances
- Bulk page creation from external data sources
- Integration with CI/CD pipelines for documentation updates
- Content synchronization with external systems
- Programmatic page templates and structures

## Authentication Requirements

All Page API endpoints require authentication. Confluence supports multiple authentication methods:

### Basic Authentication
```bash
curl -u username:password https://your-domain.atlassian.net/wiki/rest/api/content
```

### API Token (Recommended for Atlassian Cloud)
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" https://your-domain.atlassian.net/wiki/rest/api/content
```

### OAuth 2.0
For applications requiring user consent and delegated access.

## Available Endpoints

### 1. Create Page
**Method:** POST  
**Path:** `/rest/api/content`

Creates a new page in a specified space.

#### Request Example
```json
{
  "type": "page",
  "title": "New API Documentation",
  "space": {
    "key": "DEV"
  },
  "body": {
    "storage": {
      "value": "<p>This is the page content</p>",
      "representation": "storage"
    }
  },
  "ancestors": [
    {
      "id": "123456"
    }
  ]
}
```

#### Python Example
```python
import requests
import json

def create_page(base_url, auth, space_key, title, content, parent_id=None):
    url = f"{base_url}/rest/api/content"
    
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }
    
    if parent_id:
        payload["ancestors"] = [{"id": parent_id}]
    
    response = requests.post(
        url,
        auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    return response.json()

# Usage
auth = ("user@example.com", "api_token")
page = create_page(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "DEV",
    "API Documentation",
    "<h1>Overview</h1><p>API documentation content</p>"
)
```

### 2. Get Page
**Method:** GET  
**Path:** `/rest/api/content/{id}`

Retrieves a page by its ID with optional expansions.

#### Common Parameters
- `expand`: Comma-separated list of properties to expand
  - `body.storage`: Raw storage format
  - `body.view`: HTML view format
  - `version`: Version information
  - `ancestors`: Parent pages
  - `descendants`: Child pages
  - `space`: Space information
  - `history`: Page history
  - `metadata`: Page metadata

#### cURL Example
```bash
curl -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789?expand=body.storage,version,ancestors"
```

#### Response Example
```json
{
  "id": "123456789",
  "type": "page",
  "status": "current",
  "title": "API Documentation",
  "space": {
    "id": 98765,
    "key": "DEV",
    "name": "Development"
  },
  "body": {
    "storage": {
      "value": "<p>Page content here</p>",
      "representation": "storage"
    }
  },
  "version": {
    "by": {
      "type": "known",
      "username": "john.doe",
      "displayName": "John Doe"
    },
    "when": "2024-01-15T10:30:00.000Z",
    "number": 3
  },
  "ancestors": [
    {
      "id": "123456",
      "type": "page",
      "title": "Parent Page"
    }
  ]
}
```

### 3. Update Page
**Method:** PUT  
**Path:** `/rest/api/content/{id}`

Updates an existing page. Requires the current version number.

#### Request Example
```json
{
  "id": "123456789",
  "type": "page",
  "title": "Updated API Documentation",
  "space": {
    "key": "DEV"
  },
  "body": {
    "storage": {
      "value": "<p>Updated content</p>",
      "representation": "storage"
    }
  },
  "version": {
    "number": 4,
    "minorEdit": false
  }
}
```

#### Python Example
```python
def update_page(base_url, auth, page_id, title, content, version_number):
    url = f"{base_url}/rest/api/content/{page_id}"
    
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        },
        "version": {
            "number": version_number + 1,
            "minorEdit": False
        }
    }
    
    response = requests.put(
        url,
        auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    return response.json()
```

### 4. Delete Page
**Method:** DELETE  
**Path:** `/rest/api/content/{id}`

Deletes a page or moves it to trash.

#### Parameters
- `status`: Set to "trashed" to move to trash (can be restored)
- Permanent deletion requires admin permissions

#### cURL Example
```bash
# Move to trash
curl -X DELETE -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789?status=trashed"

# Permanent delete (admin only)
curl -X DELETE -u admin@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789"
```

### 5. Search Pages
**Method:** GET  
**Path:** `/rest/api/content/search`

Search for pages using CQL (Confluence Query Language).

#### Parameters
- `cql`: Confluence Query Language string
- `limit`: Maximum results (default: 25, max: 100)
- `start`: Starting index for pagination
- `expand`: Properties to expand

#### CQL Examples
```bash
# Find pages in space
cql=space=DEV and type=page

# Find pages by title
cql=title~"API Documentation" and space=DEV

# Find recently updated pages
cql=lastmodified>now("-7d") and type=page

# Find pages by label
cql=label="api-docs" and space=DEV

# Find pages by creator
cql=creator=john.doe and space=DEV
```

#### Python Search Example
```python
def search_pages(base_url, auth, cql_query, limit=25):
    url = f"{base_url}/rest/api/content/search"
    
    params = {
        "cql": cql_query,
        "limit": limit,
        "expand": "body.storage,version"
    }
    
    response = requests.get(url, auth=auth, params=params)
    return response.json()

# Search for API documentation pages
results = search_pages(
    "https://your-domain.atlassian.net/wiki",
    auth,
    'title~"API" and space=DEV and type=page'
)
```

### 6. Get Page Children
**Method:** GET  
**Path:** `/rest/api/content/{id}/child/page`

Retrieves child pages of a specific page.

#### cURL Example
```bash
curl -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789/child/page?expand=body.storage"
```

### 7. Get Page History
**Method:** GET  
**Path:** `/rest/api/content/{id}/history`

Retrieves the version history of a page.

## Common Parameters

### Expansion Parameters
Most GET endpoints support the `expand` parameter for including additional data:
- `body.storage`: Raw storage format content
- `body.view`: Rendered HTML content
- `body.export_view`: Export-friendly HTML
- `version`: Version information
- `ancestors`: Parent page hierarchy
- `descendants`: Child pages
- `space`: Space details
- `history`: Change history
- `metadata`: Custom metadata
- `restrictions`: View/edit restrictions
- `operations`: Available operations

### Pagination Parameters
- `start`: Starting index (0-based)
- `limit`: Number of results (max: 100)

### Format Parameters
- `representation`: Content format (storage, view, export_view)
- `status`: Content status (current, trashed, draft)

## Error Handling

### Common HTTP Status Codes
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `204 No Content`: Successful deletion
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Version conflict or duplicate content

### Error Response Format
```json
{
  "statusCode": 400,
  "data": {
    "authorized": true,
    "valid": false,
    "errors": [
      {
        "message": "Version number must be incremented for updates"
      }
    ]
  },
  "message": "com.atlassian.confluence.api.service.exceptions.BadRequestException"
}
```

### Python Error Handling Example
```python
def safe_create_page(base_url, auth, space_key, title, content):
    try:
        response = requests.post(
            f"{base_url}/rest/api/content",
            auth=auth,
            headers={"Content-Type": "application/json"},
            json={
                "type": "page",
                "title": title,
                "space": {"key": space_key},
                "body": {"storage": {"value": content, "representation": "storage"}}
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print(f"Bad request: {e.response.json()}")
        elif e.response.status_code == 401:
            print("Authentication failed")
        elif e.response.status_code == 403:
            print("Insufficient permissions")
        else:
            print(f"HTTP error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
```

## Best Practices

### 1. Version Management
- Always fetch the current version before updating
- Increment version number correctly
- Use minor edits for small changes
- Handle version conflicts gracefully

### 2. Content Formatting
- Use storage format for API operations
- Validate HTML/XML before sending
- Escape special characters properly
- Use Confluence macros appropriately

### 3. Performance Optimization
- Use specific field expansions instead of expanding all
- Implement pagination for large result sets
- Cache frequently accessed content
- Batch operations when possible

### 4. Security Considerations
- Store credentials securely
- Use API tokens instead of passwords
- Implement proper access controls
- Validate and sanitize user input
- Use HTTPS for all requests

### 5. Rate Limiting
- Implement exponential backoff
- Respect rate limit headers
- Cache responses when appropriate
- Use bulk operations to reduce API calls

### 6. Error Recovery
```python
import time

def retry_with_backoff(func, max_retries=3, backoff_factor=2):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [429, 503]:  # Rate limit or service unavailable
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise
```

### 7. Bulk Operations Example
```python
def bulk_create_pages(base_url, auth, pages_data):
    """Create multiple pages efficiently"""
    created_pages = []
    
    for page_data in pages_data:
        try:
            page = create_page(
                base_url,
                auth,
                page_data['space_key'],
                page_data['title'],
                page_data['content'],
                page_data.get('parent_id')
            )
            created_pages.append(page)
            print(f"Created page: {page['title']}")
        except Exception as e:
            print(f"Failed to create page {page_data['title']}: {e}")
            
    return created_pages
```

## Advanced Examples

### Page Template Usage
```python
def create_page_from_template(base_url, auth, space_key, title, template_id, replacements):
    """Create a page using a template with variable substitution"""
    
    # Get template content
    template = requests.get(
        f"{base_url}/rest/api/content/{template_id}?expand=body.storage",
        auth=auth
    ).json()
    
    # Replace variables in template
    content = template['body']['storage']['value']
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    
    # Create new page
    return create_page(base_url, auth, space_key, title, content)
```

### Hierarchical Page Structure
```python
def create_page_hierarchy(base_url, auth, space_key, hierarchy):
    """Create a nested page structure"""
    
    def create_recursive(items, parent_id=None):
        for item in items:
            page = create_page(
                base_url,
                auth,
                space_key,
                item['title'],
                item['content'],
                parent_id
            )
            
            if 'children' in item:
                create_recursive(item['children'], page['id'])
    
    create_recursive(hierarchy)
```

### Content Migration
```python
def migrate_pages(source_url, source_auth, target_url, target_auth, space_key, cql_filter):
    """Migrate pages between Confluence instances"""
    
    # Search source pages
    search_results = search_pages(source_url, source_auth, cql_filter)
    
    for page in search_results['results']:
        # Get full page content
        full_page = requests.get(
            f"{source_url}/rest/api/content/{page['id']}?expand=body.storage,attachments",
            auth=source_auth
        ).json()
        
        # Create in target
        create_page(
            target_url,
            target_auth,
            space_key,
            full_page['title'],
            full_page['body']['storage']['value']
        )
```