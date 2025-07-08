#!/usr/bin/env python3
"""
Confluence Cloud REST API v2 Client
A Python client for interacting with Confluence Cloud REST API v2
"""

import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, quote
import base64


class ConfluenceClient:
    """Client for Confluence Cloud REST API v2"""
    
    def __init__(self, base_url: str, username: str, api_token: str):
        """
        Initialize Confluence client
        
        Args:
            base_url: Your Confluence instance URL (e.g., https://your-domain.atlassian.net)
            username: Your email address
            api_token: Your API token (get from https://id.atlassian.com/manage/api-tokens)
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/wiki/api/v2/"
        
        # Setup authentication
        auth_string = f"{username}:{api_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                 json_data: Optional[Dict] = None) -> requests.Response:
        """Make HTTP request to API"""
        url = urljoin(self.api_base, endpoint)
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data
        )
        
        response.raise_for_status()
        return response
    
    def _paginate(self, endpoint: str, params: Optional[Dict] = None, 
                  limit: int = 100) -> List[Dict]:
        """Handle pagination for list endpoints"""
        if params is None:
            params = {}
        
        params['limit'] = min(limit, 100)
        results = []
        
        while True:
            response = self._request('GET', endpoint, params=params)
            data = response.json()
            
            results.extend(data.get('results', []))
            
            # Check for next page
            links = response.headers.get('Link', '')
            if 'rel="next"' not in links:
                break
            
            # Extract cursor from next link
            # This is a simplified extraction - you may need to parse the Link header properly
            if '_links' in data and 'next' in data['_links']:
                next_url = data['_links']['next']
                # Extract cursor from URL
                if 'cursor=' in next_url:
                    cursor = next_url.split('cursor=')[1].split('&')[0]
                    params['cursor'] = cursor
                else:
                    break
            else:
                break
        
        return results
    
    # Space Operations
    def get_spaces(self, **params) -> List[Dict]:
        """Get all spaces"""
        return self._paginate('spaces', params)
    
    def get_space(self, space_id: str) -> Dict:
        """Get space by ID"""
        response = self._request('GET', f'spaces/{space_id}')
        return response.json()
    
    # Page Operations
    def get_pages(self, space_id: Optional[str] = None, **params) -> List[Dict]:
        """Get pages, optionally filtered by space"""
        if space_id:
            params['space-id'] = space_id
        return self._paginate('pages', params)
    
    def get_page(self, page_id: str, body_format: str = 'storage', 
                 include_labels: bool = False, include_version: bool = True) -> Dict:
        """Get page by ID"""
        params = {
            'body-format': body_format,
            'include-labels': str(include_labels).lower(),
            'include-version': str(include_version).lower()
        }
        
        response = self._request('GET', f'pages/{page_id}', params=params)
        return response.json()
    
    def create_page(self, space_id: str, title: str, content: str, 
                    parent_id: Optional[str] = None, status: str = 'current') -> Dict:
        """Create a new page"""
        data = {
            'spaceId': space_id,
            'status': status,
            'title': title,
            'body': {
                'representation': 'storage',
                'value': content
            }
        }
        
        if parent_id:
            data['parentId'] = parent_id
        
        response = self._request('POST', 'pages', json_data=data)
        return response.json()
    
    def update_page(self, page_id: str, title: str, content: str, 
                    version_number: int, status: str = 'current') -> Dict:
        """Update an existing page"""
        data = {
            'id': page_id,
            'status': status,
            'title': title,
            'body': {
                'representation': 'storage',
                'value': content
            },
            'version': {
                'number': version_number + 1,
                'message': 'Updated via API'
            }
        }
        
        response = self._request('PUT', f'pages/{page_id}', json_data=data)
        return response.json()
    
    def delete_page(self, page_id: str, purge: bool = False) -> None:
        """Delete a page (move to trash or purge)"""
        params = {'purge': 'true'} if purge else {}
        self._request('DELETE', f'pages/{page_id}', params=params)
    
    # Blog Post Operations
    def get_blogposts(self, space_id: Optional[str] = None, **params) -> List[Dict]:
        """Get blog posts, optionally filtered by space"""
        if space_id:
            params['space-id'] = space_id
        return self._paginate('blogposts', params)
    
    def create_blogpost(self, space_id: str, title: str, content: str, 
                        status: str = 'current') -> Dict:
        """Create a new blog post"""
        data = {
            'spaceId': space_id,
            'status': status,
            'title': title,
            'body': {
                'representation': 'storage',
                'value': content
            }
        }
        
        response = self._request('POST', 'blogposts', json_data=data)
        return response.json()
    
    # Comment Operations
    def get_page_comments(self, page_id: str, comment_type: str = 'footer', 
                          **params) -> List[Dict]:
        """Get comments for a page"""
        endpoint = f'pages/{page_id}/{comment_type}-comments'
        return self._paginate(endpoint, params)
    
    def create_footer_comment(self, page_id: str, content: str, 
                              parent_comment_id: Optional[str] = None) -> Dict:
        """Create a footer comment on a page"""
        data = {
            'pageId': page_id,
            'body': {
                'representation': 'storage',
                'value': content
            }
        }
        
        if parent_comment_id:
            data['parentCommentId'] = parent_comment_id
        
        response = self._request('POST', 'footer-comments', json_data=data)
        return response.json()
    
    def create_inline_comment(self, page_id: str, content: str, 
                              selection: str, selection_index: int = 0) -> Dict:
        """Create an inline comment on a page"""
        data = {
            'pageId': page_id,
            'body': {
                'representation': 'storage',
                'value': content
            },
            'inlineCommentProperties': {
                'textSelection': selection,
                'textSelectionMatchIndex': selection_index
            }
        }
        
        response = self._request('POST', 'inline-comments', json_data=data)
        return response.json()
    
    # Attachment Operations
    def get_attachments(self, page_id: Optional[str] = None, **params) -> List[Dict]:
        """Get attachments, optionally for a specific page"""
        if page_id:
            endpoint = f'pages/{page_id}/attachments'
        else:
            endpoint = 'attachments'
        
        return self._paginate(endpoint, params)
    
    def upload_attachment(self, page_id: str, file_path: str, comment: str = '') -> Dict:
        """Upload an attachment to a page"""
        # Note: File upload requires multipart/form-data which is different from JSON
        # This is a simplified example
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'comment': comment}
            
            # Temporarily remove JSON content-type for file upload
            headers = self.headers.copy()
            del headers['Content-Type']
            
            response = requests.post(
                f"{self.api_base}pages/{page_id}/attachments",
                headers=headers,
                files=files,
                data=data
            )
            
            response.raise_for_status()
            return response.json()
    
    # Search Operations
    def search_content(self, cql: str, limit: int = 100) -> List[Dict]:
        """Search content using CQL (Confluence Query Language)"""
        # Note: Search might use a different API version
        params = {
            'cql': cql,
            'limit': limit
        }
        
        # This would typically use /wiki/rest/api/content/search
        # Adjust based on your needs
        return self._paginate('search', params)
    
    # Label Operations
    def get_page_labels(self, page_id: str) -> List[Dict]:
        """Get labels for a page"""
        response = self._request('GET', f'pages/{page_id}/labels')
        return response.json().get('results', [])
    
    def add_page_label(self, page_id: str, label: str) -> Dict:
        """Add a label to a page"""
        data = {
            'name': label
        }
        
        response = self._request('POST', f'pages/{page_id}/labels', json_data=data)
        return response.json()
    
    # User Operations
    def get_current_user(self) -> Dict:
        """Get information about the current user"""
        response = self._request('GET', 'user/current')
        return response.json()
    
    # Version Operations
    def get_page_versions(self, page_id: str) -> List[Dict]:
        """Get version history for a page"""
        return self._paginate(f'pages/{page_id}/versions')
    
    # Classification Level Operations
    def get_classification_levels(self) -> List[Dict]:
        """Get available classification levels"""
        response = self._request('GET', 'classification-levels')
        return response.json().get('results', [])
    
    def set_page_classification(self, page_id: str, level_id: str) -> Dict:
        """Set classification level for a page"""
        data = {
            'classificationLevelId': level_id
        }
        
        response = self._request('PUT', f'pages/{page_id}/classification-level', 
                                 json_data=data)
        return response.json()


# Example usage
if __name__ == '__main__':
    # Initialize client
    client = ConfluenceClient(
        base_url='https://your-domain.atlassian.net',
        username='your-email@example.com',
        api_token='your-api-token'
    )
    
    # Example: Get all spaces
    try:
        spaces = client.get_spaces()
        print(f"Found {len(spaces)} spaces")
        
        for space in spaces[:5]:  # Print first 5
            print(f"- {space.get('name')} (ID: {space.get('id')})")
    
    except requests.exceptions.HTTPError as e:
        print(f"API Error: {e}")
        print(f"Response: {e.response.text}")
    
    # Example: Create a page
    try:
        new_page = client.create_page(
            space_id='12345',
            title='API Test Page',
            content='<p>This page was created via the API!</p>'
        )
        print(f"Created page: {new_page.get('title')} (ID: {new_page.get('id')})")
    
    except requests.exceptions.HTTPError as e:
        print(f"Failed to create page: {e}")
    
    # Example: Search for pages
    try:
        # Search using CQL
        results = client.search_content('type=page AND text~"API"')
        print(f"Found {len(results)} pages containing 'API'")
    
    except requests.exceptions.HTTPError as e:
        print(f"Search failed: {e}")