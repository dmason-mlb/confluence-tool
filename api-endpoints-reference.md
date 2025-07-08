# Confluence Cloud REST API v2 - Complete Endpoint Reference

This document provides a complete reference of all API endpoints with HTTP methods, paths, and key parameters.

## Authentication Setup
```
Authorization: Basic {base64(username:apiToken)}
Content-Type: application/json
Accept: application/json
```

## Endpoint Reference by Category

### Admin Key Management

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/admin-key` | Get Admin Key information | - |
| POST | `/admin-key` | Enable Admin Key | `durationInMinutes` (optional, default: 10) |
| DELETE | `/admin-key` | Disable Admin Key | - |

**Required Permissions:** Organization or site admin

### Attachment Operations

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/attachments` | Get all attachments | `sort`, `cursor`, `status`, `mediaType`, `filename`, `limit` |
| GET | `/attachments/:id` | Get attachment by ID | `version`, `include-*` params |
| DELETE | `/attachments/:id` | Delete attachment | `purge` (boolean) |
| GET | `/pages/:id/attachments` | Get page attachments | Same as `/attachments` |
| GET | `/blogposts/:id/attachments` | Get blog post attachments | Same as `/attachments` |
| GET | `/custom-content/:id/attachments` | Get custom content attachments | Same as `/attachments` |
| GET | `/labels/:id/attachments` | Get attachments by label | `sort`, `cursor`, `limit` |

### Content Ancestors

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/pages/:id/ancestors` | Get page ancestors | `limit` |
| GET | `/whiteboards/:id/ancestors` | Get whiteboard ancestors | `limit` |
| GET | `/databases/:id/ancestors` | Get database ancestors | `limit` |
| GET | `/embeds/:id/ancestors` | Get Smart Link ancestors | `limit` |
| GET | `/folders/:id/ancestors` | Get folder ancestors | `limit` |

### Blog Post Management

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/blogposts` | Get all blog posts | `id`, `space-id`, `sort`, `status`, `title`, `body-format`, `cursor`, `limit` |
| POST | `/blogposts` | Create blog post | `private` (boolean) |
| GET | `/blogposts/:id` | Get blog post by ID | `body-format`, `get-draft`, `status`, `version`, `include-*` params |
| PUT | `/blogposts/:id` | Update blog post | - |
| DELETE | `/blogposts/:id` | Delete blog post | `purge`, `draft` |
| GET | `/labels/:id/blogposts` | Get blog posts by label | `space-id`, `body-format`, `sort`, `cursor`, `limit` |
| GET | `/spaces/:id/blogposts` | Get blog posts in space | `sort`, `status`, `title`, `body-format`, `cursor`, `limit` |

### Content Children

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/pages/:id/children` | Get child pages | `cursor`, `limit`, `sort` |
| GET | `/pages/:id/direct-children` | Get direct children | `cursor`, `limit`, `sort` |
| GET | `/custom-content/:id/children` | Get child custom content | `cursor`, `limit`, `sort` |
| GET | `/whiteboards/:id/direct-children` | Get whiteboard children | `cursor`, `limit`, `sort` |
| GET | `/databases/:id/direct-children` | Get database children | `cursor`, `limit`, `sort` |
| GET | `/embeds/:id/direct-children` | Get Smart Link children | `cursor`, `limit`, `sort` |
| GET | `/folders/:id/direct-children` | Get folder children | `cursor`, `limit`, `sort` |

### Classification Level Management

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/classification-levels` | Get available classification levels | - |
| GET | `/spaces/:id/classification-level/default` | Get space default classification | - |
| PUT | `/spaces/:id/classification-level/default` | Update space default classification | Request body with level |
| DELETE | `/spaces/:id/classification-level/default` | Delete space default classification | - |
| GET | `/pages/:id/classification-level` | Get page classification | `status` |
| PUT | `/pages/:id/classification-level` | Update page classification | Request body with level |
| POST | `/pages/:id/classification-level/reset` | Reset page classification | - |
| GET | `/blogposts/:id/classification-level` | Get blog post classification | `status` |
| PUT | `/blogposts/:id/classification-level` | Update blog post classification | Request body with level |
| POST | `/blogposts/:id/classification-level/reset` | Reset blog post classification | - |
| GET | `/whiteboards/:id/classification-level` | Get whiteboard classification | - |
| PUT | `/whiteboards/:id/classification-level` | Update whiteboard classification | Request body with level |
| POST | `/whiteboards/:id/classification-level/reset` | Reset whiteboard classification | - |
| GET | `/databases/:id/classification-level` | Get database classification | - |
| PUT | `/databases/:id/classification-level` | Update database classification | Request body with level |
| POST | `/databases/:id/classification-level/reset` | Reset database classification | - |

