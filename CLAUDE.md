# Confluence Tool - Implementation Notes

## Modern Editor Support

### Discovery
Initially, we thought pages created via the Confluence v2 API would default to the Legacy Editor. However, testing revealed that Confluence now automatically sets the `editor` property to `v2` for all pages created via the API, enabling the modern editor by default.

### Implementation
The `create_page_modern_editor()` method implements a 3-step process:
1. Creates a blank page with minimal content
2. Checks if the editor property is already set to v2 (it usually is)
3. Updates the page with the actual content

This method is defensive and will work whether or not Confluence automatically sets the editor property.

### Key Findings
- The `editor` content property with value `v2` enables the modern editor
- Pages created via API automatically have this property set
- Content must still be in storage format, but renders properly in modern editor
- The property update endpoint expects numeric IDs, not string keys

### Test Results
All pages created during testing (IDs: 4940136475, 4940267532, 4940136507) had the editor property automatically set to v2, confirming that modern editor support is now standard for API-created pages.

## API Limitations

### Read-Only Operations
- **Labels**: Cannot be added/removed via v2 API (GET only)
- **Comments**: Cannot be created via v2 API (GET only)
- Use v1 API endpoints if these operations are required

### No Current User Endpoint
The v2 API lacks a `/users/current` endpoint. The client provides a compatibility method that returns basic auth information.

## Testing
Use `scripts/check_page_properties.py <page_id>` to inspect content properties on any page.