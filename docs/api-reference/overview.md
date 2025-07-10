# Confluence Cloud REST API v2 Overview

## Introduction

The Confluence Cloud REST API v2 provides programmatic access to Confluence Cloud instances. This API enables you to create, read, update, and delete content, manage spaces and permissions, work with attachments, and perform administrative tasks.

## Base URL

```
https://{your-domain}.atlassian.net/wiki/api/v2/
```

## Authentication

All API requests require authentication using Basic Authentication with:
- **Username**: Your email address
- **Password**: API token (not your Confluence password)

### Creating an API Token
1. Visit https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give your token a descriptive name
4. Copy the token immediately (it won't be shown again)

### Authentication Header
```
Authorization: Basic {base64_encoded_email:api_token}
```

## API Categories

### Core Content Management
- **[Pages](core/pages.md)** - Create and manage wiki pages
- **[Blog Posts](core/blog-posts.md)** - Work with blog content
- **[Attachments](core/attachments.md)** - Upload and manage file attachments
- **[Comments](core/comments.md)** - Footer and inline comments

### Advanced Content
- **[Whiteboards](content/whiteboards.md)** - Visual collaboration boards
- **[Databases](content/databases.md)** - Structured data management

### Space Management
- **[Spaces](space/spaces.md)** - Create and manage spaces
- **[Space Permissions](space/permissions.md)** - Control access

## Common Patterns

### Pagination
Most list endpoints support pagination:
```
?limit=25&start=0
```

### Sorting
Sort results using the `sort` parameter:
```
?sort=created-date
?sort=-modified-date  # Descending order
```

### Content Formats
Specify content format using `body-format`:
- `storage` - Confluence storage format (default)
- `atlas_doc_format` - Atlassian Document Format
- `view` - HTML view format

### Response Formats
Include additional data using `include-*` parameters:
- `include-labels=true`
- `include-properties=true`
- `include-operations=true`
- `include-versions=true`
- `include-version=true`
- `include-favorited-by-current-user-status=true`

## Error Handling

### HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful request with no response body
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "errors": [
    {
      "status": 400,
      "code": "INVALID_PARAMETER",
      "title": "Invalid Parameter",
      "detail": "The 'limit' parameter must be between 1 and 250"
    }
  ]
}
```

## Rate Limiting

Confluence Cloud enforces rate limits:
- **Default**: 10 requests per second per user
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **429 Response**: Includes `Retry-After` header

## Best Practices

1. **Use Pagination**: Always paginate when fetching lists
2. **Cache Responses**: Reduce API calls by caching unchanged data
3. **Batch Operations**: Use bulk endpoints when available
4. **Handle Errors**: Implement proper error handling and retries
5. **Respect Rate Limits**: Implement exponential backoff
6. **Use Webhooks**: For real-time updates instead of polling

## Quick Start

For practical examples and code samples, see:
- **[Example Scripts](../../scripts/examples/)** - Complete working examples
- **[Generic Scripts](../../generic-scripts/)** - Standalone scripts for external use
- **[Python Client](../../scripts/confluence_client.py)** - Full-featured client library