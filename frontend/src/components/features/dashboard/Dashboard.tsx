// src/components/features/dashboard/Dashboard.tsx
"use client";
import { useState } from "react";
import PeriodSelector from "./PeriodSelector";
import EntityRankings from "./EntityRankings";
import TopKeywords from "./TopKeywords";

export default function Dashboard() {
  const [selectedPeriod, setSelectedPeriod] = useState("2024");

  return (
    <>
      <PeriodSelector
        selectedPeriod={selectedPeriod}
        onPeriodChange={setSelectedPeriod}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <EntityRankings selectedPeriod={selectedPeriod} />
        </div>
        <TopKeywords selectedPeriod={selectedPeriod} />
      </div>
    </>
  );
}
