# Confluence API v2 Changes and Limitations

## Overview

The Confluence Cloud REST API v2 introduces several changes from v1. This document highlights key differences and limitations.

## Key Changes

### User Endpoints

#### No Current User Endpoint
- **v1**: `GET /rest/api/user/current`
- **v2**: **Not available**

The v2 API does not provide a dedicated endpoint to get the current authenticated user's information. This is a significant change from v1.

**Workarounds:**
1. Store user information during initial authentication
2. Use `POST /wiki/api/v2/users-bulk` if you have the account ID
3. Extract user info from other API responses where available

#### Bulk User Operations
- **New**: `POST /wiki/api/v2/users-bulk` - Get user details for multiple account IDs
- Requires account IDs (not emails or usernames)
- Returns user profile information for provided IDs

### Authentication
- Same methods as v1: Basic Auth with API token, OAuth 2.0
- No changes to authentication headers or token generation

### Account IDs vs Usernames
- v2 focuses on account IDs for GDPR compliance
- User keys and usernames are deprecated
- All user references should use account IDs

## API Client Adaptations

The Python client in this repository handles these limitations:

```python
# The get_current_user() method returns basic info
# since v2 doesn't have a dedicated endpoint
user = client.get_current_user()
# Returns: {'email': 'user@example.com', 'displayName': 'user', 'accountId': 'authenticated-user'}

# For actual user details, use bulk lookup if you have account IDs
users = client.get_users_bulk(['account-id-1', 'account-id-2'])
```

## Testing Authentication

Since we can't directly verify the current user, authentication is tested by:
1. Making a request to list spaces
2. If successful, authentication is working
3. If it fails with 401, credentials are invalid

## Other Notable Changes

1. **Generic Content Types**: New content types include DATABASES, EMBEDS, FOLDERS, WHITEBOARDS
2. **Improved Performance**: v2 endpoints are optimized for better performance
3. **Consistent Pagination**: Standardized pagination across all list endpoints
4. **Enhanced Filtering**: More powerful CQL queries and filtering options

## Read-Only Operations

Several operations that were available in v1 are now read-only in v2:

### Labels
- **GET** operations only - can retrieve labels but cannot add/remove them
- No POST/PUT/DELETE endpoints for label management
- Must use v1 API or UI for label modifications

### Comments
- **GET** operations only - can retrieve comments but cannot add them via v2
- No POST endpoints for creating footer or inline comments
- Must use v1 API for comment creation

### Workarounds
- Use v1 API endpoints for these operations
- Include labels during initial content creation if supported
- Use the Confluence UI for manual label/comment management

## Migration Tips

When migrating from v1 to v2:
1. Remove dependencies on `/user/current` endpoint
2. Update user identification to use account IDs
3. Test authentication using space or content endpoints
4. Handle the absence of current user info in your application logic