# Whiteboard Operations

## Overview
Confluence whiteboards provide visual collaboration spaces for teams. They support shapes, connectors, sticky notes, and embedded content.

## Endpoints

### Get Whiteboard
```
GET /wiki/api/v2/whiteboards/{id}
```

### Create Whiteboard
```
POST /wiki/api/v2/whiteboards
```

### Update Whiteboard
```
PUT /wiki/api/v2/whiteboards/{id}
```

### Delete Whiteboard
```
DELETE /wiki/api/v2/whiteboards/{id}
```

### Get Whiteboard Content
```
GET /wiki/api/v2/whiteboards/{id}/content
```

## Request/Response Examples

### Create Whiteboard Request
```json
{
  "spaceId": "786433",
  "title": "Project Planning Board",
  "parentId": "123456",
  "body": {
    "representation": "whiteboard",
    "value": {
      "version": 1,
      "type": "whiteboard",
      "content": []
    }
  }
}
```

### Whiteboard Response
```json
{
  "id": "987654",
  "type": "whiteboard",
  "status": "current",
  "title": "Project Planning Board",
  "spaceId": "786433",
  "version": {
    "number": 1,
    "createdAt": "2025-01-08T10:00:00Z"
  },
  "_links": {
    "webui": "/spaces/PROJ/whiteboard/987654",
    "self": "https://instance.atlassian.net/wiki/api/v2/whiteboards/987654"
  }
}
```

### Whiteboard Content Structure
```json
{
  "version": 1,
  "type": "whiteboard",
  "content": [
    {
      "id": "sticky-1",
      "type": "sticky",
      "position": { "x": 100, "y": 100 },
      "size": { "width": 200, "height": 150 },
      "content": {
        "text": "Task 1",
        "color": "yellow"
      }
    },
    {
      "id": "shape-1",
      "type": "rectangle",
      "position": { "x": 400, "y": 100 },
      "size": { "width": 300, "height": 200 },
      "style": {
        "fill": "#e3f2fd",
        "stroke": "#1976d2"
      }
    }
  ]
}
```

## Code Examples

### Python - Create Whiteboard with Content
```python
import requests
import json

url = "https://instance.atlassian.net/wiki/api/v2/whiteboards"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}

whiteboard_data = {
    "spaceId": "786433",
    "title": "Sprint Planning",
    "body": {
        "representation": "whiteboard",
        "value": {
            "version": 1,
            "type": "whiteboard",
            "content": [
                {
                    "id": "sticky-1",
                    "type": "sticky",
                    "position": {"x": 50, "y": 50},
                    "content": {"text": "Sprint Goal"}
                }
            ]
        }
    }
}

response = requests.post(url, json=whiteboard_data, headers=headers)
```

### JavaScript - Update Whiteboard Elements
```javascript
async function addStickyNote(whiteboardId, text, position) {
  const response = await fetch(
    `https://instance.atlassian.net/wiki/api/v2/whiteboards/${whiteboardId}/content`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        operations: [
          {
            op: 'add',
            path: '/content/-',
            value: {
              id: `sticky-${Date.now()}`,
              type: 'sticky',
              position: position,
              content: { text: text }
            }
          }
        ]
      })
    }
  );
  return response.json();
}
```

## Common Use Cases

1. **Sprint Planning**: Visual task organization
2. **Mind Mapping**: Brainstorming sessions
3. **Process Flows**: Diagram workflows
4. **Retrospectives**: Team feedback boards
5. **Architecture Diagrams**: System design

## Best Practices

- Keep whiteboards focused on single topics
- Use consistent color coding
- Regular cleanup of old content
- Export important diagrams as images
- Set appropriate permissions
- Use templates for common patterns
- Limit number of elements for performance
- Include legends for complex diagrams