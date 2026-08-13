"""Prepare the immune-only object for the manually curated notebook-5 annotation step.

This script intentionally does not invent final fine-grained immune labels. It subsets
broad Myeloid/Lymphoid cells, removes proliferating cells if already labeled, and writes
the object expected by the refactored immunosenescence analysis.
"""
from pathlib import Path
import scanpy as sc

input_path = Path(snakemake.input.object)
output_path = Path(snakemake.output.object)
output_path.parent.mkdir(parents=True, exist_ok=True)

adata = sc.read_h5ad(input_path)
labels = set(snakemake.params.immune_labels)
immune = adata[adata.obs["cluster_label"].astype(str).isin(labels)].copy()

# Final cell_type and cell_type_short are manually curated in notebook 5.
required = {"cell_type", "cell_type_short"}
missing = required - set(immune.obs.columns)
if missing:
    raise ValueError(
        "The broad immune subset was created, but final notebook-5 annotations are missing: "
        f"{sorted(missing)}. Run the refactored immune-annotation notebook once and save "
        f"its output to {output_path}."
    )

if "Proliferating" in immune.obs["cell_type_short"].astype(str).unique():
    immune = immune[immune.obs["cell_type_short"].astype(str) != "Proliferating"].copy()

immune.write_h5ad(output_path)
