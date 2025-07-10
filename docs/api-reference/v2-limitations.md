# Confluence v2 API Limitations

## Critical Limitations

### 1. Storage Format Only (Modern Editor Support Available)

**Update**: While the v2 API only supports creating content in the `storage` format, Confluence now automatically configures pages created via API to use the modern editor by setting the `editor` property to `v2`.

**Current Behavior**:
- Pages created via v2 API automatically have the `editor` property set to `v2`
- This enables the modern editor without additional configuration
- Content must still be provided in storage format, not ADF
- The modern editor will properly render storage format content

**Details**:
- **For Creating Content**: Only `storage` representation is supported
- **For Reading Content**: Both `storage` and `atlas_doc_format` (ADF) are supported
- The modern editor uses Atlassian Document Format (ADF), but v2 API doesn't support creating pages with ADF

**Workaround**:
- Use v1 API if modern editor support is critical
- Create content via storage format and manually convert in the UI
- Consider using Confluence Cloud's GraphQL API (if available) for modern format support
- **Recommended**: Use the 3-step process implemented in `create_page_modern_editor()`:
  1. Create a blank page with title only
  2. Set the `editor` content property to `v2`
  3. Update the page with actual content
  
  This ensures pages open in the modern editor by default.

### 2. No Current User Endpoint

The v2 API does not provide a `/users/current` endpoint to get authenticated user information.

**Workaround**: Store user info during authentication or use bulk user lookup.

### 3. Read-Only Operations

Several operations are read-only in v2:

#### Labels
- Can retrieve labels but cannot add/remove them
- No POST/PUT/DELETE endpoints for label management

#### Comments
- Can retrieve comments but cannot create them
- No POST endpoints for footer or inline comments

### 4. Limited Content Types

While v2 introduces new content types (DATABASES, EMBEDS, FOLDERS, WHITEBOARDS), creating traditional content is limited to the storage format.

## Best Practices

1. **Check Format Requirements**: Always verify if your use case requires modern editor compatibility
2. **Consider v1 API**: For features requiring modern editor or label/comment management
3. **Plan for Migration**: Be aware that content created via v2 API may need manual migration to modern editor
4. **Test Formatting**: Always test how your storage format content appears in both editors

## Storage Format Notes

### Avoid These Elements
- `<time>` tags - These can cause rendering errors
- Complex custom attributes that aren't part of Confluence storage format
- Modern HTML5 semantic elements that Confluence doesn't recognize

### Safe Elements
- Basic HTML tags: `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`, `<li>`, `<table>`, etc.
- Confluence macros: `<ac:structured-macro>`, `<ac:parameter>`, etc.
- Standard formatting: `<strong>`, `<em>`, `<code>`, `<pre>`
- Links and anchors: `<a href="">`, `id` attributes for anchors