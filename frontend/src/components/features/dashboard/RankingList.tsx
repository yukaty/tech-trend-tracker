export default function RankingList({ items }: { items: { name: string; count: number; trend: number }[] }) {
    return (
      <div className="space-y-3">
        {items.map((item, index) => (
          <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <span>#{index + 1} {item.name} ({item.count} mentions)</span>
            <span className="text-green-600">+{item.trend}%</span>
          </div>
        ))}
      </div>
    );
  }
