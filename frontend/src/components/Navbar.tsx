"use client";
import { Suspense } from "react";
import { TrendingUp, MessageSquare } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import Link from "next/link";

function NavbarContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [query, setQuery] = useState(searchParams.get("q") || "");

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search/similar?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <nav className="bg-white shadow-sm border-b fixed top-0 left-0 w-full">
    <div className="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row md:items-center md:h-16 space-y-3 md:space-y-0">
      <Link href="/">
        <div className="flex items-center">
          <TrendingUp className="h-8 w-8 text-blue-600" />
          <span className="text-xl font-semibold ps-2">
            Tech Trend Tracker
          </span>
        </div>
      </Link>
      <form onSubmit={handleSearch} className="flex-grow md:ml-8">
        <div className="relative">
          <MessageSquare className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about tech trends..."
            className="w-full pl-10 pr-4 py-2 rounded-lg border bg-gray-50 focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all"
          />
        </div>
      </form>
    </div>
    </nav>
  );
}

export default function Navbar() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <NavbarContent />
    </Suspense>
  );
}
