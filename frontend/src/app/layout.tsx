import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Valuer – Kenya Real Estate Analytics",
  description:
    "AI-powered property valuations and market analytics for the Kenyan real estate market.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="flex min-h-full flex-col bg-gray-50 dark:bg-gray-950">
        {/* ── Nav ── */}
        <header className="border-b border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
            <Link
              href="/"
              className="flex items-center gap-2 text-lg font-bold text-emerald-700 dark:text-emerald-400"
            >
              🏠 Smart Valuer
            </Link>
            <nav className="flex items-center gap-6 text-sm font-medium">
              <Link
                href="/"
                className="text-gray-600 transition hover:text-emerald-600 dark:text-gray-300"
              >
                Home
              </Link>
              <Link
                href="/dashboard"
                className="text-gray-600 transition hover:text-emerald-600 dark:text-gray-300"
              >
                Dashboard
              </Link>
            </nav>
          </div>
        </header>

        {/* ── Page content ── */}
        <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-8 sm:px-6">
          {children}
        </main>

        {/* ── Footer ── */}
        <footer className="border-t border-gray-200 bg-white py-4 text-center text-xs text-gray-400 dark:border-gray-700 dark:bg-gray-900">
          © {new Date().getFullYear()} Smart Valuer · Kenya Real Estate Analytics
        </footer>
      </body>
    </html>
  );
}
