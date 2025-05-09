"use client";
import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useEffect, useState, useCallback } from "react";
import { RAGResponse } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { searchSimilarArticles } from "@/services/api";
import RAGResults from "@/components/features/search/RAGResults";

function SearchContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";
  const [data, setData] = useState<RAGResponse>({
    answer: "",
    articles: [],
    total: 0,
    hasMore: false
  });
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  const fetchArticles = useCallback(
    async (pageNum: number, reset = false) => {
      try {
        setLoading(true);
        const response = await searchSimilarArticles(query, pageNum);
        if (reset) {
          setData(response);
        } else {
          setData(prev => ({
            ...response,
            articles: [...prev.articles, ...response.articles],
          }));
        }
        setPage(pageNum);
      } finally {
        setLoading(false);
      }
    },
    [query]
  );

  useEffect(() => {
    fetchArticles(1, true); // Reset articles when query changes
  }, [fetchArticles]);

  const handleLoadMore = () => {
    fetchArticles(page + 1);
  };

  return (
    <div className="max-w-4xl mx-auto py-6 px-4">
      <h2 className="text-2xl font-semibold mb-6">
        Insights for &quot;{query}&quot;
      </h2>
      <RAGResults data={data} />
      {data.hasMore && (
        <div className="mt-6 text-center">
          <Button onClick={handleLoadMore} disabled={loading} variant="outline">
            {loading ? "Loading..." : "Load More"}
          </Button>
        </div>
      )}
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchContent />
    </Suspense>
  );
}