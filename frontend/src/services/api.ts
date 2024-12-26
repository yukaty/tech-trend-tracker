import { SearchResponse, TrendingEntity } from "@/lib/types";

const API_SERVER = process.env.NEXT_PUBLIC_API_URL
if (!API_SERVER) {
  throw new Error('NEXT_PUBLIC_API_URL environment variable is not set');
}

export async function searchSimilarArticles(query: string, page = 1, limit = 10): Promise<SearchResponse> {
  const res = await fetch(`${API_SERVER}/search/similar?query=${encodeURIComponent(query)}&page=${page}&limit=${limit}`)
  if (!res.ok) throw new Error('Failed to fetch articles')
  return res.json()
}

export async function searchByKeyword(keyword: string, page = 1, limit = 10): Promise<SearchResponse> {
  const res = await fetch(
    `${API_SERVER}/search/keyword?q=${encodeURIComponent(keyword)}&page=${page}&limit=${limit}`
  );
  if (!res.ok) throw new Error('Failed to fetch articles');
  return res.json();
}

export async function getTrendingEntities(category: string, year = 2024, month?: number): Promise<TrendingEntity[]> {
  const params = new URLSearchParams({
      category,
      year: year.toString(),
      ...(month && { month: month.toString() })
  })
  const res = await fetch(`${API_SERVER}/trends/entities?${params.toString()}`)
  if (!res.ok) throw new Error('Failed to fetch trending entities')
  return res.json()
}

export async function getTrendingKeywords(year = 2024, month?: number): Promise<TrendingEntity[]> {
  const params = new URLSearchParams({
      year: year.toString(),
      ...(month && { month: month.toString() })
  })
  const res = await fetch(`${API_SERVER}/trends/keywords?${params.toString()}`)
  if (!res.ok) throw new Error('Failed to fetch trending keywords')
  return res.json()
}