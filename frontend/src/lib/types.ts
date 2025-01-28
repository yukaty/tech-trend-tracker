export interface Article {
    id: string
    url: string
    headline: string
    description: string
    publication_date: string
    source: string
    topics: string[]
    relevance_score: number
  }

  export interface RAGResponse {
    answer: string;
    articles: Article[];
    total: number;
    hasMore: boolean;
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
