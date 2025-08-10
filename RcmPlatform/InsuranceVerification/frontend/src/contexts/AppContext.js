// File: src/contexts/AppContext.js
import React, { createContext, useContext, useReducer } from 'react';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

const initialState = {
  requests: [],
  extractedData: null,
  eligibilityResult: null,
  loading: false,
  uploadedFiles: []
};

const appReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    
    case 'ADD_REQUEST':
      return { 
        ...state, 
        requests: [action.payload, ...state.requests] 
      };
    
    case 'UPDATE_REQUEST':
      return {
        ...state,
        requests: state.requests.map(req =>
          req.id === action.payload.id ? { ...req, ...action.payload } : req
        )
      };
    
    case 'SET_EXTRACTED_DATA':
      return { ...state, extractedData: action.payload };
    
    case 'SET_ELIGIBILITY_RESULT':
      return { ...state, eligibilityResult: action.payload };
    
    case 'ADD_UPLOADED_FILE':
      return {
        ...state,
        uploadedFiles: [...state.uploadedFiles, action.payload]
      };
    
    case 'CLEAR_DATA':
      return { ...state, extractedData: null, eligibilityResult: null };
    
    default:
      return state;
  }
};

export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const value = {
    ...state,
    dispatch
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};
