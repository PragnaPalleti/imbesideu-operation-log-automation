# Data directory

Raw Dataset A/B archives are intentionally excluded from this public repository because they are large operational logs and may contain sensitive telemetry.

The pipeline accepts local directories containing the supplied ZIP archives:

```bash
python scripts/run_pipeline.py --dataset-a /path/to/dataset_a --dataset-b /path/to/dataset_b --out outputs
```

Derived, non-raw outputs used for review are committed under `outputs/`.