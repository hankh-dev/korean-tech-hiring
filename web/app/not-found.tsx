import Link from "next/link";
import { Card } from "@/components/ui";

export default function NotFound() {
  return (
    <div className="flex min-h-[50vh] items-center justify-center">
      <Card className="max-w-md p-10 text-center">
        <p className="text-5xl font-extrabold text-primary">404</p>
        <h1 className="mt-3 text-lg font-bold">페이지를 찾을 수 없습니다</h1>
        <p className="mt-2 text-sm text-muted">
          주소가 바뀌었거나 삭제된 페이지입니다. 아래에서 원하는 데이터를 찾아보세요.
        </p>
        <div className="mt-6 flex justify-center gap-2">
          <Link href="/" className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-primary/90">대시보드</Link>
          <Link href="/jobs" className="rounded-lg border border-border px-4 py-2 text-sm font-semibold hover:bg-slate-50">공고 목록</Link>
        </div>
      </Card>
    </div>
  );
}
