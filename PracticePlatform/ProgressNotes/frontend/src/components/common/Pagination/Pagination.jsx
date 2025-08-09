import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { usePagination } from '../../../hooks/usePagination';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  const {
    paginationData,
    canGoPrevious,
    canGoNext,
    goToPrevious,
    goToNext,
    goToPage
  } = usePagination(currentPage, totalPages, onPageChange);

  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-center space-x-2">
      <button
        onClick={goToPrevious}
        disabled={!canGoPrevious}
        className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ChevronLeft className="h-4 w-4" />
      </button>

      {paginationData.map((page, index) => {
        if (page === '...') {
          return (
            <span key={index} className="px-3 py-2 text-gray-500">
              ...
            </span>
          );
        }

        return (
          <button
            key={index}
            onClick={() => goToPage(page)}
            className={`px-3 py-2 border rounded-md ${
              page === currentPage
                ? 'bg-blue-600 text-white border-blue-600'
                : 'text-gray-600 border-gray-300 hover:bg-gray-50'
            }`}
          >
            {page}
          </button>
        );
      })}

      <button
        onClick={goToNext}
        disabled={!canGoNext}
        className="px-3 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ChevronRight className="h-4 w-4" />
      </button>
    </div>
  );
};

export default Pagination;
