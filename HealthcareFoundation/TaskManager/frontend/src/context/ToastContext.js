// src/context/ToastContext.js
import React, { createContext, useContext, useReducer } from 'react';

const ToastContext = createContext();

const initialState = {
  toasts: []
};

const toastReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_TOAST':
      return {
        ...state,
        toasts: [...state.toasts, { ...action.payload, id: Date.now() }]
      };
    case 'REMOVE_TOAST':
      return {
        ...state,
        toasts: state.toasts.filter(toast => toast.id !== action.payload)
      };
    case 'CLEAR_TOASTS':
      return {
        ...state,
        toasts: []
      };
    default:
      return state;
  }
};

export const ToastProvider = ({ children }) => {
  const [state, dispatch] = useReducer(toastReducer, initialState);

  const addToast = (message, type = 'info', duration = 5000) => {
    const toast = { message, type, duration };
    dispatch({ type: 'ADD_TOAST', payload: toast });

    if (duration > 0) {
      setTimeout(() => {
        removeToast(toast.id);
      }, duration);
    }
  };

  const removeToast = (id) => {
    dispatch({ type: 'REMOVE_TOAST', payload: id });
  };

  const clearToasts = () => {
    dispatch({ type: 'CLEAR_TOASTS' });
  };

  const value = {
    toasts: state.toasts,
    addToast,
    removeToast,
    clearToasts
  };

  return (
    <ToastContext.Provider value={value}>
      {children}
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};
