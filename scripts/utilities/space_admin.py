#!/usr/bin/env python3
"""
Space Administration Utilities

Manage Confluence spaces, permissions, and administrative tasks.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confluence_client import ConfluenceClient
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpaceAdmin:
    """Handle space administration tasks."""
    
    def __init__(self, client: ConfluenceClient):
        """Initialize space admin."""
        self.client = client
    
    def create_project_space(self, project_name: str, description: str, 
                           team_members: List[str]) -> Dict:
        """
        Create a new project space with standard structure.
        
        Args:
            project_name: Name of the project
            description: Project description
            team_members: List of user emails
            
        Returns:
            Created space data
        """
        # Generate space key
        key = ''.join(word[0] for word in project_name.split()[:3]).upper()
        key = key[:10]  # Max 10 chars
        
        logger.info(f"Creating space '{project_name}' with key '{key}'")
        
        # Create space
        space = self.client.create_space(
            key=key,
            name=project_name,
            description=description
        )
        
        space_id = int(space['id'])
        logger.info(f"Created space: {space['name']} (ID: {space_id})")
        
        # Create standard pages
        self._create_space_structure(space_id, project_name)
        
        # Set up permissions (would need additional API endpoints)
        # self._setup_permissions(space_id, team_members)
        
        return space
    
    def _create_space_structure(self, space_id: int, project_name: str):
        """Create standard page structure for new space."""
        
        # Create home page
        home = self.client.create_page(
            space_id=space_id,
            title=f"{project_name} Home",
            content=f"""
            <h1>Welcome to {project_name}</h1>
            <p>This is the home page for the {project_name} space.</p>
            
            <h2>Quick Links</h2>
            <ul>
                <li><a href="#meeting-notes">Meeting Notes</a></li>
                <li><a href="#documentation">Documentation</a></li>
                <li><a href="#resources">Resources</a></li>
            </ul>
            """
        )
        
        # Create standard sections
        sections = [
            {
                'title': 'Meeting Notes',
                'content': '<h1>Meeting Notes</h1><p>Archive of all project meetings.</p>'
            },
            {
                'title': 'Documentation', 
                'content': '<h1>Documentation</h1><p>Technical and project documentation.</p>'
            },
            {
                'title': 'Resources',
                'content': '<h1>Resources</h1><p>Links, files, and other resources.</p>'
            },
            {
                'title': 'Team',
                'content': '<h1>Team</h1><p>Team members and contact information.</p>'
            }
        ]
        
        for section in sections:
            page = self.client.create_page(
                space_id=space_id,
                title=section['title'],
                content=section['content'],
                parent_id=home['id']
            )
            logger.info(f"  Created section: {page['title']}")
    
    def clone_space_structure(self, source_space_id: int, target_space_id: int):
        """
        Clone page structure from one space to another.
        
        Args:
            source_space_id: Source space ID
            target_space_id: Target space ID
        """
        logger.info(f"Cloning structure from space {source_space_id} to {target_space_id}")
        
        # Get all pages in source space
        cql = f"space = {source_space_id} AND type = page"
        pages = self.client.search_pages(cql)
        
        # Build parent-child relationships
        page_tree = {}
        for page in pages:
            parent_id = page.get('parentId', 'root')
            if parent_id not in page_tree:
                page_tree[parent_id] = []
            page_tree[parent_id].append(page)
        
        # Clone pages maintaining hierarchy
        mapping = {}
        self._clone_page_tree(page_tree, 'root', None, target_space_id, mapping)
        
        logger.info(f"Cloned {len(mapping)} pages")
        return mapping
    
    def _clone_page_tree(self, tree: Dict, current_id: str, parent_id: Optional[str],
                        target_space_id: int, mapping: Dict):
        """Recursively clone page tree."""
        if current_id not in tree:
            return
        
        for page in tree[current_id]:
            # Get full page content
            full_page = self.client.get_page(page['id'], expand=['body.storage'])
            
            # Create in target space
            new_page = self.client.create_page(
                space_id=target_space_id,
                title=full_page['title'],
                content=full_page['body']['storage']['value'],
                parent_id=parent_id
            )
            
            mapping[page['id']] = new_page['id']
            logger.info(f"  Cloned: {page['title']}")
            
            # Clone children
            self._clone_page_tree(tree, page['id'], new_page['id'], 
                                target_space_id, mapping)
    
    def audit_space_content(self, space_id: int) -> Dict:
        """
        Audit space content and generate report.
        
        Args:
            space_id: Space ID to audit
            
        Returns:
            Audit report data
        """
        logger.info(f"Auditing space {space_id}")
        
        audit = {
            'space_id': space_id,
            'audit_date': datetime.now().isoformat(),
            'statistics': {
                'total_pages': 0,
                'pages_by_status': {},
                'pages_by_last_update': {
                    'last_7_days': 0,
                    'last_30_days': 0,
                    'last_90_days': 0,
                    'older': 0
                },
                'orphan_pages': 0,
                'pages_without_content': 0
            },
            'issues': []
        }
        
        # Get all pages
        cql = f"space = {space_id} AND type = page"
        pages = self.client.search_pages(cql)
        audit['statistics']['total_pages'] = len(pages)
        
        # Analyze pages
        page_ids = {p['id'] for p in pages}
        today = datetime.now()
        
        for page in pages:
            # Check status
            status = page.get('status', 'current')
            audit['statistics']['pages_by_status'][status] = \
                audit['statistics']['pages_by_status'].get(status, 0) + 1
            
            # Check last update
            last_modified = datetime.fromisoformat(
                page.get('version', {}).get('when', '').replace('Z', '+00:00')
            )
            days_old = (today - last_modified).days
            
            if days_old <= 7:
                audit['statistics']['pages_by_last_update']['last_7_days'] += 1
            elif days_old <= 30:
                audit['statistics']['pages_by_last_update']['last_30_days'] += 1
            elif days_old <= 90:
                audit['statistics']['pages_by_last_update']['last_90_days'] += 1
            else:
                audit['statistics']['pages_by_last_update']['older'] += 1
            
            # Check for orphans
            parent_id = page.get('parentId')
            if parent_id and parent_id not in page_ids:
                audit['statistics']['orphan_pages'] += 1
                audit['issues'].append({
                    'type': 'orphan_page',
                    'page_id': page['id'],
                    'page_title': page['title'],
                    'parent_id': parent_id
                })
            
            # Check for empty pages
            full_page = self.client.get_page(page['id'], expand=['body.storage'])
            content = full_page['body']['storage']['value']
            if len(content.strip()) < 50:  # Very short content
                audit['statistics']['pages_without_content'] += 1
                audit['issues'].append({
                    'type': 'empty_page',
                    'page_id': page['id'],
                    'page_title': page['title']
                })
        
        logger.info(f"Audit complete. Found {len(audit['issues'])} issues.")
        return audit
    
    def backup_space_permissions(self, space_id: int) -> Dict:
        """
        Backup space permissions configuration.
        
        Args:
            space_id: Space ID
            
        Returns:
            Permissions backup data
        """
        logger.info(f"Backing up permissions for space {space_id}")
        
        # Get space details
        space = self.client.get_space(space_id)
        
        backup = {
            'space_id': space_id,
            'space_key': space['key'],
            'space_name': space['name'],
            'backup_date': datetime.now().isoformat(),
            'permissions': []
        }
        
        # Note: Full permissions API would be needed here
        # This is a simplified example
        
        return backup
    
    def generate_space_report(self, space_id: int, output_file: str):
        """
        Generate comprehensive space report.
        
        Args:
            space_id: Space ID
            output_file: Output HTML file path
        """
        logger.info(f"Generating report for space {space_id}")
        
        # Get space info
        space = self.client.get_space(space_id)
        
        # Audit content
        audit = self.audit_space_content(space_id)
        
        # Generate HTML report
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Space Report - {space['name']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2 {{ color: #0052cc; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .warning {{ color: #ff5630; }}
                .info {{ color: #0065ff; }}
            </style>
        </head>
        <body>
            <h1>Space Report: {space['name']}</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Space Information</h2>
            <table>
                <tr><th>Property</th><th>Value</th></tr>
                <tr><td>Space Key</td><td>{space['key']}</td></tr>
                <tr><td>Space ID</td><td>{space['id']}</td></tr>
                <tr><td>Type</td><td>{space.get('type', 'N/A')}</td></tr>
                <tr><td>Status</td><td>{space.get('status', 'N/A')}</td></tr>
            </table>
            
            <h2>Content Statistics</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Pages</td><td>{audit['statistics']['total_pages']}</td></tr>
                <tr><td>Pages updated in last 7 days</td><td>{audit['statistics']['pages_by_last_update']['last_7_days']}</td></tr>
                <tr><td>Pages updated in last 30 days</td><td>{audit['statistics']['pages_by_last_update']['last_30_days']}</td></tr>
                <tr><td>Pages updated in last 90 days</td><td>{audit['statistics']['pages_by_last_update']['last_90_days']}</td></tr>
                <tr><td>Older pages</td><td>{audit['statistics']['pages_by_last_update']['older']}</td></tr>
                <tr><td>Orphan Pages</td><td class="warning">{audit['statistics']['orphan_pages']}</td></tr>
                <tr><td>Empty Pages</td><td class="warning">{audit['statistics']['pages_without_content']}</td></tr>
            </table>
            
            <h2>Issues Found</h2>
            """
        
        if audit['issues']:
            html += """
            <table>
                <tr><th>Type</th><th>Page</th><th>Details</th></tr>
            """
            for issue in audit['issues']:
                html += f"""
                <tr>
                    <td class="warning">{issue['type']}</td>
                    <td>{issue['page_title']}</td>
                    <td>{issue.get('details', 'N/A')}</td>
                </tr>
                """
            html += "</table>"
        else:
            html += "<p class='info'>No issues found!</p>"
        
        html += """
        </body>
        </html>
        """
        
        # Save report
        with open(output_file, 'w') as f:
            f.write(html)
        
        logger.info(f"Report saved to {output_file}")
        return audit


def main():
    """Example usage of space admin utilities."""
    # Configuration
    DOMAIN = os.getenv('CONFLUENCE_DOMAIN')
    EMAIL = os.getenv('CONFLUENCE_EMAIL')
    API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')
    
    if not all([DOMAIN, EMAIL, API_TOKEN]):
        print("Please set CONFLUENCE_DOMAIN, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN")
        sys.exit(1)
    
    # Initialize
    client = ConfluenceClient(DOMAIN, EMAIL, API_TOKEN)
    admin = SpaceAdmin(client)
    
    # Example: Create project space
    # space = admin.create_project_space(
    #     "API Testing Project",
    #     "Space for testing Confluence API",
    #     ["user1@example.com", "user2@example.com"]
    # )
    
    # Example: Audit space
    # audit = admin.audit_space_content(123456)
    # print(json.dumps(audit, indent=2))
    
    # Example: Generate report
    # admin.generate_space_report(123456, "space_report.html")
    
    logger.info("Space admin examples completed")


if __name__ == "__main__":
    main()