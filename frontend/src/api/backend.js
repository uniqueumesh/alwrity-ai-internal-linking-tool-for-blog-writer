const API_BASE_URL = 'http://localhost:8000';

/**
 * Fetch blog content from a URL using the backend API
 * @param {string} url - The blog URL to analyze
 * @returns {Promise<Object>} - The extracted blog content
 */
export const fetchBlogContent = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze-url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'Failed to extract content');
    }

    return data.data;
  } catch (error) {
    console.error('Error fetching blog content:', error);
    throw new Error(`Failed to fetch blog content: ${error.message}`);
  }
};

/**
 * Fetch internal linking suggestions from the backend API
 * @param {string} content - The blog content to analyze
 * @param {string} url - The original blog URL
 * @returns {Promise<Object>} - The internal linking suggestions
 */
export const fetchInternalLinks = async (content, url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/internal-linking`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content, url }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.message || 'Failed to fetch internal links');
    }

    return data.data;
  } catch (error) {
    console.error('Error fetching internal links:', error);
    throw new Error(`Failed to fetch internal links: ${error.message}`);
  }
};
