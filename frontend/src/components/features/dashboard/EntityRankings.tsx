"use client";
import React, { useState, useEffect } from "react";
import { Building2, User2, Box } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { getTrendingEntities } from "@/services/api";
import type { TrendingEntity } from "@/lib/types";
import RankingList from "./RankingList";

const TABS = [
  { id: "company", icon: Building2, label: "Companies" },
  { id: "person", icon: User2, label: "People" },
  { id: "service", icon: Box, label: "Services" }
];

interface EntityRankingsProps {
  selectedYear: number;
  selectedMonth?: number;
}

export default function EntityRankings({ selectedYear, selectedMonth }: EntityRankingsProps) {
  const [rankings, setRankings] = useState<TrendingEntity[]>([]);
  const [activeTab, setActiveTab] = useState("company");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getTrendingEntities(activeTab, selectedYear, selectedMonth);
        setRankings(data);
      } catch (error) {
        console.error('Failed to fetch rankings:', error);
      }
    };

    fetchData();
  }, [activeTab, selectedYear, selectedMonth]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Tech Industry Rankings</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="w-full mb-4">
            {TABS.map(({ id, icon: Icon, label }) => (
              <TabsTrigger key={id} value={id} className="flex-1">
                <Icon className="h-4 w-4 mr-2" />
                {label}
              </TabsTrigger>
            ))}
          </TabsList>

          {TABS.map(({ id }) => (
            <TabsContent key={id} value={id}>
              <RankingList items={rankings} />
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}