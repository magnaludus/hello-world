"use client";

import { notFound, useParams } from "next/navigation";
import { trpc } from "@/lib/trpc/client";
import { RifleForm } from "../rifle-form";

export default function EditRiflePage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const { data, isLoading, error } = trpc.rifle.get.useQuery({ id }, { enabled: Boolean(id) });

  if (error?.data?.code === "NOT_FOUND") notFound();
  if (isLoading || !data) {
    return <p className="text-sm text-muted-foreground">Loading…</p>;
  }

  return (
    <RifleForm
      defaults={{
        id: data.id,
        name: data.name,
        cartridge: data.cartridge,
        barrelLengthIn: data.barrel_length_in?.toString() ?? "",
        twistRate: data.twist_rate ?? "",
        gasSystem: data.gas_system ?? "",
        roundCountBaseline: data.round_count_baseline.toString(),
      }}
    />
  );
}
