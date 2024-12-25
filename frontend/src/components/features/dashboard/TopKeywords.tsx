"use client";
import { useEffect, useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { getTrendingKeywords } from "@/services/api";
import type { TrendingEntity } from "@/lib/types";
import RankingList from "./RankingList";

interface TopKeywordsProps {
  selectedYear: number;
  selectedMonth?: number;
}

export default function TopKeywords({ selectedYear, selectedMonth }: TopKeywordsProps) {
  const [keywords, setKeywords] = useState<TrendingEntity[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getTrendingKeywords(selectedYear, selectedMonth);
        setKeywords(data);
      } catch (error) {
        console.error('Failed to fetch keywords:', error);
      }
    };

    fetchData();
  }, [selectedYear, selectedMonth]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Keywords</CardTitle>
      </CardHeader>
      <CardContent>
        <RankingList items={keywords} />
      </CardContent>
    </Card>
  );
}