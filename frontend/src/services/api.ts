const API_SERVER = 'http://localhost:8000/api';

export async function searchSimilarArticles(query: string, page = 1, limit = 10) {
    const res = await fetch(`${API_SERVER}/articles/similar?query=${encodeURIComponent(query)}&page=${page}&limit=${limit}`)
    if (!res.ok) throw new Error('Failed to fetch articles')
    return res.json()
  }