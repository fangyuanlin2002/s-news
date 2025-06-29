// src/config/topics.js
/** @type {TopicNode[]} */
export const TOPICS = [
    {
      id: 'politics',
      name: 'Politics',
      children: [
        { id: 'elections', name: 'Elections' },
        { id: 'diplomacy', name: 'Diplomacy' },
      ]
    },
    {
      id: 'technology',
      name: 'Technology',
      children: [
        { id: 'ai', name: 'AI' },
        { id: 'mobile', name: 'Mobile' },
      ]
    },
    // …etc
  ];
  