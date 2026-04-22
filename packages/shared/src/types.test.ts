import { describe, expect, it } from "vitest";
import { ComponentType, LoadDevMethod } from "./types";

describe("LoadDevMethod enum", () => {
  it("accepts every method named in PRD §5", () => {
    const methods = [
      "satterlee",
      "ocw",
      "audette",
      "modified_audette",
      "seating_depth",
      "stat_velocity_ladder",
      "component_compare",
      "matrix",
    ] as const;
    for (const m of methods) {
      expect(() => LoadDevMethod.parse(m)).not.toThrow();
    }
  });

  it("rejects unknown methods", () => {
    expect(() => LoadDevMethod.parse("flat-spot")).toThrow();
  });
});

describe("ComponentType enum", () => {
  it("matches the Postgres check constraint", () => {
    for (const t of ["brass", "powder", "primer", "bullet"] as const) {
      expect(() => ComponentType.parse(t)).not.toThrow();
    }
  });
});
