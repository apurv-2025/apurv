// File: src/components/layout/Layout.js
import React from 'react';
import Header from './Header';
import Navigation from './Navigation';
import StatusBar from './StatusBar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Navigation />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      <StatusBar />
    </div>
  );
};

export default Layout;
