import re
from typing import Dict, Any, List
import asyncio

class TextAnalyzer:
    def __init__(self):
        pass
    
    async def analyze_text_content(self, content: str) -> Dict[str, Any]:
        """
        Analyze direct text content input
        """
        if not content or not content.strip():
            return {
                "success": False,
                "data": None,
                "message": "No content provided"
            }
        
        try:
            # Clean and process the text
            cleaned_content = self._clean_text(content)
            
            # Extract basic metrics
            word_count = len(cleaned_content.split())
            char_count = len(cleaned_content)
            
            # Extract keywords (simple approach)
            keywords = self._extract_keywords(cleaned_content)
            
            # Extract headings
            headings = self._extract_headings(content)
            
            # Extract paragraphs
            paragraphs = self._extract_paragraphs(cleaned_content)
            
            analysis_result = {
                "content": cleaned_content,
                "original_content": content,
                "word_count": word_count,
                "char_count": char_count,
                "keywords": keywords,
                "headings": headings,
                "paragraphs": paragraphs,
                "content_type": "text_input"
            }
            
            return {
                "success": True,
                "data": analysis_result,
                "message": "Content successfully analyzed"
            }
            
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Error analyzing content: {str(e)}"
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
    
    def _extract_keywords(self, text: str, max_keywords: int = 20) -> List[str]:
        """
        Extract keywords from text (simple frequency-based approach)
        """
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        # Filter out stop words and short words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequency
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
    
    def _extract_headings(self, text: str) -> List[Dict[str, str]]:
        """
        Extract headings from text (markdown and HTML style)
        """
        headings = []
        
        # Extract markdown headings
        markdown_pattern = r'^(#{1,6})\s+(.+)$'
        for line in text.split('\n'):
            match = re.match(markdown_pattern, line.strip())
            if match:
                level = len(match.group(1))
                heading_text = match.group(2).strip()
                headings.append({
                    "text": heading_text,
                    "level": level,
                    "type": "markdown"
                })
        
        return headings
    
    def _extract_paragraphs(self, text: str) -> List[str]:
        """
        Extract paragraphs from text
        """
        # Split by double newlines or single newlines followed by capital letters
        paragraphs = re.split(r'\n\s*\n', text)
        # Filter out empty paragraphs
        return [p.strip() for p in paragraphs if p.strip()]

# Global instance
text_analyzer = TextAnalyzer()

async def analyze_text_content(content: str) -> Dict[str, Any]:
    """
    Main function to analyze text content
    """
    return await text_analyzer.analyze_text_content(content)
