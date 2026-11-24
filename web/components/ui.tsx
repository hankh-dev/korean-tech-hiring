import type { ReactNode } from "react";

export function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={`rounded-2xl border border-border bg-card shadow-[0_1px_2px_rgba(16,24,40,0.04)] ${className}`}
    >
      {children}
    </div>
  );
}

export function SectionTitle({
  title,
  desc,
  action,
}: {
  title: string;
  desc?: string;
  action?: ReactNode;
}) {
  return (
    <div className="mb-4 flex items-end justify-between gap-4">
      <div>
        <h2 className="text-lg font-bold tracking-tight">{title}</h2>
        {desc ? <p className="mt-1 text-sm text-muted">{desc}</p> : null}
      </div>
      {action}
    </div>
  );
}

const BADGE_TONES: Record<string, string> = {
  default: "bg-slate-100 text-slate-600",
  primary: "bg-primary-soft text-primary",
  ai: "bg-violet-100 text-violet-700",
  remote: "bg-emerald-100 text-emerald-700",
  hybrid: "bg-sky-100 text-sky-700",
  onsite: "bg-slate-100 text-slate-500",
  korean: "bg-rose-50 text-rose-600",
  global: "bg-indigo-50 text-indigo-600",
  up: "bg-emerald-50 text-emerald-600",
  down: "bg-rose-50 text-rose-600",
};

export function Badge({
  children,
  tone = "default",
}: {
  children: ReactNode;
  tone?: keyof typeof BADGE_TONES | string;
}) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-semibold ${
        BADGE_TONES[tone] ?? BADGE_TONES.default
      }`}
    >
      {children}
    </span>
  );
}

export function Bar({
  value,
  max,
  color = "bg-primary",
}: {
  value: number;
  max: number;
  color?: string;
}) {
  const width = max > 0 ? Math.max(2, Math.round((value / max) * 100)) : 0;
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
      <div className={`h-full rounded-full ${color}`} style={{ width: `${width}%` }} />
    </div>
  );
}

export function StatCard({
  label,
  value,
  unit,
  icon,
  hint,
}: {
  label: string;
  value: string;
  unit?: string;
  icon: ReactNode;
  hint?: string;
}) {
  return (
    <Card className="p-5">
      <div className="flex items-start justify-between">
        <p className="text-sm font-medium text-muted">{label}</p>
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary-soft text-primary">
          {icon}
        </span>
      </div>
      <p className="mt-3 text-3xl font-extrabold tracking-tight">
        {value}
        {unit ? <span className="ml-1 text-base font-semibold text-muted">{unit}</span> : null}
      </p>
      {hint ? <p className="mt-1 text-xs text-muted">{hint}</p> : null}
    </Card>
  );
}

export function EmptyState({ message }: { message: string }) {
  return (
    <Card className="p-10 text-center text-sm text-muted">{message}</Card>
  );
}

export function DeltaBadge({ delta }: { delta: number }) {
  if (delta > 0) return <Badge tone="up">▲ {delta}</Badge>;
  if (delta < 0) return <Badge tone="down">▼ {Math.abs(delta)}</Badge>;
  return <Badge>―</Badge>;
}
