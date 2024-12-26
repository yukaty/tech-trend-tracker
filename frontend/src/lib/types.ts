export interface Article {
    id: string
    url: string
    headline: string
    description: string
    publication_date: string
    source: string
    topics: string[]
    similarity_score: number
  }

  export interface SearchResponse {
    articles: Article[];
    total: number;
    hasMore: boolean;
  }

  export interface TrendingEntity {
    name: string;
    count: number;
    trend: number;
  }