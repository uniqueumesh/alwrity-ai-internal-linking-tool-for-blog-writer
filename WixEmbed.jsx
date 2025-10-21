// WixEmbed.jsx - Complete Wix Embed Component (~50 lines)
import React, { useState } from 'react';

const WixEmbed = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [expanded, setExpanded] = useState(false);

  const fetchBlogContent = async (url) => {
    try {
      setLoading(true);
      setError('');
      const response = await fetch('http://localhost:8000/api/analyze-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await response.json();
      if (response.ok) {
        setResults(data);
        setExpanded(true);
      } else {
        setError(data.detail || 'Failed to extract content');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) fetchBlogContent(url.trim());
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter blog URL..."
          style={{ width: '100%', padding: '12px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '16px' }}
          required
        />
        <button
          type="submit"
          disabled={loading}
          style={{ 
            width: '100%', marginTop: '10px', padding: '12px', 
            backgroundColor: loading ? '#ccc' : '#007bff', 
            color: 'white', border: 'none', borderRadius: '4px', 
            fontSize: '16px', cursor: loading ? 'not-allowed' : 'pointer' 
          }}
        >
          {loading ? 'Extracting...' : 'Research Blog Content'}
        </button>
      </form>

      {error && (
        <div style={{ padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '10px' }}>
          {error}
        </div>
      )}

      {results && (
        <div style={{ border: '1px solid #ddd', borderRadius: '4px', overflow: 'hidden' }}>
          <button
            onClick={() => setExpanded(!expanded)}
            style={{ 
              width: '100%', padding: '12px', backgroundColor: '#f8f9fa', 
              border: 'none', cursor: 'pointer', fontSize: '16px', fontWeight: 'bold' 
            }}
          >
            {expanded ? '▼ Hide Results' : '▶ Show Results'}
          </button>
          
          {expanded && (
            <div style={{ padding: '20px', backgroundColor: 'white' }}>
              <h2 style={{ margin: '0 0 15px 0', color: '#333' }}>{results.title}</h2>
              
              {results.metadata && (
                <div style={{ marginBottom: '15px', fontSize: '14px', color: '#666' }}>
                  {results.metadata.author && <span>Author: {results.metadata.author} | </span>}
                  {results.metadata.word_count && <span>Words: {results.metadata.word_count} | </span>}
                  {results.metadata.character_count && <span>Characters: {results.metadata.character_count}</span>}
                </div>
              )}

              <div style={{ lineHeight: '1.6', color: '#333' }}>
                {results.content.split('\n').map((paragraph, i) => 
                  paragraph.trim() && <p key={i} style={{ marginBottom: '10px' }}>{paragraph}</p>
                )}
              </div>

              {results.headings && results.headings.length > 0 && (
                <div style={{ marginTop: '20px' }}>
                  <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>Headings:</h3>
                  <ul style={{ margin: 0, paddingLeft: '20px' }}>
                    {results.headings.map((heading, i) => (
                      <li key={i} style={{ marginBottom: '5px' }}>{heading}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default WixEmbed;
