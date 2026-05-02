"use client";

import Link from "next/link";
import PredictionForm from "@/components/PredictionForm";
import SearchBar from "@/components/SearchBar";

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* ── Hero ── */}
      <section className="rounded-3xl bg-gradient-to-br from-emerald-600 to-teal-700 px-8 py-14 text-center text-white shadow-lg">
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl">
          Kenya Real Estate Analytics
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-lg text-emerald-100">
          Discover fair property values, explore neighbourhood trends, and make
          data-driven real estate decisions — all powered by scraped Kenyan
          listing data.
        </p>

        {/* Search */}
        <div className="mt-8 flex justify-center">
          <SearchBar
            onSearch={(q) => {
              console.log("Search:", q);
            }}
          />
        </div>

        <div className="mt-6 flex flex-wrap justify-center gap-4">
          <Link
            href="/dashboard"
            className="rounded-lg bg-white px-6 py-3 text-sm font-semibold text-emerald-700
                       shadow transition hover:bg-emerald-50"
          >
            View Dashboard →
          </Link>
          <a
            href="#estimator"
            className="rounded-lg border border-white/50 px-6 py-3 text-sm font-semibold
                       text-white transition hover:bg-white/10"
          >
            Estimate Price
          </a>
        </div>
      </section>

      {/* ── Feature cards ── */}
      <section className="grid gap-6 sm:grid-cols-3">
        {[
          {
            emoji: "🕷️",
            title: "Live Data Scraping",
            desc: "Scrapy spiders crawl BuyRentKenya and Jiji daily to keep property data fresh.",
          },
          {
            emoji: "📊",
            title: "Market Analytics",
            desc: "Interactive charts show average prices by bedroom count and neighbourhood trends.",
          },
          {
            emoji: "🤖",
            title: "AI Valuations",
            desc: "FastAPI + Scikit-learn model estimates property value from your inputs in seconds.",
          },
        ].map((f) => (
          <div
            key={f.title}
            className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm
                       dark:border-gray-700 dark:bg-gray-900"
          >
            <span className="text-3xl">{f.emoji}</span>
            <h3 className="mt-3 font-semibold text-gray-900 dark:text-white">{f.title}</h3>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">{f.desc}</p>
          </div>
        ))}
      </section>

      {/* ── Price estimator ── */}
      <section id="estimator" className="scroll-mt-20">
        <h2 className="mb-6 text-2xl font-bold text-gray-900 dark:text-white">
          Instant Price Estimate
        </h2>
        <div className="mx-auto max-w-2xl">
          <PredictionForm />
        </div>
      </section>
    </div>
  );
}
