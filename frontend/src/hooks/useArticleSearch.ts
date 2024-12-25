import { useState } from 'react';
import { Article } from '@/lib/types';
import { searchSimilarArticles } from '@/services/api'

export function useArticleSearch() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const searchArticles = async (query: string) => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await searchSimilarArticles(query);
      setArticles(response.articles);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search articles');
    } finally {
      setIsLoading(false);
    }
  };

  return { articles, isLoading, error, searchArticles };
}