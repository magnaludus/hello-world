import { defineWorkspace } from "vitest/config";

export default defineWorkspace([
  "apps/web/vitest.config.ts",
  "packages/shared/vitest.config.ts",
  "packages/chrono-parsers/vitest.config.ts",
  "packages/db/vitest.config.ts",
]);
