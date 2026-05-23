# Package Boundary

## Evidence Checked

- Published CSTP PDF: `/Users/dlev2617/Documents/Papers/~05-Published/Case Studies on Transport Policy/CSTP-Missed Opportunities/1-s2.0-S2213624X26001471-main.pdf`
- Paper source folder: `/Users/dlev2617/Documents/Papers/~05-Published/Case Studies on Transport Policy/CSTP-Missed Opportunities`
- Thesis-derived data/code folder: `/Users/dlev2617/Documents/U Sydney Academics/Theses - Honours and Masters/Undergraduate-Masters Theses 2024/Stuart Mills Eastern Suburbs Rail Thesis/Thesis Data Stuart Mills`

The paper states that the analysis uses R5Py with OpenStreetMap and GTFS, TfNSW travel zones and employment/population, NSW Valuer General land values, public cost benchmarks, and edited scenario networks.

## Release Boundary

The package includes authored notebooks and compact local data/results needed to understand and rerun much of the workflow. Raw public source portals should be cited for authoritative current copies. The no-shapes GTFS zips retain schedule, stop, route, trip, and stop-time tables but remove `shapes.txt`, which is the sole reason the original zips exceed normal GitHub file limits.

## Not Packaged

- Full thesis PDF: `/Users/dlev2617/Documents/U Sydney Academics/Theses - Honours and Masters/Undergraduate-Masters Theses 2024/Stuart Mills Eastern Suburbs Rail Thesis/Stuart_Mills_Eastern_Suburbs_Rail_Thesis.pdf`. It is 147 MB and is treated as local evidence, not a GitHub asset here.
- Original full scenario GTFS zips: kept as local source evidence and listed in `metadata/GTFS_TRANSFORMATION_MANIFEST.csv`.
- Manuscript drafts, journal correspondence, response letters, declarations, and figure-only duplicates.
- Raw public downloads that can be obtained from TfNSW, OSM, NSW Valuer General, Transit Costs Project, Sydney Metro/TfNSW, or other cited public sources.
