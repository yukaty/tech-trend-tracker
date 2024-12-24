// src/services/articles.ts
import { SearchResponse } from '@/types/article';

export async function searchSimilarArticles(query: string): Promise<SearchResponse> {
  const response = await fetch('/api/articles/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error('Failed to search articles');
  }

  return response.json();
}