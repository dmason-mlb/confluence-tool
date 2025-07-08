# Confluence Cloud REST API v2 - Quick Reference

## Setup
```bash
BASE_URL="https://your-domain.atlassian.net/wiki/api/v2"
AUTH="your-email@example.com:your-api-token"
```

## Common cURL Examples

### Authentication Test
```bash
curl -u $AUTH "$BASE_URL/user/current" | jq .
```

### Spaces
```bash
# List all spaces
curl -u $AUTH "$BASE_URL/spaces" | jq .

# Get specific space
curl -u $AUTH "$BASE_URL/spaces/{space-id}" | jq .
```

### Pages
```bash
# Get all pages
curl -u $AUTH "$BASE_URL/pages?limit=10" | jq .

# Get pages in a space
curl -u $AUTH "$BASE_URL/pages?space-id={space-id}" | jq .

# Get specific page with content
curl -u $AUTH "$BASE_URL/pages/{page-id}?body-format=storage" | jq .

# Create a page
curl -u $AUTH -X POST "$BASE_URL/pages" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "12345",
    "status": "current",
    "title": "My New Page",
    "body": {
      "representation": "storage",
      "value": "<p>Page content</p>"
    }
  }' | jq .

# Update a page
curl -u $AUTH -X PUT "$BASE_URL/pages/{page-id}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "{page-id}",
    "status": "current",
    "title": "Updated Title",
    "body": {
      "representation": "storage",
      "value": "<p>Updated content</p>"
    },
    "version": {
      "number": 2
    }
  }' | jq .

# Delete a page (move to trash)
curl -u $AUTH -X DELETE "$BASE_URL/pages/{page-id}"

# Purge a page (permanent delete)
curl -u $AUTH -X DELETE "$BASE_URL/pages/{page-id}?purge=true"
```

### Blog Posts
```bash
# Get blog posts in a space
curl -u $AUTH "$BASE_URL/spaces/{space-id}/blogposts" | jq .

# Create a blog post
curl -u $AUTH -X POST "$BASE_URL/blogposts" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "12345",
    "status": "current",
    "title": "My Blog Post",
    "body": {
      "representation": "storage",
      "value": "<p>Blog content</p>"
    }
  }' | jq .
```

### Comments
```bash
# Get page comments
curl -u $AUTH "$BASE_URL/pages/{page-id}/footer-comments" | jq .

# Create a footer comment
curl -u $AUTH -X POST "$BASE_URL/footer-comments" \
  -H "Content-Type: application/json" \
  -d '{
    "pageId": "12345",
    "body": {
      "representation": "storage",
      "value": "<p>My comment</p>"
    }
  }' | jq .

# Create an inline comment
curl -u $AUTH -X POST "$BASE_URL/inline-comments" \
  -H "Content-Type: application/json" \
  -d '{
    "pageId": "12345",
    "body": {
      "representation": "storage",
      "value": "<p>Inline comment</p>"
    },
    "inlineCommentProperties": {
      "textSelection": "selected text",
      "textSelectionMatchIndex": 0
    }
  }' | jq .
```

### Attachments
```bash
# Get page attachments
curl -u $AUTH "$BASE_URL/pages/{page-id}/attachments" | jq .

# Upload an attachment (multipart/form-data)
curl -u $AUTH -X POST "$BASE_URL/pages/{page-id}/attachments" \
  -F "file=@/path/to/file.pdf" \
  -F "comment=File description" | jq .
```

### Labels
```bash
# Get page labels
curl -u $AUTH "$BASE_URL/pages/{page-id}/labels" | jq .

# Add a label to a page
curl -u $AUTH -X POST "$BASE_URL/pages/{page-id}/labels" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-label"}' | jq .
```

### Children and Ancestors
```bash
# Get page children
curl -u $AUTH "$BASE_URL/pages/{page-id}/children" | jq .

# Get page ancestors
curl -u $AUTH "$BASE_URL/pages/{page-id}/ancestors" | jq .
```

### Classification Levels
```bash
# Get available classification levels
curl -u $AUTH "$BASE_URL/classification-levels" | jq .

# Set page classification
curl -u $AUTH -X PUT "$BASE_URL/pages/{page-id}/classification-level" \
  -H "Content-Type: application/json" \
  -d '{"classificationLevelId": "confidential"}' | jq .
```

## Query Parameters Cheat Sheet

### Pagination
- `limit`: Max results per page (usually 1-100)
- `cursor`: Opaque cursor for next page

### Filtering
- `status`: current, draft, archived, trashed
- `space-id`: Filter by space ID(s)
- `title`: Filter by title
- `sort`: Sort by field (prefix with - for descending)

### Content Format
- `body-format`: storage, atlas_doc_format, view

### Include Parameters
- `include-labels`: true/false
- `include-properties`: true/false
- `include-operations`: true/false
- `include-likes`: true/false
- `include-versions`: true/false
- `include-version`: true/false
- `include-collaborators`: true/false

## Response Headers to Watch
- `Link`: Contains pagination links
- `X-RateLimit-Limit`: Rate limit maximum
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Reset timestamp

## Common Status Codes
- `200`: Success (GET/PUT)
- `201`: Created (POST)
- `204`: No Content (DELETE)
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests

## Python Quick Start
```python
import requests
import base64

# Setup
base_url = "https://your-domain.atlassian.net/wiki/api/v2"
auth = base64.b64encode(b"email:token").decode("ascii")
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# Get pages
response = requests.get(f"{base_url}/pages", headers=headers)
pages = response.json()

# Create page
data = {
    "spaceId": "12345",
    "title": "New Page",
    "body": {
        "representation": "storage",
        "value": "<p>Content</p>"
    }
}
response = requests.post(f"{base_url}/pages", headers=headers, json=data)
```

## JavaScript/Node.js Quick Start
```javascript
const axios = require('axios');

// Setup
const baseURL = 'https://your-domain.atlassian.net/wiki/api/v2';
const auth = Buffer.from('email:token').toString('base64');

const client = axios.create({
  baseURL,
  headers: {
    'Authorization': `Basic ${auth}`,
    'Content-Type': 'application/json'
  }
});

// Get pages
const pages = await client.get('/pages');

// Create page
const newPage = await client.post('/pages', {
  spaceId: '12345',
  title: 'New Page',
  body: {
    representation: 'storage',
    value: '<p>Content</p>'
  }
});
```

## Tips
1. Always handle pagination for list endpoints
2. Use appropriate body-format for your needs
3. Include version number when updating content
4. Check permissions before operations
5. Implement exponential backoff for rate limits
6. Cache responses when appropriate
7. Use batch operations to minimize API calls