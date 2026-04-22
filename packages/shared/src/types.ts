import { z } from "zod";

// Mirrors the Postgres enums / checks in Section 7.1

export const LoadDevMethod = z.enum([
  "satterlee",
  "ocw",
  "audette",
  "modified_audette",
  "seating_depth",
  "stat_velocity_ladder",
  "component_compare",
  "matrix",
]);
export type LoadDevMethod = z.infer<typeof LoadDevMethod>;

export const ComponentType = z.enum(["brass", "powder", "primer", "bullet"]);
export type ComponentType = z.infer<typeof ComponentType>;

export const ConfidenceTier = z.enum([
  "high",
  "moderate",
  "low",
  "insufficient",
]);
export type ConfidenceTier = z.infer<typeof ConfidenceTier>;

export const Rifle = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  name: z.string().min(1),
  cartridge: z.string().min(1),
  barrelLengthIn: z.number().positive().nullable(),
  twistRate: z.string().nullable(),
  gasSystem: z.string().nullable(),
  roundCountBaseline: z.number().int().nonnegative().default(0),
  createdAt: z.string().datetime(),
});
export type Rifle = z.infer<typeof Rifle>;

export const Component = z.object({
  id: z.string().uuid(),
  userId: z.string().uuid(),
  type: ComponentType,
  brand: z.string().min(1),
  model: z.string().nullable(),
  lotNumber: z.string().nullable(),
  weightGr: z.number().positive().nullable(),
  bcG1: z.number().positive().nullable(),
  bcG7: z.number().positive().nullable(),
  notes: z.string().nullable(),
});
export type Component = z.infer<typeof Component>;

export const ShotRecord = z.object({
  shotNumber: z.number().int().positive(),
  velocityFps: z.number().positive().nullable(),
  poiXIn: z.number().nullable(),
  poiYIn: z.number().nullable(),
  flagged: z.boolean().default(false),
  flagReason: z.string().nullable(),
  notes: z.string().nullable(),
});
export type ShotRecord = z.infer<typeof ShotRecord>;

export const Environment = z.object({
  tempF: z.number().nullable(),
  pressureInHg: z.number().nullable(),
  humidityPct: z.number().min(0).max(100).nullable(),
  densityAltitudeFt: z.number().nullable(),
});
export type Environment = z.infer<typeof Environment>;
