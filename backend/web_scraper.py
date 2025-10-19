import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import asyncio
import aiohttp
import re

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def scrape_url_content(self, url: str) -> Dict[str, Any]:
        """
        Scrape and extract content from a blog URL using simple web scraping
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        return self._extract_content_from_html(html_content, url)
                    else:
                        return {
                            "success": False,
                            "data": None,
                            "message": f"Failed to fetch URL. Status code: {response.status}"
                        }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error scraping content: {str(e)}"
            }
    
    def _extract_content_from_html(self, html_content: str, url: str) -> Dict[str, Any]:
        """
        Extract and clean content from HTML
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()
            
            # Extract title
            title = ""
            if soup.title:
                title = soup.title.get_text().strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text().strip()
            
            # Extract main content - try different selectors
            content = ""
            content_selectors = [
                'article',
                'main',
                '.post-content',
                '.entry-content',
                '.content',
                '.post',
                '.article-content',
                '[role="main"]'
            ]
            
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(separator=' ', strip=True)
                    break
            
            # If no specific content area found, get body text
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(separator=' ', strip=True)
            
            # Clean up content
            content = self._clean_text(content)
            
            # Extract headings
            headings = []
            for i in range(1, 7):  # h1 to h6
                for heading in soup.find_all(f'h{i}'):
                    headings.append({
                        "text": heading.get_text().strip(),
                        "level": i,
                        "type": "html"
                    })
            
            # Extract paragraphs
            paragraphs = []
            for p in soup.find_all('p'):
                para_text = p.get_text().strip()
                if para_text and len(para_text) > 20:  # Only meaningful paragraphs
                    paragraphs.append(para_text)
            
            # Extract meta description
            meta_description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                meta_description = meta_desc.get('content', '')
            
            # Extract author
            author = ""
            author_selectors = [
                'meta[name="author"]',
                '.author',
                '.byline',
                '[rel="author"]'
            ]
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    if author_elem.name == 'meta':
                        author = author_elem.get('content', '')
                    else:
                        author = author_elem.get_text().strip()
                    break
            
            # Calculate word count
            word_count = len(content.split()) if content else 0
            
            extracted_content = {
                "url": url,
                "title": title,
                "content": content,
                "meta_description": meta_description,
                "author": author,
                "headings": headings,
                "paragraphs": paragraphs,
                "word_count": word_count,
                "char_count": len(content) if content else 0
            }
            
            return {
                "success": True,
                "data": extracted_content,
                "message": "Content successfully extracted using web scraping"
            }
            
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error processing HTML content: {str(e)}"
            }
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\-()]', '', text)
        return text.strip()

# Global instance
web_scraper = WebScraper()

async def scrape_url_content(url: str) -> Dict[str, Any]:
    """
    Main function to scrape URL content using web scraping
    """
    return await web_scraper.scrape_url_content(url)
