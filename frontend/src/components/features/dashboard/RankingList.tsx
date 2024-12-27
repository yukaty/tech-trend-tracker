import { TrendingUp, TrendingDown } from 'lucide-react';
import type { TrendingEntity } from "@/lib/types";
import { useRouter } from "next/navigation";

interface RankingListProps {
  items: TrendingEntity[];
}

export default function RankingList({ items }: RankingListProps) {
  const router = useRouter();

  const handleKeywordClick = async (keyword: string) => {
    try {
      router.push(`/search/keyword?q=${encodeURIComponent(keyword)}`);
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  const renderTrendIndicator = (trend: number) => {
    if (trend === null || trend === 0) {
      return <span className="text-gray-500">-</span>;
    }

    return trend > 0 ? (
      <div className="flex items-center text-emerald-600">
        <span>+{trend}%</span>
        <TrendingUp className="h-4 w-4 ml-2" />
      </div>
    ) : (
      <div className="flex items-center text-red-600">
        <span>{trend}%</span>
        <TrendingDown className="h-4 w-4 ml-2" />
      </div>
    );
  };

  return (
    <div className="space-y-3">
      {items.map((item, index) => (
        <div
          key={item.name}
          className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100"
        >
          <div className="flex items-center gap-4">
            <span className="text-xl font-bold text-blue-600 w-8">#{index + 1}</span>
            <div>
              <button
                onClick={() => handleKeywordClick(item.name)}
                className="font-medium hover:text-blue-600 transition-colors"
              >
                {item.name}
              </button>
              <div className="text-sm text-gray-500">{item.count} mentions</div>
            </div>
          </div>
          {renderTrendIndicator(item.trend)}
        </div>
      ))}
    </div>
  );
}