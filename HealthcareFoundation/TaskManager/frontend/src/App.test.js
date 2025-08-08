// src/App.test.js
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders task management app', () => {
  render(<App />);
  const titleElement = screen.getByText(/taskmanager/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders sidebar navigation', () => {
  render(<App />);
  const tasksLink = screen.getByText(/tasks/i);
  const clientsLink = screen.getByText(/clients/i);
  expect(tasksLink).toBeInTheDocument();
  expect(clientsLink).toBeInTheDocument();
});
