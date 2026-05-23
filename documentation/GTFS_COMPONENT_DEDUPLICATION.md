# GTFS Component Deduplication

Generated: 2026-05-23 10:59:33 AEST

The package previously contained per-scenario no-shapes GTFS zips. Direct inspection showed substantial repeated content inside those zips: agency, calendar, calendar_dates, levels, notes, pathways, routes, trips, stops, and several stop_times tables recur across scenarios.

- Scenario feeds componentized: `29`
- Unique GTFS member components retained: `59`
- Former no-shapes zip bytes removed: `1427622363`
- Component gzip bytes retained: `1127185001`
- Approximate package reduction from GTFS member deduplication: `300437362` bytes

The scenarios are not treated as identical. The manifest maps every scenario to its own combination of GTFS table components. Reconstruction is by table content, not by assumption from filenames.

Key files:

- `metadata/GTFS_COMPONENT_MANIFEST.csv`
- `metadata/GTFS_COMPONENT_SUMMARY.csv`
- `metadata/GTFS_SHAPES_DEDUP_MANIFEST.csv`
- `code/reconstruct_full_gtfs_with_shapes.py`
