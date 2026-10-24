# GIS Production Workflow Examples

These **additive** examples supplement the existing `templates/` and installed skills. All datasets under `fixtures/` are invented solely for deterministic tests, not real measurements.

| Workflow | Entry | Dependencies | Status |
| --- | --- | --- | --- |
| Network line duplicates / endpoint dangles | [Network README](network-topology/README.md) | Python 3.11+ standard library | Offline synthetic test (T1); not full topology |
| Hourly weather response → GeoJSON | [API README](api-ingestion/README.md) | Python 3.11+ standard library | Offline fixture test (T1); live API untested |
| Multiple layout PDFs | [ArcGIS Pro README](batch-export/README.md) | ArcGIS Pro/ArcPy | Source only; native execution not verified |
| Spatial index and SQL | [PostGIS SQL](spatial-sql/postgis_network_index.sql) | PostgreSQL/PostGIS | Sandbox illustration, not executed |
| Satellite STAC/COG processing | [Workflow checklist](remote-sensing/STAC_COG_WORKFLOW.md) | Depends on source | Documentation only |

See [quality benchmark](../docs/QUALITY_BENCHMARK.md). All commands should write to **new output locations** and never silently modify input datasets.
