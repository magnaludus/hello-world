import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { protectedProcedure, router } from "../trpc";

const rifleInput = z.object({
  name: z.string().min(1).max(120),
  cartridge: z.string().min(1).max(120),
  barrelLengthIn: z.number().positive().nullable(),
  twistRate: z.string().max(40).nullable(),
  gasSystem: z.string().max(40).nullable(),
  roundCountBaseline: z.number().int().nonnegative().default(0),
});

type RifleRow = {
  id: string;
  user_id: string;
  name: string;
  cartridge: string;
  barrel_length_in: number | null;
  twist_rate: string | null;
  gas_system: string | null;
  round_count_baseline: number;
  created_at: string;
};

function toRifleInputRow(input: z.infer<typeof rifleInput>) {
  return {
    name: input.name,
    cartridge: input.cartridge,
    barrel_length_in: input.barrelLengthIn,
    twist_rate: input.twistRate,
    gas_system: input.gasSystem,
    round_count_baseline: input.roundCountBaseline,
  };
}

export const rifleRouter = router({
  list: protectedProcedure.query(async ({ ctx }) => {
    const { data, error } = await ctx.supabase
      .from("rifle")
      .select("*")
      .order("created_at", { ascending: false });
    if (error) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: error.message });
    return (data as RifleRow[]) ?? [];
  }),

  get: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ ctx, input }) => {
      const { data, error } = await ctx.supabase
        .from("rifle")
        .select("*")
        .eq("id", input.id)
        .single();
      if (error) throw new TRPCError({ code: "NOT_FOUND", message: error.message });
      return data as RifleRow;
    }),

  create: protectedProcedure.input(rifleInput).mutation(async ({ ctx, input }) => {
    const row = { ...toRifleInputRow(input), user_id: ctx.user.id };
    const { data, error } = await ctx.supabase.from("rifle").insert(row).select().single();
    if (error) throw new TRPCError({ code: "BAD_REQUEST", message: error.message });
    return data as RifleRow;
  }),

  update: protectedProcedure
    .input(rifleInput.extend({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => {
      const { id, ...rest } = input;
      const { data, error } = await ctx.supabase
        .from("rifle")
        .update(toRifleInputRow(rest))
        .eq("id", id)
        .select()
        .single();
      if (error) throw new TRPCError({ code: "BAD_REQUEST", message: error.message });
      return data as RifleRow;
    }),

  delete: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => {
      const { error } = await ctx.supabase.from("rifle").delete().eq("id", input.id);
      if (error) throw new TRPCError({ code: "BAD_REQUEST", message: error.message });
      return { ok: true as const };
    }),
});
