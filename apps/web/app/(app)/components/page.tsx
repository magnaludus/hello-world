"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { trpc } from "@/lib/trpc/client";

export default function ComponentsPage() {
  const { data, isLoading, error } = trpc.component.list.useQuery();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Components</h1>
          <p className="text-sm text-muted-foreground">
            Brass, powder, primers, bullets. Lot numbers matter.
          </p>
        </div>
        <Button asChild>
          <Link href="/components/new">New component</Link>
        </Button>
      </div>

      {error && (
        <p className="text-sm text-destructive">Failed to load: {error.message}</p>
      )}

      {isLoading ? (
        <p className="text-sm text-muted-foreground">Loading…</p>
      ) : data && data.length > 0 ? (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Type</TableHead>
              <TableHead>Brand</TableHead>
              <TableHead>Model</TableHead>
              <TableHead>Lot</TableHead>
              <TableHead>Weight (gr)</TableHead>
              <TableHead className="text-right">Edit</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((c) => (
              <TableRow key={c.id}>
                <TableCell className="capitalize">{c.type}</TableCell>
                <TableCell className="font-medium">{c.brand}</TableCell>
                <TableCell>{c.model ?? "—"}</TableCell>
                <TableCell>{c.lot_number ?? "—"}</TableCell>
                <TableCell>{c.weight_gr ?? "—"}</TableCell>
                <TableCell className="text-right">
                  <Button asChild variant="ghost" size="sm">
                    <Link href={`/components/${c.id}`}>Edit</Link>
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      ) : (
        <p className="text-sm text-muted-foreground">
          No components yet. Add powder, primers, brass, bullets.
        </p>
      )}
    </div>
  );
}
