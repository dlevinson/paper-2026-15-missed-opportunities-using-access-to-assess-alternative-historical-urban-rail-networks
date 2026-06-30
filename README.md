# Missed Opportunities: Using Access to Assess Alternative Historical Urban Rail Networks

## Contribution

This paper introduces an accessibility-based, land-value appraisal of historical and proposed urban rail networks. Applying the method to a century of Sydney plans identifies overlooked alignments with strong potential benefits, while testing alternative costs and discount rates makes clear both the value and the limits of capitalized accessibility as a complement to conventional cost–benefit analysis.

Mills, S., & Levinson, D. M. (2026). Missed opportunities: Using access to assess alternative historical urban rail networks. Case Studies on Transport Policy, 25, 101851. https://doi.org/10.1016/j.cstp.2026.101851

## Package Status

This is a ready public package. The paper is open access under CC BY-NC 4.0. The staged research materials are thesis-derived analysis code, compact public-source inputs, scenario GTFS edits, and result tables/GIS files for the Sydney historical rail-network accessibility analysis.

## License

The operative root license is `LICENSE.md`. Author-created code and scripts
are licensed under MIT. Author-created derived data and documentation are
licensed under CC BY 4.0.

The published paper PDF in `paper/` remains under the article's original
CC BY-NC 4.0 terms. Public-source inputs and third-party assets retain their
original terms and are not relicensed here.

## Contents

- `paper/`: final published reference PDF.
- `code/notebooks_stripped/`: Jupyter notebooks with execution outputs removed.
- `code/notebooks_as_py/`: plain Python exports of the notebook code.
- `data/source_inputs/`: compact travel-zone, employment, population, and route-geometry inputs.
- `data/scenario_gtfs_components/`: content-addressed GTFS member components replacing duplicated no-shapes scenario zips.
- `data/gtfs_shapes_deduplicated/`: split, gzipped shared `shapes.txt` components for reconstructing full GTFS zips.
- `code/reconstruct_full_gtfs_with_shapes.py`: reconstruction tool for no-shapes and full GTFS zips.
- `data/results_and_gis/`: compact CSV, workbook, GeoPackage, QGIS project, and QGIS template outputs from the thesis-derived workflow.
- `metadata/`: file manifest, source decisions, notebook conversion manifest, GTFS transformation manifest, CSV dictionary, and workbook sheet inventory.

## Exclusions

Draft manuscripts, cover letters, response letters, journal forms, duplicate figure-only folders, notebook checkpoints, Java crash logs, PNG render outputs, the 147 MB honours thesis PDF, the full >100 MB GTFS zips with embedded duplicate `shapes.txt`, and the duplicated no-shapes GTFS zips are excluded from this GitHub-ready package; their GTFS tables and shapes are componentized, deduplicated, and reconstructable. The full source paths and original GTFS checksums are preserved in metadata for optional future Git LFS release.

Checked and staged: 2026-05-23 09:50:16



<!-- missed-opportunities-dedup-status:start -->
## Deduplication Status

Generated: 2026-05-23 10:59:33 AEST

- Scenario GTFS feeds represented as components: `29`
- Unique GTFS member components retained: `59`
- Former no-shapes zip bytes removed: `1427622363`
- Component gzip bytes retained: `1127185001`
- Exact duplicate non-GTFS bytes removed: `1376655`
- Reconstruction command example: `python3 code/reconstruct_full_gtfs_with_shapes.py --scenario 1974_v2.zip --output-dir reconstructed_full_gtfs`
<!-- missed-opportunities-dedup-status:end -->

<!-- package-hardening-status:start -->
## Package Hardening Status

Generated: 2026-05-23 11:12:11 AEST

- Pipeline: `UPLOADED`
- Sidecars added/updated: `PACKAGE_STATUS.md`, `PACKAGE_MANIFEST.csv`, `LICENSE_STATUS.md`.
- Public paper-package repositories include `paper/` PDF reference copies by owner decision; publisher takedown requests can be handled later if they arise.
- Final GitHub upload should use the manifest include statuses and the license-status note.
<!-- package-hardening-status:end -->
