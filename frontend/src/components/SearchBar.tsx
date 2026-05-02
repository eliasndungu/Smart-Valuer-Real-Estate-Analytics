"use client";

import { useState } from "react";
import { Search } from "lucide-react";

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

export default function SearchBar({
  onSearch,
  placeholder = "Search by neighbourhood, county or property type…",
}: SearchBarProps) {
  const [query, setQuery] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSearch(query.trim());
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-2 w-full max-w-2xl"
      role="search"
    >
      <div className="relative flex-1">
        <Search
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
          size={18}
          aria-hidden="true"
        />
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          aria-label="Search properties"
          className="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-10 pr-4 text-sm
                     shadow-sm outline-none transition focus:border-emerald-500 focus:ring-2
                     focus:ring-emerald-200 dark:border-gray-600 dark:bg-gray-800 dark:text-white"
        />
      </div>
      <button
        type="submit"
        className="rounded-lg bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white
                   shadow-sm transition hover:bg-emerald-700 focus:outline-none
                   focus:ring-2 focus:ring-emerald-400"
      >
        Search
      </button>
    </form>
  );
}
