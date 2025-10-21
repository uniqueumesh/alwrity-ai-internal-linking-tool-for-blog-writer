import { useState } from 'react';

const ResultsDisplay = ({ results, isVisible, onToggle, internalLinks }) => {
  if (!results) return null;

  return (
    <div className="mt-6 w-full max-w-4xl">
      <button
        onClick={onToggle}
        className="w-full bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-between"
      >
        <span>View Extracted Content</span>
        <span className={`transform transition-transform duration-200 ${isVisible ? 'rotate-180' : ''}`}>
          ▼
        </span>
      </button>
      
      {isVisible && (
        <div className="mt-4 bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
          {/* Title */}
          {results.title && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Title</h2>
              <p className="text-lg text-gray-700">{results.title}</p>
            </div>
          )}

          {/* Metadata */}
          <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            {results.author && (
              <div className="bg-gray-50 p-3 rounded">
                <h3 className="text-sm font-medium text-gray-600 mb-1">Author</h3>
                <p className="text-gray-900">{results.author}</p>
              </div>
            )}
            {results.word_count && (
              <div className="bg-gray-50 p-3 rounded">
                <h3 className="text-sm font-medium text-gray-600 mb-1">Word Count</h3>
                <p className="text-gray-900">{results.word_count.toLocaleString()}</p>
              </div>
            )}
            {results.char_count && (
              <div className="bg-gray-50 p-3 rounded">
                <h3 className="text-sm font-medium text-gray-600 mb-1">Character Count</h3>
                <p className="text-gray-900">{results.char_count.toLocaleString()}</p>
              </div>
            )}
          </div>

          {/* Headings */}
          {results.headings && results.headings.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Headings</h3>
              <div className="space-y-2">
                {results.headings.map((heading, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      H{heading.level}
                    </span>
                    <span className="text-gray-700">{heading.text}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Content */}
          {results.content && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Content</h3>
              <div className="prose max-w-none">
                {results.content.split('\n').map((paragraph, index) => (
                  paragraph.trim() && (
                    <p key={index} className="text-gray-700 mb-4 leading-relaxed">
                      {paragraph}
                    </p>
                  )
                ))}
              </div>
            </div>
          )}

          {/* Meta Description */}
          {results.meta_description && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Meta Description</h3>
              <p className="text-gray-600 italic">{results.meta_description}</p>
            </div>
          )}

          {/* Internal Links Section */}
          {internalLinks && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Internal Linking Suggestions</h3>
              <div className="space-y-4">
                {internalLinks.internal_links?.map((link, index) => (
                  <div key={index} className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-blue-900">{link.title}</h4>
                      <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        {Math.round(link.relevance_score * 100)}% match
                      </span>
                    </div>
                    <p className="text-sm text-blue-700 mb-3">{link.snippet}</p>
                    <div className="bg-white p-3 rounded border">
                      <p className="text-xs text-gray-600 mb-1">Copy this HTML link:</p>
                      <code className="text-xs bg-gray-100 p-2 rounded block break-all">
                        {link.html}
                      </code>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
