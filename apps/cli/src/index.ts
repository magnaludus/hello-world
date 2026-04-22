#!/usr/bin/env node
import { Command } from "commander";

const program = new Command();

program
  .name("loadlab")
  .description("LoadLab CLI - batch import, analyze, export, power analysis")
  .version("0.1.0");

program
  .command("power")
  .description("Compute sample size for a given effect size (stub)")
  .option("--sd <number>", "estimated standard deviation")
  .option("--delta <number>", "minimum detectable effect size")
  .option("--alpha <number>", "significance level", "0.05")
  .option("--power <number>", "desired power", "0.8")
  .action(() => {
    console.error("Not yet implemented. See PRD §6.6 and Phase 3.");
    process.exit(1);
  });

program
  .command("import")
  .description("Bulk import chronograph data (stub)")
  .argument("<vendor>", "garmin | labradar | magnetospeed")
  .argument("<csv>", "path to CSV file")
  .action(() => {
    console.error("Not yet implemented. See PRD §10 and Phase 6.");
    process.exit(1);
  });

program
  .command("analyze")
  .description("Run analysis on a session (stub)")
  .argument("<session-id>", "LoadLab session id")
  .action(() => {
    console.error("Not yet implemented. See Phase 8.");
    process.exit(1);
  });

program.parse();
