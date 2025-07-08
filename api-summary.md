# Confluence Cloud REST API v2 Summary

This document provides a structured summary of all API endpoints in the Confluence Cloud REST API v2, organized by category.

## Overview

The Confluence Cloud REST API v2 is an iteration on the existing Confluence Cloud REST API with improvements in both endpoint definitions and performance.

### Authentication
- **Method**: Basic Authentication
- **Username**: `{{username}}`
- **API Token**: `{{apiToken}}`

### Base URL Structure
- **Protocol**: `{{protocol}}`
- **Host**: `{{host}}`
- **Base Path**: `{{basePath}}`

## API Categories

### 1. Admin Key
Admin Key feature is only offered with Confluence Cloud Premium and Enterprise to organization or site admins.

**Endpoints:**
- `GET /admin-key` - Get Admin Key
- `POST /admin-key` - Enable Admin Key
- `DELETE /admin-key` - Disable Admin Key

**Key Parameters:**
- `durationInMinutes` - Optional duration for admin key (default: 10 minutes)

**Required Header for API calls with Admin Key:**
- `Atl-Confluence-With-Admin-Key: true`

### 2. Attachment
Manage file attachments on pages, blog posts, and custom content.

**Endpoints:**
- `GET /attachments` - Get all attachments
- `GET /attachments/:id` - Get attachment by ID
- `DELETE /attachments/:id` - Delete attachment
- `GET /pages/:id/attachments` - Get attachments for page
- `GET /blogposts/:id/attachments` - Get attachments for blog post
- `GET /custom-content/:id/attachments` - Get attachments for custom content
- `GET /labels/:id/attachments` - Get attachments for label

**Common Query Parameters:**
- `sort` - Sort results by field
- `cursor` - Pagination cursor
- `status` - Filter by status (current, archived)
- `mediaType` - Filter by media type
- `filename` - Filter by filename
- `limit` - Maximum results per page

### 3. Ancestors
Retrieve ancestor hierarchy for content items.

**Endpoints:**
- `GET /pages/:id/ancestors` - Get all ancestors of page
- `GET /whiteboards/:id/ancestors` - Get all ancestors of whiteboard
- `GET /databases/:id/ancestors` - Get all ancestors of database
- `GET /embeds/:id/ancestors` - Get all ancestors of Smart Link
- `GET /folders/:id/ancestors` - Get all ancestors of folder

**Query Parameters:**
- `limit` - Maximum number of items to return

### 4. Blog Post
Create, read, update, and delete blog posts.

**Endpoints:**
- `GET /blogposts` - Get all blog posts
- `POST /blogposts` - Create blog post
- `GET /blogposts/:id` - Get blog post by ID
- `PUT /blogposts/:id` - Update blog post
- `DELETE /blogposts/:id` - Delete blog post
- `GET /labels/:id/blogposts` - Get blog posts for label
- `GET /spaces/:id/blogposts` - Get blog posts in space

**Query Parameters:**
- `id` - Filter by blog post IDs (comma-separated)
- `space-id` - Filter by space IDs
- `status` - Filter by status (current, draft)
- `title` - Filter by title
- `body-format` - Content format to return (storage, atlas_doc_format, view)
- `private` - Create private blog post (boolean)

### 5. Children
Get child content for various content types.

**Endpoints:**
- `GET /pages/:id/children` - Get child pages
- `GET /pages/:id/direct-children` - Get direct children of page
- `GET /custom-content/:id/children` - Get child custom content
- `GET /whiteboards/:id/direct-children` - Get direct children of whiteboard
- `GET /databases/:id/direct-children` - Get direct children of database
- `GET /embeds/:id/direct-children` - Get direct children of Smart Link
- `GET /folders/:id/direct-children` - Get direct children of folder

**Supported Child Types:**
- Database
- Embed
- Folder
- Page
- Whiteboard

### 6. Classification Level
Manage data classification levels for content and spaces.

**Endpoints:**
- `GET /classification-levels` - Get list of classification levels
- `GET /spaces/:id/classification-level/default` - Get space default classification
- `PUT /spaces/:id/classification-level/default` - Update space default classification
- `DELETE /spaces/:id/classification-level/default` - Delete space default classification
- `GET /pages/:id/classification-level` - Get page classification level
- `PUT /pages/:id/classification-level` - Update page classification level
- `POST /pages/:id/classification-level/reset` - Reset page classification level
- Similar endpoints for blog posts, whiteboards, and databases

### 7. Comment
Manage footer and inline comments on content.

