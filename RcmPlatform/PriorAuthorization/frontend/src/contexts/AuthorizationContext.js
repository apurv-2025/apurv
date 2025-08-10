// File: src/contexts/AuthorizationContext.js - Main State Management
import React, { createContext, useContext, useReducer } from 'react';

const AuthorizationContext = createContext();

export const useAuthorization = () => {
  const context = useContext(AuthorizationContext);
  if (!context) {
    throw new Error('useAuthorization must be used within AuthorizationProvider');
  }
  return context;
};

const initialState = {
  requests: [],
  patients: [],
  loading: false,
  error: null
};

const authorizationReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    
    case 'ADD_REQUEST':
      return { 
        ...state, 
        requests: [action.payload, ...state.requests],
        loading: false 
      };
    
    case 'UPDATE_REQUEST':
      return {
        ...state,
        requests: state.requests.map(req =>
          req.id === action.payload.id ? { ...req, ...action.payload } : req
        )
      };
    
    case 'ADD_PATIENT':
      return { 
        ...state, 
        patients: [action.payload, ...state.patients],
        loading: false 
      };
    
    case 'UPDATE_PATIENT':
      return {
        ...state,
        patients: state.patients.map(patient =>
          patient.id === action.payload.id ? { ...patient, ...action.payload } : patient
        )
      };
    
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    
    default:
      return state;
  }
};

export const AuthorizationProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authorizationReducer, initialState);

  const value = {
    ...state,
    dispatch
  };

  return (
    <AuthorizationContext.Provider value={value}>
      {children}
    </AuthorizationContext.Provider>
  );
};

