# Space Operations

## Overview
Confluence spaces are containers for pages and content. Each space has a unique key and can be configured with permissions, themes, and settings.

## Endpoints

### Get All Spaces
```
GET /wiki/rest/api/space
```

**Query Parameters:**
- `spaceKey` - Filter by space keys (comma-separated)
- `type` - Filter by type: `global` or `personal`
- `status` - Filter by status: `current` or `archived`
- `limit` - Max results per page (default: 25)
- `start` - Starting index for pagination

### Get Space by Key
```
GET /wiki/rest/api/space/{spaceKey}
```

**Expand Options:**
- `settings` - Space settings
- `metadata.labels` - Space labels
- `operations` - Available operations
- `permissions` - Space permissions summary

### Create Space
```
POST /wiki/rest/api/space
```

### Update Space
```
PUT /wiki/rest/api/space/{spaceKey}
```

### Delete Space
```
DELETE /wiki/rest/api/space/{spaceKey}
```

## Request/Response Examples

### Create Space Request
```json
{
  "key": "PROJ",
  "name": "Project Space",
  "description": {
    "plain": {
      "value": "Space for project documentation",
      "representation": "plain"
    }
  },
  "metadata": {}
}
```

### Space Response
```json
{
  "id": 786433,
  "key": "PROJ",
  "name": "Project Space",
  "type": "global",
  "status": "current",
  "_links": {
    "webui": "/spaces/PROJ",
    "self": "https://instance.atlassian.net/wiki/rest/api/space/PROJ"
  }
}
```

## Code Examples

### Python - Create Space
```python
import requests

url = "https://instance.atlassian.net/wiki/rest/api/space"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "key": "NEWSPACE",
    "name": "New Space"
}

response = requests.post(url, json=data, headers=headers)
```

### JavaScript - Get Space with Expansion
```javascript
const response = await fetch(
  'https://instance.atlassian.net/wiki/rest/api/space/PROJ?expand=settings,permissions',
  {
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN'
    }
  }
);
const space = await response.json();
```

## Common Use Cases

1. **Space Templates**: Create spaces with predefined structure
2. **Archive Management**: Archive old project spaces
3. **Personal Spaces**: Create user-specific workspaces
4. **Space Migration**: Copy space structure and settings

## Best Practices

- Use meaningful space keys (3-10 uppercase letters)
- Set appropriate default permissions
- Archive rather than delete spaces when possible
- Implement space naming conventions
- Regular permission audits
- Use space categories for organization