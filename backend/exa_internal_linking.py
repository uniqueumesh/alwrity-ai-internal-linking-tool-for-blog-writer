import os
from exa_py import Exa
from typing import Dict, List, Any
import asyncio
from urllib.parse import urlparse

class ExaInternalLinking:
    def __init__(self):
        self.exa = Exa(api_key=os.getenv("EXA_API_KEY"))
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return ""
    
    async def find_similar_content(self, content: str, domain: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Find similar content from the same domain using EXA API
        """
        try:
            if not domain:
                return {
                    "success": False,
                    "data": None,
                    "message": "Invalid domain extracted from URL"
                }
            
            # Use EXA to search for similar content within the domain
            results = self.exa.search_and_contents(
                query=content[:500],  # Limit query length
                include_domains=[domain],
                num_results=num_results,
                use_autoprompt=True
            )
            
            # Format results for internal linking
            similar_pages = []
            for result in results.results:
                similar_pages.append({
                    "url": result.url,
                    "title": result.title,
                    "snippet": result.text[:200] + "..." if len(result.text) > 200 else result.text,
                    "relevance_score": getattr(result, 'score', 0.0)
                })
            
            return {
                "success": True,
                "data": {
                    "domain": domain,
                    "similar_pages": similar_pages,
                    "total_found": len(similar_pages)
                },
                "message": f"Found {len(similar_pages)} similar pages from {domain}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error finding similar content: {str(e)}"
            }
    
    async def generate_internal_links(self, content: str, domain: str) -> Dict[str, Any]:
        """
        Generate internal linking suggestions with HTML links
        """
        try:
            # Find similar content
            similar_result = await self.find_similar_content(content, domain)
            
            if not similar_result["success"]:
                return similar_result
            
            similar_pages = similar_result["data"]["similar_pages"]
            
            # Generate HTML links for copy-paste
            html_links = []
            for page in similar_pages:
                html_link = f'<a href="{page["url"]}" title="{page["title"]}">{page["title"]}</a>'
                html_links.append({
                    "html": html_link,
                    "url": page["url"],
                    "title": page["title"],
                    "snippet": page["snippet"],
                    "relevance_score": page["relevance_score"]
                })
            
            return {
                "success": True,
                "data": {
                    "domain": domain,
                    "internal_links": html_links,
                    "total_suggestions": len(html_links)
                },
                "message": f"Generated {len(html_links)} internal linking suggestions"
            }
            
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error generating internal links: {str(e)}"
            }

# Global instance
exa_linking = ExaInternalLinking()

async def find_internal_linking_suggestions(content: str, url: str) -> Dict[str, Any]:
    """
    Main function to find internal linking suggestions
    """
    domain = exa_linking.extract_domain(url)
    return await exa_linking.generate_internal_links(content, domain)
