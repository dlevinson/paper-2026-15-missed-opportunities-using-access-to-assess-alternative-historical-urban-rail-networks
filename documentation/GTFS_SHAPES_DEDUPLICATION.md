# Deduplicated GTFS Shapes

The original scenario GTFS zips include very large `shapes.txt` files. Direct inspection found that most of those shape tables are identical:

- `a8fc638492806b0f`: 27 original GTFS zips
- `09a7e77e2f0eb394`: 1 original GTFS zips
- `1b7d735293f406c6`: 1 original GTFS zips

The package therefore stores:

- content-addressed no-shapes GTFS table components in `data/scenario_gtfs_components/`;
- split, gzipped `shapes.txt` components in `data/gtfs_shapes_deduplicated/`;
- `metadata/GTFS_SHAPES_DEDUP_MANIFEST.csv`, mapping each original zip to the correct shape component; and
- `code/reconstruct_full_gtfs_with_shapes.py`, which reconstructs full GTFS zips when needed.

This preserves the ability to rebuild full GTFS inputs without storing the same near-gigabyte shape table, or other repeated GTFS tables, inside every scenario archive.

This does not mean the scenarios are identical. Hash checks found distinct scenario encodings in other GTFS tables: `stop_times.txt` has 24 distinct hashes, `stops.txt` has 19, and `routes.txt`/`trips.txt` have 5 each. The shared `shapes.txt` table is a common geometric component for most scenarios; the scenario alternatives are primarily represented in schedule, stop, trip, and route tables.
