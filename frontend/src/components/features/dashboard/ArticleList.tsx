"use client"

import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Calendar } from 'lucide-react'

export default function ArticleList({ articles }) {
 if (!articles.length) return null

 return (
   <div className="space-y-4">
     {articles.map(article => (
       <Card key={article.id} className="hover:shadow-lg transition-shadow">
         <CardHeader>
           <div className="flex justify-between items-center text-sm">
             <span className="text-blue-600">{article.source}</span>
             <div className="flex items-center text-gray-500">
               <Calendar className="h-4 w-4 mr-1" />
               {new Date(article.publication_date).toLocaleDateString()}
             </div>
           </div>
           <h3 className="font-medium mt-1">{article.headline}</h3>
         </CardHeader>
         <CardContent>
           <p className="text-sm text-gray-600">{article.description}</p>
           <div className="mt-3 flex gap-2">
             {article.topics.slice(0,3).map(topic => (
               <span key={topic} className="px-2 py-1 bg-blue-50 text-blue-600 text-xs rounded">
                 {topic}
               </span>
             ))}
           </div>
         </CardContent>
       </Card>
     ))}
   </div>
 )
}