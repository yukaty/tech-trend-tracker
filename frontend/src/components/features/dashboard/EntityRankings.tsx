// src/components/features/dashboard/EntityRankings.tsx
"use client";
import React, { useState } from "react";
import { Building2, User2, Box, TrendingUp } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

import RankingList from "./RankingList";

// Mock data for rankings
const mockData = {
  companies: [
    { name: 'OpenAI', count: 245, trend: 85 },
    { name: 'Microsoft', count: 189, trend: 45 },
    { name: 'Google', count: 156, trend: 32 },
    { name: 'NVIDIA', count: 134, trend: 78 },
    { name: 'Meta', count: 98, trend: 23 }
  ],
  people: [
    { name: 'Sam Altman', count: 156, trend: 92 },
    { name: 'Sundar Pichai', count: 89, trend: 34 },
    { name: 'Mark Zuckerberg', count: 76, trend: 28 },
    { name: 'Jensen Huang', count: 67, trend: 65 },
    { name: 'Satya Nadella', count: 54, trend: 41 }
  ],
  services: [
    { name: 'ChatGPT', count: 312, trend: 88 },
    { name: 'GitHub Copilot', count: 145, trend: 56 },
    { name: 'Azure AI', count: 123, trend: 43 },
    { name: 'Gemini', count: 98, trend: 95 },
    { name: 'AWS Lambda', count: 87, trend: 32 }
  ]
}


export default function EntityRankings({
  selectedPeriod,
}: {
  selectedPeriod: string;
}) {
  // const [data, setData] = useState({
  //   companies: [],
  //   people: [],
  //   services: [],
  // });

  // useEffect(() => {
  //   fetch(`/api/industry-rankings?period=${selectedPeriod}`)
  //     .then((res) => res.json())
  //     .then((data) => setData(data));
  // }, [selectedPeriod]);

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Tech Industry Rankings</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="companies" className="w-full">
          <TabsList className="w-full mb-4">
            <TabsTrigger value="companies" className="flex-1">
              <Building2 className="h-4 w-4 mr-2" />
              Companies
            </TabsTrigger>
            <TabsTrigger value="people" className="flex-1">
              <User2 className="h-4 w-4 mr-2" />
              People
            </TabsTrigger>
            <TabsTrigger value="services" className="flex-1">
              <Box className="h-4 w-4 mr-2" />
              Services
            </TabsTrigger>
          </TabsList>

          {["companies", "people", "services"].map((category) => (
            <TabsContent key={category} value={category}>
              <div className="space-y-3">
                {mockData[category].map((item, index) => (
                  <div
                    key={item.name}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-all"
                  >
                    <div className="flex items-center gap-4">
                      <span className="text-xl font-bold text-blue-600 w-8">
                        #{index + 1}
                      </span>
                      <div>
                        <div className="font-medium">{item.name}</div>
                        <div className="text-sm text-gray-500">
                          {item.count} mentions
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center text-emerald-600">
                      <span>+{item.trend}%</span>
                      <TrendingUp className="h-4 w-4 ml-2" />
                    </div>
                  </div>
                ))}
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}
