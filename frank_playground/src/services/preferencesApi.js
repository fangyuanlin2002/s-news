// src/services/preferencesApi.js

const BASE = '/preferences';

export async function fetchPreferences() {
  const res = await fetch(BASE);
  if (!res.ok) throw new Error('Failed to fetch preferences');
  return res.json();
}

export async function savePreferences(prefs) {
  const res = await fetch(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(prefs),
  });
  if (!res.ok) throw new Error('Failed to save preferences');
  return res.json();
}
