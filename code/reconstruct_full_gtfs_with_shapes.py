#!/usr/bin/env python3
"""Reconstruct Missed Opportunities scenario GTFS zips from deduplicated components.

Run from the package root. By default the script reconstructs full scenario
GTFS zips by combining member components and the deduplicated shapes.txt table.
Use --no-shapes-only to rebuild the intermediate no-shapes zips.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import shutil
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def scenario_key(value: str) -> str:
    name = Path(value).name
    if name.endswith("_no_shapes.zip"):
        return name.replace("_no_shapes.zip", ".zip")
    if name.endswith(".zip"):
        return name
    return f"{name}.zip"


def assemble_gzip(package_root: Path, parts: str, tmp_dir: Path, label: str) -> Path:
    out = tmp_dir / f"{label}.gz"
    with out.open("wb") as dest:
        for rel in [part.strip() for part in parts.split(";") if part.strip()]:
            with (package_root / rel).open("rb") as src:
                shutil.copyfileobj(src, dest, length=1024 * 1024)
    return out


def write_member_from_component(package_root: Path, row: dict[str, str], zout: zipfile.ZipFile, tmp_dir: Path) -> None:
    label = row["component_group"] + "_" + Path(row["member_path"]).name
    gz_path = assemble_gzip(package_root, row["component_parts"], tmp_dir, label)
    with gzip.open(gz_path, "rb") as source, zout.open(row["member_path"], "w", force_zip64=True) as dest:
        shutil.copyfileobj(source, dest, length=1024 * 1024)


def build_no_shapes(package_root: Path, scenario: str, output_zip: Path, tmp_dir: Path) -> None:
    rows = read_csv(package_root / "metadata/GTFS_COMPONENT_MANIFEST.csv")
    wanted = scenario_key(scenario)
    selected = [row for row in rows if row["scenario_original_zip"] == wanted]
    if not selected:
        raise SystemExit(f"No component rows found for scenario {scenario!r}")
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for row in sorted(selected, key=lambda item: item["member_path"]):
            write_member_from_component(package_root, row, zout, tmp_dir)


def shape_row_for(package_root: Path, scenario: str) -> dict[str, str] | None:
    wanted = scenario_key(scenario)
    for row in read_csv(package_root / "metadata/GTFS_SHAPES_DEDUP_MANIFEST.csv"):
        if Path(row["source_zip"]).name == wanted and row.get("dedup_component_parts"):
            return row
    return None


def add_shapes(package_root: Path, no_shapes_zip: Path, scenario: str, output_zip: Path, tmp_dir: Path) -> None:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    row = shape_row_for(package_root, scenario)
    if not row:
        shutil.copy2(no_shapes_zip, output_zip)
        return
    shapes_gz = assemble_gzip(package_root, row["dedup_component_parts"], tmp_dir, "shapes")
    with zipfile.ZipFile(no_shapes_zip) as zin, zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for info in zin.infolist():
            if Path(info.filename).name.lower() == "shapes.txt":
                continue
            zout.writestr(info.filename, zin.read(info.filename))
        with gzip.open(shapes_gz, "rb") as source, zout.open("shapes.txt", "w", force_zip64=True) as dest:
            shutil.copyfileobj(source, dest, length=1024 * 1024)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "reconstructed_full_gtfs")
    parser.add_argument("--scenario", help="Optional scenario zip, e.g. 1974_v2.zip. Defaults to all scenarios.")
    parser.add_argument("--no-shapes-only", action="store_true", help="Rebuild no-shapes zips instead of full zips.")
    args = parser.parse_args()

    package_root = args.package_root.resolve()
    component_rows = read_csv(package_root / "metadata/GTFS_COMPONENT_MANIFEST.csv")
    scenarios = sorted({row["scenario_original_zip"] for row in component_rows})
    if args.scenario:
        scenarios = [scenario_key(args.scenario)]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for scenario in scenarios:
            no_shapes = tmp_dir / scenario.replace(".zip", "_no_shapes.zip")
            build_no_shapes(package_root, scenario, no_shapes, tmp_dir)
            if args.no_shapes_only:
                out = args.output_dir / no_shapes.name
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(no_shapes, out)
            else:
                out = args.output_dir / scenario
                add_shapes(package_root, no_shapes, scenario, out, tmp_dir)
            print(out)


if __name__ == "__main__":
    main()
