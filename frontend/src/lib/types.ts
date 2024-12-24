type Period = '7d' | '30d' | '2024';
type TimelineData = {
  keywords: { text: string; count: number; trend: number }[];
  companies: { name: string; count: number; trend: number }[];
  people: { name: string; count: number; trend: number }[];
  services: { name: string; count: number; trend: number }[];
};
