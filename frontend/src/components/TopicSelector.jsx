// frontend/src/components/TopicSelector.jsx
import React from 'react';
import { usePreferences } from '../contexts/PreferencesContext';

const allTopics = [
  'Politics',
  'Technology',
  'Business',
  'Sports',
  'Health',
  'Entertainment',
  'Science'
];

export default function TopicSelector() {
  const { topics, setTopics } = usePreferences();

  function toggleTopic(topic) {
    if (topics.includes(topic)) {
      setTopics(topics.filter(t => t !== topic));
    } else {
      setTopics([...topics, topic]);
    }
  }

  return (
    <div className="flex flex-col mb-4">
      <span className="mb-1 font-medium">Choose Topics</span>
      <div className="flex flex-wrap gap-2">
        {allTopics.map(topic => {
          const isSelected = topics.includes(topic);
          return (
            <button
              key={topic}
              onClick={() => toggleTopic(topic)}
              className={`px-3 py-1 rounded-full border ${
                isSelected
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-800'
              } hover:opacity-80`}
            >
              {topic}
            </button>
          );
        })}
      </div>
    </div>
  );
}
