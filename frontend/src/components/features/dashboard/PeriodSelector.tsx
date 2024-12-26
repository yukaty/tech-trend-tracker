"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const MONTHS = [
  { value: 1, label: "Jan" },
  { value: 2, label: "Feb" },
  { value: 3, label: "Mar" },
  { value: 4, label: "Apr" },
  { value: 5, label: "May" },
  { value: 6, label: "Jun" },
  { value: 7, label: "Jul" },
  { value: 8, label: "Aug" },
  { value: 9, label: "Sep" },
  { value: 10, label: "Oct" },
  { value: 11, label: "Nov" },
  { value: 12, label: "Dec" },
];

const PeriodButton = ({
  isSelected,
  onClick,
  children,
}: {
  isSelected: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) => (
  <button
    onClick={onClick}
    className={`
     px-4 py-2 rounded-md transition-all
     ${
       isSelected
         ? "bg-blue-600 text-white shadow-md"
         : "bg-gray-100 text-gray-500 hover:bg-gray-200"
     }
   `}
  >
    {children}
  </button>
);

export default function PeriodSelector({
  selectedYear = 2024,
  selectedMonth,
  onYearChange,
  onMonthChange,
}: {
  selectedYear?: number;
  selectedMonth?: number;
  onYearChange: (year: number) => void;
  onMonthChange: (month: number | undefined) => void;
}) {
  const DesktopView = (
    <div className="hidden sm:flex flex-wrap gap-2">
      <PeriodButton
        isSelected={selectedYear === 2024}
        onClick={() => onYearChange(2024)}
      >
        2024
      </PeriodButton>
      <div className="w-px h-8 bg-gray-200 mx-2 self-center" />
      <PeriodButton
        isSelected={selectedMonth === undefined}
        onClick={() => onMonthChange(undefined)}
      >
        All Months
      </PeriodButton>
      {MONTHS.map((month) => (
        <PeriodButton
          key={month.value}
          isSelected={selectedMonth === month.value}
          onClick={() => onMonthChange(month.value)}
        >
          {month.label}
        </PeriodButton>
      ))}
    </div>
  );

  const MobileView = (
    <div className="sm:hidden space-y-3 w-full px-4">
      <Select
        value={selectedYear.toString()}
        onValueChange={(val) => onYearChange(parseInt(val))}
      >
        <SelectTrigger>
          <SelectValue placeholder="Select year" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="2024">2024</SelectItem>
        </SelectContent>
      </Select>

      <Select
        value={selectedMonth?.toString() || "all"}
        onValueChange={(val) =>
          onMonthChange(val === "all" ? undefined : parseInt(val))
        }
      >
        <SelectTrigger>
          <SelectValue placeholder="Select month" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All Months</SelectItem>
          {MONTHS.map((month) => (
            <SelectItem key={month.value} value={month.value.toString()}>
              {month.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );

  return (
    <div className="flex flex-col gap-4 my-4">
      {DesktopView}
      {MobileView}
    </div>
  );
}