import React from 'react';
import RegionSelector from '../components/RegionSelector';
import TopicSelector from '../components/TopicSelector';
import TopStories from '../components/TopStories';

export default function Home() {
    return (
      <div className="max-w-2xl mx-auto p-6 space-y-8">
        <div>
          <h1 className="text-3xl font-bold mb-6">Welcome to S-News</h1>
          <RegionSelector />
          <TopicSelector />
        </div>
        <section>
          <h2 className="text-2xl font-semibold mb-4">Top Stories</h2>
          <TopStories />
        </section>
      </div>
    );
  }