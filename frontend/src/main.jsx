import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';                // your Tailwind imports
import App from './App';             // your top-level component
import { PreferencesProvider } from './contexts/PreferencesContext';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <PreferencesProvider>
      <App />
    </PreferencesProvider>
  </React.StrictMode>
);
