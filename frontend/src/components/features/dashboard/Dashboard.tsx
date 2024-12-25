"use client";
import { useState } from "react";
import PeriodSelector from "./PeriodSelector";
import EntityRankings from "./EntityRankings";
import TopKeywords from "./TopKeywords";

export default function Dashboard() {
  const [selectedYear, setSelectedYear] = useState(2024);
  const [selectedMonth, setSelectedMonth] = useState<number | undefined>(undefined);

  return (
    <>
      <PeriodSelector
        selectedYear={selectedYear}
        selectedMonth={selectedMonth}
        onYearChange={setSelectedYear}
        onMonthChange={setSelectedMonth}
      />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <EntityRankings
            selectedYear={selectedYear}
            selectedMonth={selectedMonth}
          />
        </div>
        <TopKeywords
          selectedYear={selectedYear}
          selectedMonth={selectedMonth}
        />
      </div>
    </>
  );
}