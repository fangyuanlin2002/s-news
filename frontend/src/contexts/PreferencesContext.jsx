// src/contexts/PreferencesContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchPreferences, savePreferences } from '../services/preferencesApi';

const PrefContext = createContext();

export function PreferencesProvider({ children }) {
  const [region, setRegion] = useState('Global');
  const [topics, setTopics] = useState([]);

  // 1) Load from server on mount
  useEffect(() => {
    fetchPreferences()
      .then(({ region, topics }) => {
        setRegion(region);
        setTopics(topics);
      })
      .catch(console.error);
  }, []);

  // 2) Save whenever they change
  useEffect(() => {
    // avoid saving before initial load
    savePreferences({ region, topics }).catch(console.error);
  }, [region, topics]);

  return (
    <PrefContext.Provider value={{ region, setRegion, topics, setTopics }}>
      {children}
    </PrefContext.Provider>
  );
}

export function usePreferences() {
  const ctx = useContext(PrefContext);
  if (!ctx) throw new Error('usePreferences must be inside PreferencesProvider');
  return ctx;
}
