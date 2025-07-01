import React, { useEffect, useState } from 'react';
import { fetchTopHeadlines } from '../services/newsApi';
import { usePreferences } from '../contexts/PreferencesContext';

export default function TopStories() {
  const { region, topics } = usePreferences();
  const [stories, setStories] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTopHeadlines({ region, topics })
      .then(setStories)
      .catch(err => setError(err.message));
  }, [region, topics]);

  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (!stories.length) return <p>Loading top stories…</p>;

  return (
    <div className="space-y-4">
      {stories.map(story => (
        <a
          key={story.id}
          href={story.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block p-4 border rounded hover:shadow"
        >
          <h2 className="font-semibold">{story.title}</h2>
          <p className="text-sm text-gray-600">{story.source}</p>
          <p className="mt-1 text-gray-800">{story.description}</p>
        </a>
      ))}
    </div>
  );
}