### Comment Management

#### Footer Comments

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/footer-comments` | Get all footer comments | `body-format`, `sort`, `cursor`, `limit` |
| POST | `/footer-comments` | Create footer comment | Request body with content |
| GET | `/footer-comments/:comment-id` | Get footer comment by ID | `body-format`, `version`, `include-*` params |
| PUT | `/footer-comments/:comment-id` | Update footer comment | Request body with updates |
| DELETE | `/footer-comments/:comment-id` | Delete footer comment | - |
| GET | `/footer-comments/:id/children` | Get child comments | `body-format`, `sort`, `cursor`, `limit` |
| GET | `/pages/:id/footer-comments` | Get page footer comments | `body-format`, `status`, `sort`, `cursor`, `limit` |
| GET | `/blogposts/:id/footer-comments` | Get blog post footer comments | `body-format`, `status`, `sort`, `cursor`, `limit` |
| GET | `/attachments/:id/footer-comments` | Get attachment comments | `body-format`, `cursor`, `limit`, `sort`, `version` |
| GET | `/custom-content/:id/footer-comments` | Get custom content comments | `body-format`, `cursor`, `limit`, `sort` |

#### Inline Comments

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/inline-comments` | Get all inline comments | `body-format`, `sort`, `cursor`, `limit` |
| POST | `/inline-comments` | Create inline comment | Request body with content and properties |
| GET | `/inline-comments/:comment-id` | Get inline comment by ID | `body-format`, `version`, `include-*` params |
| PUT | `/inline-comments/:comment-id` | Update inline comment | Request body with updates |
| DELETE | `/inline-comments/:comment-id` | Delete inline comment | - |
| GET | `/inline-comments/:id/children` | Get child inline comments | `body-format`, `sort`, `cursor`, `limit` |
| GET | `/pages/:id/inline-comments` | Get page inline comments | `body-format`, `status`, `resolution-status`, `sort`, `cursor`, `limit` |
| GET | `/blogposts/:id/inline-comments` | Get blog post inline comments | `body-format`, `status`, `resolution-status`, `sort`, `cursor`, `limit` |

### Content Utilities

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| POST | `/content/convert-ids-to-types` | Convert content IDs to types | Request body with ID array |

### Content Properties

| Method | Path | Description | Key Parameters |
|--------|------|-------------|----------------|
| GET | `/attachments/:attachment-id/properties` | Get attachment properties | `key`, `sort`, `cursor`, `limit` |
| POST | `/attachments/:attachment-id/properties` | Create attachment property | Request body with property |
| GET | `/attachments/:attachment-id/properties/:property-id` | Get specific property | - |

## Request Body Examples

### Create Blog Post
```json
{
  "spaceId": "12345",
  "status": "current",
  "title": "My Blog Post",
  "body": {
    "representation": "storage",
    "value": "<p>Blog post content</p>"
  }
}
```

### Create Footer Comment
```json
{
  "pageId": "12345",
  "body": {
    "representation": "storage",
    "value": "<p>Comment text</p>"
  }
}
```

### Create Inline Comment
```json
{
  "pageId": "12345",
  "body": {
    "representation": "storage",
    "value": "<p>Inline comment text</p>"
  },
  "inlineCommentProperties": {
    "textSelection": "selected text",
    "textSelectionMatchIndex": 0
  }
}
```

### Update Classification Level
```json
{
  "classificationLevelId": "confidential"
}
```

## Common Query Parameters

### Pagination
- `cursor`: Opaque cursor for next page
- `limit`: Number of results (usually max 100)

### Filtering
- `status`: current, draft, archived, trashed
- `sort`: Field to sort by (e.g., "created", "-modified")
- `body-format`: storage, atlas_doc_format, view

### Including Related Data
- `include-labels`: Include associated labels
- `include-properties`: Include content properties
- `include-operations`: Include available operations
- `include-likes`: Include like information
- `include-versions`: Include version history
- `include-version`: Include current version info
- `include-collaborators`: Include collaborator list
- `include-favorited-by-current-user-status`: Include favorite status
- `include-webresources`: Include web resources for rendering

## Error Responses

Common HTTP status codes:
- `200 OK`: Successful GET/PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Authentication failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate)
- `429 Too Many Requests`: Rate limit exceeded

## Rate Limiting

The API implements rate limiting. Check response headers:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets

## Best Practices

1. **Use Pagination**: Always implement pagination for list endpoints
2. **Cache Results**: Use ETags and If-None-Match headers
3. **Batch Operations**: Minimize API calls by using include parameters
4. **Error Handling**: Implement exponential backoff for rate limits
5. **Content Format**: Use appropriate body-format for your use case
6. **Permissions**: Check permissions before attempting operations