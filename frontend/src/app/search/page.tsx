// src/app/search/page.tsx
"use client"

import { useSearchParams } from 'next/navigation'
import { useEffect, useState, useCallback } from 'react'
import { Article } from '@/types/article'
import { Button } from '@/components/ui/button'
import { searchSimilarArticles } from '@/services/api'
import ArticleList from '@/components/features/search/ArticleList'

export default function SearchPage() {
 const searchParams = useSearchParams()
 const query = searchParams.get('q') || ''
 const [articles, setArticles] = useState<Article[]>([])
 const [page, setPage] = useState(1)
 const [hasMore, setHasMore] = useState(true)
 const [loading, setLoading] = useState(true)

 const fetchArticles = useCallback(async (pageNum: number, reset = false) => {
  try {
    setLoading(true)
    const data = await searchSimilarArticles(query, pageNum)
    setArticles(prev => reset ? data.articles : [...prev, ...data.articles])
    setHasMore(data.hasMore)
    setPage(pageNum)
  } finally {
    setLoading(false)
  }
}, [query])

useEffect(() => {
  fetchArticles(1, true) // Reset articles when query changes
}, [fetchArticles])

 const handleLoadMore = () => {
   fetchArticles(page + 1)
 }

 return (
   <div className="max-w-4xl mx-auto py-6 px-4">
     <ArticleList articles={articles} />
     {hasMore && (
       <div className="mt-6 text-center">
         <Button
           onClick={handleLoadMore}
           disabled={loading}
           variant="outline"
         >
           {loading ? 'Loading...' : 'Load More'}
         </Button>
       </div>
     )}
   </div>
 )
}