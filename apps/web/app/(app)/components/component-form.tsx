"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";
import type { ComponentType } from "@loadlab/shared";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { trpc } from "@/lib/trpc/client";

type FormState = {
  type: ComponentType;
  brand: string;
  model: string;
  lotNumber: string;
  weightGr: string;
  bcG1: string;
  bcG7: string;
  notes: string;
};

export type ComponentDefaults = Partial<FormState> & { id?: string };

const empty: FormState = {
  type: "powder",
  brand: "",
  model: "",
  lotNumber: "",
  weightGr: "",
  bcG1: "",
  bcG7: "",
  notes: "",
};

function parseOptionalNumber(s: string): number | null {
  if (s.trim() === "") return null;
  const n = Number(s);
  return Number.isFinite(n) && n > 0 ? n : null;
}

function optStr(s: string): string | null {
  const t = s.trim();
  return t === "" ? null : t;
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
        if (confirm("Delete this component?")) {
          onDelete(id);
        }
      }}
    >
      Delete
    </Button>
  );
}

export function ComponentForm({ defaults }: { defaults?: ComponentDefaults }) {
  const router = useRouter();
  const utils = trpc.useUtils();
  const [state, setState] = useState<FormState>({ ...empty, ...defaults });
  const isEdit = Boolean(defaults?.id);

  const createMut = trpc.component.create.useMutation({
    onSuccess: async () => {
      toast.success("Component created");
      await utils.component.list.invalidate();
      router.push("/components");
    },
    onError: (e) => toast.error(e.message),
  });
  const updateMut = trpc.component.update.useMutation({
    onSuccess: async () => {
      toast.success("Component updated");
      await utils.component.list.invalidate();
      router.push("/components");
    },
    onError: (e) => toast.error(e.message),
  });
  const deleteMut = trpc.component.delete.useMutation({
    onSuccess: async () => {
      toast.success("Component deleted");
      await utils.component.list.invalidate();
      router.push("/components");
    },
    onError: (e) => toast.error(e.message),
  });

  function onChange<K extends keyof FormState>(key: K, value: FormState[K]) {
    setState((s) => ({ ...s, [key]: value }));
  }

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const payload = {
      type: state.type,
      brand: state.brand.trim(),
      model: optStr(state.model),
      lotNumber: optStr(state.lotNumber),
      weightGr: parseOptionalNumber(state.weightGr),
      bcG1: parseOptionalNumber(state.bcG1),
      bcG7: parseOptionalNumber(state.bcG7),
      notes: optStr(state.notes),
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
        <CardTitle>{isEdit ? "Edit component" : "New component"}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="type">Type</Label>
              <Select
                value={state.type}
                onValueChange={(v) => onChange("type", v as ComponentType)}
              >
                <SelectTrigger id="type">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="brass">Brass</SelectItem>
                  <SelectItem value="powder">Powder</SelectItem>
                  <SelectItem value="primer">Primer</SelectItem>
                  <SelectItem value="bullet">Bullet</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="brand">Brand</Label>
              <Input
                id="brand"
                required
                value={state.brand}
                onChange={(e) => onChange("brand", e.target.value)}
                placeholder="e.g. Hodgdon"
              />
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="model">Model</Label>
              <Input
                id="model"
                value={state.model}
                onChange={(e) => onChange("model", e.target.value)}
                placeholder="e.g. H4350"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="lot">Lot number</Label>
              <Input
                id="lot"
                value={state.lotNumber}
                onChange={(e) => onChange("lotNumber", e.target.value)}
              />
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="wg">Weight (gr)</Label>
              <Input
                id="wg"
                inputMode="decimal"
                value={state.weightGr}
                onChange={(e) => onChange("weightGr", e.target.value)}
                placeholder="bullet only"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="bcg1">BC (G1)</Label>
              <Input
                id="bcg1"
                inputMode="decimal"
                value={state.bcG1}
                onChange={(e) => onChange("bcG1", e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="bcg7">BC (G7)</Label>
              <Input
                id="bcg7"
                inputMode="decimal"
                value={state.bcG7}
                onChange={(e) => onChange("bcG7", e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
            <Input
              id="notes"
              value={state.notes}
              onChange={(e) => onChange("notes", e.target.value)}
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <div className="flex gap-2">
              <Button type="submit" disabled={busy}>
                {busy ? "Saving..." : isEdit ? "Save changes" : "Create component"}
              </Button>
              <Button
                type="button"
                variant="ghost"
                disabled={busy}
                onClick={() => router.push("/components")}
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
