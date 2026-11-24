import type { WeeklyRow } from "@/lib/data";

export function WeeklyBars({ weeks }: { weeks: WeeklyRow[] }) {
  const max = Math.max(1, ...weeks.map((w) => w.jobs));
  const W = 640;
  const H = 180;
  const pad = 8;
  const gap = 10;
  const barW = (W - pad * 2 - gap * (weeks.length - 1)) / weeks.length;

  return (
    <div>
      <svg viewBox={`0 0 ${W} ${H + 34}`} className="w-full" role="img" aria-label="주간 신규 공고 추이">
        {weeks.map((w, i) => {
          const h = Math.max(3, Math.round((w.jobs / max) * (H - 24)));
          const x = pad + i * (barW + gap);
          const y = H - h;
          return (
            <g key={w.week}>
              <rect
                x={x}
                y={y}
                width={barW}
                height={h}
                rx={6}
                className={w.partial ? "fill-slate-300" : "fill-primary"}
              />
              <text
                x={x + barW / 2}
                y={y - 6}
                textAnchor="middle"
                className="fill-slate-500 text-[11px] font-semibold"
              >
                {w.jobs}
              </text>
              <text
                x={x + barW / 2}
                y={H + 16}
                textAnchor="middle"
                className="fill-slate-400 text-[10px]"
              >
                {w.start.slice(5).replace("-", "/")}
              </text>
              {w.partial ? (
                <text
                  x={x + barW / 2}
                  y={H + 30}
                  textAnchor="middle"
                  className="fill-slate-400 text-[9px]"
                >
                  진행중
                </text>
              ) : null}
            </g>
          );
        })}
      </svg>
      <p className="mt-1 text-xs text-muted">
        막대는 해당 주에 게시된 신규 개발 공고 수입니다. 회색 막대는 아직 끝나지 않은 이번 주입니다.
      </p>
    </div>
  );
}

export function DailySpark({ days }: { days: { date: string; jobs: number }[] }) {
  const max = Math.max(1, ...days.map((d) => d.jobs));
  const W = 640;
  const H = 64;
  const gap = 3;
  const barW = (W - gap * (days.length - 1)) / days.length;
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="최근 30일 일별 신규 공고">
      {days.map((d, i) => {
        const h = Math.max(2, Math.round((d.jobs / max) * (H - 4)));
        return (
          <rect
            key={d.date}
            x={i * (barW + gap)}
            y={H - h}
            width={barW}
            height={h}
            rx={2}
            className="fill-accent/70"
          />
        );
      })}
    </svg>
  );
}
