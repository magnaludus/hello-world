# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Status

This repository currently contains only a `README.md`. There is no source code, build system, test suite, package manifest, or CI configuration yet. Treat any new work as bootstrapping: choose conventions deliberately and update this file when they are established.

## When Adding Code

Before introducing tooling, confirm with the user what stack is intended (the repo name `hello-world` does not imply a language). Once a stack is chosen, record in this file:

- Build / run / lint / test commands (including how to run a single test)
- Project layout and any non-obvious architectural decisions
- Any required environment variables or external services

## Branching

The active development branch for Claude-driven work is `claude/add-claude-documentation-9hOON`. The default branch is `master`. Do not push to `master` without explicit user approval.
