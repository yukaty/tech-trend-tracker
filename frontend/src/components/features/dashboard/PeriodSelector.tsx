export default function PeriodSelector({
  selectedPeriod,
  onPeriodChange,
}: {
  selectedPeriod: string;
  onPeriodChange: (period: string) => void;
}) {
  const periods = [
    { value: "2024", label: "2024 Overview" },
    { value: "30d", label: "30 Days" },
    { value: "7d", label: "7 Days" },
  ];

  return (
    <div className="inline-flex rounded-lg">
      {periods.map((period) => (
        <button
          key={period.value}
          onClick={() => onPeriodChange(period.value)}
          className={`px-4 py-2 me-2 my-4 rounded-md transition-colors ${
            selectedPeriod === period.value
              ? "bg-blue-600 text-white"
              : "bg-gray-100 hover:bg-gray-200"
          }`}
        >
          {period.label}
        </button>
      ))}
    </div>
  );
}
