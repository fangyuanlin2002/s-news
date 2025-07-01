// frontend/src/components/RegionSelector.jsx
import React from 'react';
import { usePreferences } from '../contexts/PreferencesContext';

const regions = [
  'Global',
  'North America',
  'Europe',
  'Asia',
  'South America',
  'Africa',
  'Oceania'
];

export default function RegionSelector() {
  const { region, setRegion } = usePreferences();

  return (
    <div className="flex flex-col mb-4">
      <label className="mb-1 font-medium">Select Region</label>
      <select
        className="border rounded p-2"
        value={region}
        onChange={e => setRegion(e.target.value)}
      >
        {regions.map(r => (
          <option key={r} value={r}>
            {r}
          </option>
        ))}
      </select>
    </div>
  );
}
