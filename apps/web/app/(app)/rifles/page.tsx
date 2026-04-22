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

export default function RiflesPage() {
  const { data, isLoading, error } = trpc.rifle.list.useQuery();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Rifles</h1>
          <p className="text-sm text-muted-foreground">
            Every session is attached to a rifle.
          </p>
        </div>
        <Button asChild>
          <Link href="/rifles/new">New rifle</Link>
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
              <TableHead>Name</TableHead>
              <TableHead>Cartridge</TableHead>
              <TableHead>Barrel</TableHead>
              <TableHead>Twist</TableHead>
              <TableHead>Round count</TableHead>
              <TableHead className="text-right">Edit</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((r) => (
              <TableRow key={r.id}>
                <TableCell className="font-medium">{r.name}</TableCell>
                <TableCell>{r.cartridge}</TableCell>
                <TableCell>{r.barrel_length_in ? `${r.barrel_length_in}"` : "—"}</TableCell>
                <TableCell>{r.twist_rate ?? "—"}</TableCell>
                <TableCell>{r.round_count_baseline}</TableCell>
                <TableCell className="text-right">
                  <Button asChild variant="ghost" size="sm">
                    <Link href={`/rifles/${r.id}`}>Edit</Link>
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      ) : (
        <p className="text-sm text-muted-foreground">No rifles yet. Add one to get started.</p>
      )}
    </div>
  );
}
