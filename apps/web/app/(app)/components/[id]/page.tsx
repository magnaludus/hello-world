"use client";

import { notFound, useParams } from "next/navigation";
import { trpc } from "@/lib/trpc/client";
import { ComponentForm } from "../component-form";

export default function EditComponentPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { data, isLoading, error } = trpc.component.get.useQuery({ id }, { enabled: Boolean(id) });

  if (error?.data?.code === "NOT_FOUND") notFound();
  if (isLoading || !data) {
    return <p className="text-sm text-muted-foreground">Loading…</p>;
  }

  return (
    <ComponentForm
      defaults={{
        id: data.id,
        type: data.type,
        brand: data.brand,
        model: data.model ?? "",
        lotNumber: data.lot_number ?? "",
        weightGr: data.weight_gr?.toString() ?? "",
        bcG1: data.bc_g1?.toString() ?? "",
        bcG7: data.bc_g7?.toString() ?? "",
        notes: data.notes ?? "",
      }}
    />
  );
}
