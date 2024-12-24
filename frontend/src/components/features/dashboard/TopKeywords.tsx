"use client";

import { TrendingUp } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function TopKeywords({
  selectedPeriod,
}: {
  selectedPeriod: string;
}) {
  const keywords = [
    { text: "Artificial Intelligence", trend: 85 },
    { text: "Machine Learning", trend: 62 },
    { text: "Cloud Computing", trend: 56 },
    { text: "Cybersecurity", trend: 44 },
    { text: "Blockchain", trend: 38 },
  ];

  // const [keywords, setKeywords] = useState([]);
  // useEffect(() => {
  //   fetch(`/api/top-keywords?period=${selectedPeriod}`)
  //     .then((res) => res.json())
  //     .then((data) => setKeywords(data));
  // }, [selectedPeriod]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Keywords</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {keywords.map((keyword, index) => (
            <div
              key={keyword.text}
              className="flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 rounded-lg"
            >
              <div className="flex items-center gap-3">
                <span className="text-lg font-semibold text-blue-600">
                  #{index + 1}
                </span>
                <span className="font-medium">{keyword.text}</span>
              </div>
              <div className="flex items-center text-emerald-600">
                <span>+{keyword.trend}%</span>
                <TrendingUp className="h-4 w-4 ml-2" />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
