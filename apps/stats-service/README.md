# @loadlab/stats-service

Python FastAPI statistics engine. See PRD Section 6 for the statistical foundation that drives the module layout below.

## Layout

```
src/loadlab_stats/
  methods/      One module per load dev method (Section 5)
  detection/    Node detection algorithms (6.4, 6.5, 6.8)
  power/        Sample size and power analysis (6.6)
  bayesian/     Posterior updating, SD confidence intervals (6.1, 6.7)
  validation/   Monte Carlo harness (6.9)
  api.py        FastAPI entrypoint
```

## Local development

```bash
cd apps/stats-service
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pnpm dev                      # uvicorn with reload on :8000
```

## Acceptance criteria (PRD Phase 3)

All algorithms validated against reference implementations (SciPy, statsmodels) to 1e-9. See `tests/` and `src/loadlab_stats/validation/monte_carlo.py`.
