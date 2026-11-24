"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3 } from "lucide-react";

const LINKS = [
  { href: "/", label: "대시보드" },
  { href: "/stacks", label: "스택" },
  { href: "/roles", label: "직군" },
  { href: "/companies", label: "기업" },
  { href: "/jobs", label: "공고" },
  { href: "/reports", label: "리포트" },
  { href: "/about", label: "소개" },
];

export function Nav() {
  const pathname = usePathname();
  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-card/90 backdrop-blur">
      <div className="mx-auto flex h-14 max-w-6xl items-center gap-4 px-4">
        <Link href="/" className="flex items-center gap-2 font-extrabold tracking-tight">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-white">
            <BarChart3 className="h-4 w-4" />
          </span>
          <span className="hidden sm:inline">개발자 채용 데이터랩</span>
          <span className="sm:hidden">채용 데이터랩</span>
        </Link>
        <nav className="ml-auto flex items-center gap-1 overflow-x-auto">
          {LINKS.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className={`whitespace-nowrap rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
                isActive(l.href)
                  ? "bg-primary-soft text-primary"
                  : "text-muted hover:bg-slate-100 hover:text-foreground"
              }`}
            >
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
