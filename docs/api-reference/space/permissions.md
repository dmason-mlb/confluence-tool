# Space Permissions

## Overview
Space permissions control access to content within a Confluence space. Permissions can be granted to users, groups, or anonymous access.

## Permission Types

### Space Permissions
- `VIEWSPACE` - View pages and blog posts
- `REMOVEOWNCONTENT` - Delete own content
- `EDITSPACE` - Administer the space
- `REMOVEPAGE` - Delete any page
- `EDITBLOG` - Create and edit blog posts
- `REMOVEBLOG` - Delete any blog post
- `CREATEATTACHMENT` - Upload attachments
- `REMOVEATTACHMENT` - Delete attachments
- `COMMENT` - Add comments
- `REMOVECOMMENT` - Delete any comment
- `SETPAGEPERMISSIONS` - Restrict page access
- `EXPORTSPACE` - Export space content
- `SETSPACEPERMISSIONS` - Manage space permissions

## Endpoints

### Get Space Permissions
```
GET /wiki/rest/api/space/{spaceKey}/permission
```

### Add Permission
```
POST /wiki/rest/api/space/{spaceKey}/permission
```

### Remove Permission
```
DELETE /wiki/rest/api/space/{spaceKey}/permission/{id}
```

## Request/Response Examples

### Add Permission Request
```json
{
  "subject": {
    "type": "group",
    "identifier": "developers"
  },
  "operation": {
    "operation": "create",
    "targetType": "page"
  }
}
```

### Permission Response
```json
{
  "id": 12345,
  "subject": {
    "type": "group",
    "identifier": "developers",
    "id": "567890"
  },
  "operation": {
    "operation": "create",
    "targetType": "page"
  },
  "_links": {
    "self": "/wiki/rest/api/space/PROJ/permission/12345"
  }
}
```

## Code Examples

### Python - Grant Group Permission
```python
import requests

url = f"https://instance.atlassian.net/wiki/rest/api/space/{space_key}/permission"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "subject": {
        "type": "group",
        "identifier": "project-team"
    },
    "operation": {
        "operation": "create",
        "targetType": "page"
    }
}

response = requests.post(url, json=data, headers=headers)
```

### JavaScript - Check User Permissions
```javascript
async function checkUserPermissions(spaceKey, username) {
  const response = await fetch(
    `https://instance.atlassian.net/wiki/rest/api/space/${spaceKey}/permission`,
    {
      headers: {
        'Authorization': 'Bearer YOUR_TOKEN'
      }
    }
  );
  
  const permissions = await response.json();
  return permissions.results.filter(p => 
    p.subject.type === 'user' && 
    p.subject.identifier === username
  );
}
```

## Common Use Cases

1. **Role-Based Access**: Set permissions by team roles
2. **Guest Access**: Configure anonymous viewing
3. **Content Restrictions**: Limit editing to specific groups
4. **Audit Trail**: Track permission changes
5. **Bulk Updates**: Apply permissions across spaces

## Best Practices

- Follow principle of least privilege
- Use groups instead of individual users
- Document permission schemes
- Regular permission reviews
- Test permission changes in staging
- Maintain permission templates
- Avoid complex permission hierarchies
- Consider inheritance implications