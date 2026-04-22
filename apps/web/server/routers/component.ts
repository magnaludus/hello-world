import { TRPCError } from "@trpc/server";
import { ComponentType } from "@loadlab/shared";
import { z } from "zod";
import { protectedProcedure, router } from "../trpc";

const componentInput = z.object({
  type: ComponentType,
  brand: z.string().min(1).max(120),
  model: z.string().max(120).nullable(),
  lotNumber: z.string().max(120).nullable(),
  weightGr: z.number().positive().nullable(),
  bcG1: z.number().positive().nullable(),
  bcG7: z.number().positive().nullable(),
  notes: z.string().max(2000).nullable(),
});

type ComponentRow = {
  id: string;
  user_id: string;
  type: ComponentType;
  brand: string;
  model: string | null;
  lot_number: string | null;
  weight_gr: number | null;
  bc_g1: number | null;
  bc_g7: number | null;
  notes: string | null;
};

function toInputRow(input: z.infer<typeof componentInput>) {
  return {
    type: input.type,
    brand: input.brand,
    model: input.model,
    lot_number: input.lotNumber,
    weight_gr: input.weightGr,
    bc_g1: input.bcG1,
    bc_g7: input.bcG7,
    notes: input.notes,
  };
}

export const componentRouter = router({
  list: protectedProcedure
    .input(z.object({ type: ComponentType.optional() }).optional())
    .query(async ({ ctx, input }) => {
      let query = ctx.supabase.from("component").select("*").order("brand", { ascending: true });
      if (input?.type) query = query.eq("type", input.type);
      const { data, error } = await query;
      if (error) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: error.message });
      return (data as ComponentRow[]) ?? [];
    }),

  get: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ ctx, input }) => {
      const { data, error } = await ctx.supabase
        .from("component")
        .select("*")
        .eq("id", input.id)
        .single();
      if (error) throw new TRPCError({ code: "NOT_FOUND", message: error.message });
      return data as ComponentRow;
    }),

  create: protectedProcedure.input(componentInput).mutation(async ({ ctx, input }) => {
    const row = { ...toInputRow(input), user_id: ctx.user.id };
    const { data, error } = await ctx.supabase.from("component").insert(row).select().single();
    if (error) throw new TRPCError({ code: "BAD_REQUEST", message: error.message });
    return data as ComponentRow;
  }),

  update: protectedProcedure
    .input(componentInput.extend({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => {
      const { id, ...rest } = input;
      const { data, error } = await ctx.supabase
        .from("component")
        .update(toInputRow(rest))
        .eq("id", id)
        .select()
        .single();
      if (error) throw new TRPCError({ code: "BAD_REQUEST", message: error.message });
      return data as ComponentRow;
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => {
      const { error } = await ctx.supabase.from("component").delete().eq("id", input.id);
      if (error) throw new TRPCError({ code: "BAD_REQUEST", message: error.message });
      return { ok: true as const };
    }),
});
