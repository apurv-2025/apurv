// src/components/Tasks/TaskEmptyState.jsx
import React from 'react';
import { CheckSquare } from 'lucide-react';

const TaskEmptyState = ({ onAddTask }) => {
  return (
    <div className="flex-1 flex items-center justify-center p-12">
      <div className="text-center max-w-md">
        {/* Illustration */}
        <div className="mb-8">
          <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
            <CheckSquare className="w-12 h-12 text-blue-600" />
          </div>
        </div>

        {/* Text Content */}
        <h2 className="text-xl font-semibold text-gray-900 mb-3">
          Stay organized with Tasks
        </h2>
        
        <p className="text-gray-600 mb-8 leading-relaxed">
          Keep track of your to-dos by creating tasks, setting due dates, and assigning priority levels
        </p>

        {/* CTA Button */}
        <button
          onClick={onAddTask}
          className="btn-primary"
        >
          Add task
        </button>
      </div>
    </div>
  );
};

export default TaskEmptyState;
