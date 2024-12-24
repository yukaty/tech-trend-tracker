import { Article } from "@/types/article";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Calendar } from "lucide-react";

interface ArticleListProps {
  articles: Article[];
}

export default function ArticleList({ articles }: ArticleListProps) {
  return (
    <div className="space-y-4">
      {articles.map((article) => (
        <Card key={article.id} className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <div className="flex justify-between items-center text-sm">
              <span className="text-blue-600">{article.source}</span>
              <div className="flex items-center text-gray-600">
                <Calendar className="h-4 w-4 mr-2" />
                {new Date(article.publication_date).toLocaleDateString(
                  "en-US",
                  {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                  }
                )}
              </div>
            </div>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium mt-1 text-black hover:underline"
            >
              {article.headline}
            </a>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-700">{article.description}</p>
            <div className="mt-3 flex justify-end">
              <a
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block bg-blue-600 text-white text-xs font-medium px-4 py-2 rounded hover:bg-blue-700 transition-colors"
              >
                Read More
              </a>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
