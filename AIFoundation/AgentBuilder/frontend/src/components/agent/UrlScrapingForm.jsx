import React from 'react';
import { Globe, Loader } from 'lucide-react';

const UrlScrapingForm = ({ 
  urlInput, 
  setUrlInput, 
  isScrapingUrl, 
  handleUrlScrape 
}) => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Website Data Scraping</h3>
      <p className="text-gray-600 mb-4">Import training data from existing websites, documentation, or knowledge bases.</p>
      
      <div className="flex space-x-4">
        <div className="flex-1">
          <input
            type="url"
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            placeholder="https://example.com"
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          onClick={handleUrlScrape}
          disabled={!urlInput.trim() || isScrapingUrl}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
        >
          {isScrapingUrl ? <Loader className="w-4 h-4 animate-spin" /> : <Globe className="w-4 h-4" />}
          <span>{isScrapingUrl ? 'Scraping...' : 'Scrape URL'}</span>
        </button>
      </div>
    </div>
  );
};

export default UrlScrapingForm; 