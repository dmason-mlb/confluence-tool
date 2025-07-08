# Database Operations

## Overview
Confluence databases (formerly known as tables) provide structured data storage with custom fields, filters, and views. They support various field types and can be embedded in pages.

## Endpoints

### Get Database
```
GET /wiki/api/v2/databases/{id}
```

### Create Database
```
POST /wiki/api/v2/databases
```

### Update Database
```
PUT /wiki/api/v2/databases/{id}
```

### Delete Database
```
DELETE /wiki/api/v2/databases/{id}
```

### Database Entries
```
GET /wiki/api/v2/databases/{id}/entries
POST /wiki/api/v2/databases/{id}/entries
PUT /wiki/api/v2/databases/{id}/entries/{entryId}
DELETE /wiki/api/v2/databases/{id}/entries/{entryId}
```

## Field Types

- `text` - Single line text
- `paragraph` - Multi-line text
- `number` - Numeric values
- `date` - Date picker
- `checkbox` - Boolean values
- `select` - Single selection
- `multiselect` - Multiple selections
- `person` - User selector
- `status` - Status labels
- `label` - Tags
- `url` - Links

## Request/Response Examples

### Create Database Request
```json
{
  "spaceId": "786433",
  "parentId": "123456",
  "title": "Project Tasks",
  "schema": {
    "fields": [
      {
        "id": "title",
        "name": "Task Name",
        "type": "text",
        "required": true
      },
      {
        "id": "status",
        "name": "Status",
        "type": "select",
        "options": [
          {"value": "todo", "label": "To Do"},
          {"value": "progress", "label": "In Progress"},
          {"value": "done", "label": "Done"}
        ]
      },
      {
        "id": "assignee",
        "name": "Assignee",
        "type": "person"
      },
      {
        "id": "dueDate",
        "name": "Due Date",
        "type": "date"
      }
    ]
  }
}
```

### Database Entry Response
```json
{
  "id": "entry-123",
  "databaseId": "db-456",
  "values": {
    "title": "Implement login feature",
    "status": "progress",
    "assignee": {
      "accountId": "557058:c4f2c3b5",
      "displayName": "John Doe"
    },
    "dueDate": "2025-01-15"
  },
  "createdAt": "2025-01-08T10:00:00Z",
  "updatedAt": "2025-01-08T14:30:00Z"
}
```

## Code Examples

### Python - Create Database with Entries
```python
import requests

# Create database
db_url = "https://instance.atlassian.net/wiki/api/v2/databases"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}

database = {
    "spaceId": "786433",
    "title": "Bug Tracker",
    "schema": {
        "fields": [
            {"id": "title", "name": "Bug Title", "type": "text"},
            {"id": "severity", "name": "Severity", "type": "select",
             "options": [
                 {"value": "low", "label": "Low"},
                 {"value": "medium", "label": "Medium"},
                 {"value": "high", "label": "High"}
             ]},
            {"id": "reporter", "name": "Reporter", "type": "person"}
        ]
    }
}

db_response = requests.post(db_url, json=database, headers=headers)
db_id = db_response.json()["id"]

# Add entry
entry_url = f"{db_url}/{db_id}/entries"
entry = {
    "values": {
        "title": "Login button not working",
        "severity": "high",
        "reporter": {"accountId": "current"}
    }
}

entry_response = requests.post(entry_url, json=entry, headers=headers)
```

### JavaScript - Query Database Entries
```javascript
async function queryDatabase(databaseId, filters) {
  const params = new URLSearchParams({
    filter: JSON.stringify(filters),
    limit: 50
  });
  
  const response = await fetch(
    `https://instance.atlassian.net/wiki/api/v2/databases/${databaseId}/entries?${params}`,
    {
      headers: {
        'Authorization': 'Bearer YOUR_TOKEN'
      }
    }
  );
  
  return response.json();
}

// Example: Get high severity bugs
const highSeverityBugs = await queryDatabase('db-456', {
  severity: { $eq: 'high' },
  status: { $ne: 'resolved' }
});
```

## Common Use Cases

1. **Task Management**: Track project tasks and assignments
2. **Bug Tracking**: Log and monitor issues
3. **Asset Inventory**: Manage resources and equipment
4. **Contact Lists**: Store team or customer information
5. **Meeting Notes**: Structured meeting records
6. **Risk Register**: Track project risks

## Best Practices

- Define clear field naming conventions
- Use appropriate field types for data
- Set required fields for data integrity
- Create views for common queries
- Regular data validation
- Export backups periodically
- Limit database size for performance
- Use filters instead of manual sorting
- Implement access controls
- Document field meanings and usage