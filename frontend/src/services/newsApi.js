// src/services/newsApi.js
const BASE_URL = 'https://newsapi.org/v2';
const KEY = import.meta.env.VITE_NEWSAPI_KEY;

// map our regions to NewsAPI country codes
const regionToCountry = {
  Global: 'us',
  'North America': 'us',
  Europe: 'gb',
  Asia: 'cn',
  'South America': 'br',
  Africa: 'za',
  Oceania: 'au'
};

export async function fetchTopHeadlines({ region, topics = [] }) {
  const country = regionToCountry[region] || 'us';
  const params = new URLSearchParams({
    apiKey: KEY,
    country,
    pageSize: '10',
  });

  // optional topic filter
  if (topics.length) {
    params.append('q', topics.join(' OR '));
  }

  const res = await fetch(`${BASE_URL}/top-headlines?${params.toString()}`);
  if (!res.ok) {
    const err = await res.json();
    console.error('NewsAPI error:', err);
    throw new Error(err.message || 'Failed to fetch headlines');
  }
  const { articles } = await res.json();
  return articles.map(a => ({
    id: a.url,
    title: a.title,
    source: a.source.name,
    url: a.url,
    publishedAt: a.publishedAt,
    description: a.description,
  }));
}
