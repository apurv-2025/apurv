// src/components/Tasks/TaskCard.jsx
import React, { useState } from 'react';
import { 
  MoreVertical, 
  Edit, 
  Trash2, 
  Calendar, 
  User, 
  Paperclip,
  CheckCircle,
  Circle,
  Clock
} from 'lucide-react';

const TaskCard = ({ 
  task, 
  clientName,
  onEdit, 
  onDelete, 
  onStatusChange 
}) => {
  const [showMenu, setShowMenu] = useState(false);

  const handleStatusToggle = () => {
    const newStatus = task.status === 'completed' ? 'todo' : 'completed';
    onStatusChange(newStatus);
  };

  const getPriorityClasses = (priority) => {
    const classes = {
      high: 'priority-high',
      medium: 'priority-medium',
      low: 'priority-low',
      none: 'priority-none'
    };
    return classes[priority] || classes.none;
  };

  const isOverdue = task.dueDate && new Date(`${task.dueDate}T${task.dueTime || '23:59'}`) < new Date() && task.status !== 'completed';

  return (
    <div className="task-card">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-start space-x-3 flex-1">
          <button
            onClick={handleStatusToggle}
            className="mt-0.5 text-gray-400 hover:text-blue-600 transition-colors"
          >
            {task.status === 'completed' ? (
              <CheckCircle className="w-5 h-5 text-green-600" />
            ) : (
              <Circle className="w-5 h-5" />
            )}
          </button>

          <div className="flex-1 min-w-0">
            <h3 className={`font-medium text-gray-900 truncate ${
              task.status === 'completed' ? 'line-through text-gray-500' : ''
            }`}>
              {task.name}
            </h3>
            
            {task.description && (
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                {task.description}
              </p>
            )}
          </div>
        </div>

        {/* Menu */}
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="p-1 hover:bg-gray-100 rounded"
          >
            <MoreVertical className="w-4 h-4 text-gray-500" />
          </button>

          {showMenu && (
            <div className="absolute right-0 top-8 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-10 min-w-32">
              <button
                onClick={() => {
                  onEdit();
                  setShowMenu(false);
                }}
                className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center space-x-2"
              >
                <Edit className="w-4 h-4" />
                <span>Edit</span>
              </button>
              <button
                onClick={() => {
                  onDelete();
                  setShowMenu(false);
                }}
                className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-gray-50 flex items-center space-x-2"
              >
                <Trash2 className="w-4 h-4" />
                <span>Delete</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Priority Badge */}
      {task.priority !== 'none' && (
        <div className="mb-3">
          <span className={getPriorityClasses(task.priority)}>
            {task.priority}
          </span>
        </div>
      )}

      {/* Task Meta */}
      <div className="space-y-2 text-sm text-gray-600">
        {task.dueDate && (
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4" />
            <span className={isOverdue ? 'text-red-600 font-medium' : ''}>
              {new Date(task.dueDate).toLocaleDateString()}
              {task.dueTime && ` at ${task.dueTime}`}
            </span>
            {isOverdue && <Clock className="w-4 h-4 text-red-600" />}
          </div>
        )}

        {clientName && (
          <div className="flex items-center space-x-2">
            <User className="w-4 h-4" />
            <span>{clientName}</span>
          </div>
        )}

        {task.attachments && task.attachments.length > 0 && (
          <div className="flex items-center space-x-2">
            <Paperclip className="w-4 h-4" />
            <span>{task.attachments.length} attachment{task.attachments.length !== 1 ? 's' : ''}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskCard;
