"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { trpc } from "@/lib/trpc/client";

type FormState = {
  name: string;
  cartridge: string;
  barrelLengthIn: string;
  twistRate: string;
  gasSystem: string;
  roundCountBaseline: string;
};

export type RifleDefaults = Partial<FormState> & { id?: string };

const empty: FormState = {
  name: "",
  cartridge: "",
  barrelLengthIn: "",
  twistRate: "",
  gasSystem: "",
  roundCountBaseline: "0",
};

function parseOptionalNumber(s: string): number | null {
  if (s.trim() === "") return null;
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

function DeleteButton({
  id,
  busy,
  onDelete,
}: {
  id: string;
  busy: boolean;
  onDelete: (id: string) => void;
}) {
  return (
    <Button
      type="button"
      variant="destructive"
      disabled={busy}
      onClick={() => {
        if (confirm("Delete this rifle? Sessions referencing it will be blocked.")) {
          onDelete(id);
        }
      }}
    >
      Delete
    </Button>
  );
}

export function RifleForm({ defaults }: { defaults?: RifleDefaults }) {
  const router = useRouter();
  const utils = trpc.useUtils();
  const [state, setState] = useState<FormState>({ ...empty, ...defaults });
  const isEdit = Boolean(defaults?.id);

  const createMut = trpc.rifle.create.useMutation({
    onSuccess: async () => {
      toast.success("Rifle created");
      await utils.rifle.list.invalidate();
      router.push("/rifles");
    },
    onError: (e) => toast.error(e.message),
  });
  const updateMut = trpc.rifle.update.useMutation({
    onSuccess: async () => {
      toast.success("Rifle updated");
      await utils.rifle.list.invalidate();
      router.push("/rifles");
    },
    onError: (e) => toast.error(e.message),
  });
  const deleteMut = trpc.rifle.delete.useMutation({
    onSuccess: async () => {
      toast.success("Rifle deleted");
      await utils.rifle.list.invalidate();
      router.push("/rifles");
    },
    onError: (e) => toast.error(e.message),
  });

  function onChange<K extends keyof FormState>(key: K, value: FormState[K]) {
    setState((s) => ({ ...s, [key]: value }));
  }

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const payload = {
      name: state.name.trim(),
      cartridge: state.cartridge.trim(),
      barrelLengthIn: parseOptionalNumber(state.barrelLengthIn),
      twistRate: state.twistRate.trim() === "" ? null : state.twistRate.trim(),
      gasSystem: state.gasSystem.trim() === "" ? null : state.gasSystem.trim(),
      roundCountBaseline: Math.max(0, Math.floor(Number(state.roundCountBaseline) || 0)),
    };
    if (isEdit && defaults?.id) {
      updateMut.mutate({ id: defaults.id, ...payload });
    } else {
      createMut.mutate(payload);
    }
  }

  const busy = createMut.isPending || updateMut.isPending || deleteMut.isPending;

  return (
    <Card className="max-w-2xl">
      <CardHeader>
        <CardTitle>{isEdit ? "Edit rifle" : "New rifle"}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              required
              value={state.name}
              onChange={(e) => onChange("name", e.target.value)}
              placeholder="e.g. Tikka T3x 6 Creedmoor"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="cartridge">Cartridge</Label>
            <Input
              id="cartridge"
              required
              value={state.cartridge}
              onChange={(e) => onChange("cartridge", e.target.value)}
              placeholder="e.g. 6 Creedmoor"
            />
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="barrel">Barrel length (in)</Label>
              <Input
                id="barrel"
                inputMode="decimal"
                value={state.barrelLengthIn}
                onChange={(e) => onChange("barrelLengthIn", e.target.value)}
                placeholder="26"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="twist">Twist rate</Label>
              <Input
                id="twist"
                value={state.twistRate}
                onChange={(e) => onChange("twistRate", e.target.value)}
                placeholder="1:7.5"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="gas">Gas system</Label>
              <Input
                id="gas"
                value={state.gasSystem}
                onChange={(e) => onChange("gasSystem", e.target.value)}
                placeholder="bolt / rifle-length / ..."
              />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="rc">Round count baseline</Label>
            <Input
              id="rc"
              type="number"
              min="0"
              value={state.roundCountBaseline}
              onChange={(e) => onChange("roundCountBaseline", e.target.value)}
            />
          </div>
          <div className="flex items-center justify-between pt-2">
            <div className="flex gap-2">
              <Button type="submit" disabled={busy}>
                {busy ? "Saving..." : isEdit ? "Save changes" : "Create rifle"}
              </Button>
              <Button
                type="button"
                variant="ghost"
                disabled={busy}
                onClick={() => router.push("/rifles")}
              >
                Cancel
              </Button>
            </div>
            {isEdit && defaults?.id ? (
              <DeleteButton
                id={defaults.id}
                busy={busy}
                onDelete={(id) => deleteMut.mutate({ id })}
              />
            ) : null}
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