**Endpoints:**
- `GET /footer-comments` - Get all footer comments
- `POST /footer-comments` - Create footer comment
- `GET /footer-comments/:comment-id` - Get footer comment by ID
- `PUT /footer-comments/:comment-id` - Update footer comment
- `DELETE /footer-comments/:comment-id` - Delete footer comment
- `GET /footer-comments/:id/children` - Get child footer comments
- `GET /inline-comments` - Get all inline comments
- `POST /inline-comments` - Create inline comment
- `GET /inline-comments/:comment-id` - Get inline comment by ID
- `PUT /inline-comments/:comment-id` - Update inline comment
- `DELETE /inline-comments/:comment-id` - Delete inline comment
- `GET /pages/:id/footer-comments` - Get footer comments for page
- `GET /pages/:id/inline-comments` - Get inline comments for page
- Similar endpoints for blog posts, attachments, and custom content

**Comment Parameters:**
- `body-format` - Content format type
- `resolution-status` - Filter inline comments by resolution status
- `parentCommentId` - For creating replies
- `inlineCommentProperties` - For selecting text to highlight

### 8. Content
Content conversion utilities.

**Endpoints:**
- `POST /content/convert-ids-to-types` - Convert content IDs to content types

### 9. Content Properties
Manage properties attached to content items.

**Endpoints:**
- `GET /attachments/:attachment-id/properties` - Get properties for attachment
- `POST /attachments/:attachment-id/properties` - Create property for attachment
- `GET /attachments/:attachment-id/properties/:property-id` - Get specific property
- Similar patterns for other content types

### 10. Custom Content
Manage custom content types.

**Note:** The specific endpoints for custom content would follow similar patterns to pages and blog posts.

### 11. Database
Manage Confluence databases.

**Note:** Database endpoints would follow similar patterns to other content types.

### 12. Data Policies
Manage data access and retention policies.

**Note:** Specific endpoints would be related to policy management.

### 13. Descendants
Get descendant content items.

**Note:** Similar to children/ancestors but for full descendant tree.

### 14. Folder
Manage folder structures in content tree.

**Note:** Folder endpoints would follow similar patterns to other content types.

### 15. Label
Manage content labels.

**Endpoints:**
- Label management for various content types
- Getting content by label

### 16. Like
Manage likes on content.

**Note:** Like endpoints for various content types.

### 17. Operation
Content operations and permissions.

**Note:** Operations define what actions can be performed on content.

### 18. Page
Create, read, update, and delete pages.

**Endpoints:**
- `GET /pages` - Get all pages
- `POST /pages` - Create page
- `GET /pages/:id` - Get page by ID
- `PUT /pages/:id` - Update page
- `DELETE /pages/:id` - Delete page

**Key Parameters:**
- Similar to blog posts with additional page-specific options

### 19. Redactions
Manage content redactions for compliance.

**Note:** Redaction endpoints for sensitive content removal.

### 20. Smart Link
Manage Smart Links (embeds) in content tree.

**Note:** Smart Link endpoints for embedded content.

### 21. Space
Manage Confluence spaces.

**Endpoints:**
- Space CRUD operations
- Space configuration

### 22. Space Permissions
Manage permissions within spaces.

**Note:** Permission management endpoints.

### 23. Space Properties
Manage space-level properties.

**Note:** Property management for spaces.

### 24. Space Roles
Manage user roles within spaces.

**Note:** Role assignment and management.

### 25. Task
Manage tasks within content.

**Note:** Task creation and tracking endpoints.

### 26. User
User-related operations.

**Note:** User profile and preference management.

### 27. Version
Content versioning operations.

**Endpoints:**
- Version history retrieval
- Version comparison
- Rollback operations

### 28. Whiteboard
Manage Confluence whiteboards.

**Note:** Whiteboard CRUD operations similar to pages.

## Common Patterns

### Pagination
Most list endpoints support pagination using:
- `cursor` - Opaque cursor for next page
- `limit` - Number of results per page
- Response includes `Link` header with next URL

### Content Formats
Many endpoints support `body-format` parameter:
- `storage` - Raw storage format
- `atlas_doc_format` - Atlas Document Format
- `view` - Rendered view format

### Status Filters
Content can be filtered by status:
- `current` - Published content
- `draft` - Draft content
- `archived` - Archived content
- `trashed` - Deleted content

### Include Parameters
Many GET endpoints support include parameters to fetch related data:
- `include-labels`
- `include-properties`
- `include-operations`
- `include-likes`
- `include-versions`
- `include-collaborators`

### Permissions
All endpoints require appropriate permissions:
- Global: "Can use" Confluence permission
- Space: View/edit space permissions
- Content: View/edit content permissions
- Admin: Space or site admin for certain operations