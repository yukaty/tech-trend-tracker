import ReactMarkdown from "react-markdown";
import { Calendar } from "lucide-react";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Article, RAGResponse } from "@/lib/types";

interface RAGAnswerProps {
  answer: string;
}

function RAGAnswer({ answer }: RAGAnswerProps) {
  return (
    <Card className="mb-6">
      <CardHeader>
        <h3 className="font-semibold">AI Summary</h3>
      </CardHeader>
      <CardContent>
        <ReactMarkdown className="prose text-gray-700">
          {answer}
        </ReactMarkdown>
      </CardContent>
    </Card>
  );
}

interface RAGResultListProps {
  articles: Article[];
}

function RAGResultList({ articles }: RAGResultListProps) {
  return (
    <div className="space-y-4">
      <h3 className="text-2xl font-semibold mb-6">
      Source Articles
      </h3>
      {articles.map((article) => (
        <Card key={article.id} className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <div className="flex justify-between items-center text-sm">
              <span className="text-blue-600">{article.source}</span>
              <div className="flex items-center text-gray-600">
                <Calendar className="h-4 w-4 mr-2" />
                {new Date(article.publication_date).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "short",
                  day: "numeric",
                })}
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
            <div className="mt-3 flex justify-between items-center">
              <span className="px-2 py-1 bg-blue-100 text-blue-600 text-xs rounded-full">
                {(article.relevance_score * 100).toFixed(1)}% relevant
              </span>
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

interface RAGResultsProps {
  data: RAGResponse;
}

export default function RAGResults({ data }: RAGResultsProps) {
  return (
    <div>
      <RAGAnswer answer={data.answer} />
      <RAGResultList articles={data.articles} />
    </div>
  );
}