import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Phase 1 scaffold. Session flow lands in Phase 2 (PRD §13).
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <Link href="/rifles">
          <Card className="hover:bg-accent/30 transition-colors">
            <CardHeader>
              <CardTitle>Rifles</CardTitle>
              <CardDescription>Manage the rifles you develop loads for.</CardDescription>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Name, cartridge, barrel length, twist, round-count baseline.
            </CardContent>
          </Card>
        </Link>
        <Link href="/components">
          <Card className="hover:bg-accent/30 transition-colors">
            <CardHeader>
              <CardTitle>Components</CardTitle>
              <CardDescription>Brass, powder, primers, bullets with lot numbers.</CardDescription>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              Every session references these. Lot-to-lot comparisons live in Phase 4.
            </CardContent>
          </Card>
        </Link>
      </div>
    </div>
  );
}
