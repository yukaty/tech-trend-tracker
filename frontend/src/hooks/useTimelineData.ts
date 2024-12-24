// src/hooks/useTimelineData.ts
import { useState, useEffect } from 'react';
import { fetchTimelineData } from '@/services/api';

export function useTimelineData(period: Period) {
  const [data, setData] = useState<TimelineData>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const getData = async () => {
      try {
        const response = await fetchTimelineData(period);
        setData(response);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };
    getData();
  }, [period]);

  return { data, loading, error };
}

// export function useArticleSearch();
// export function useKeywordTrends();
// export function useEntityDetails();