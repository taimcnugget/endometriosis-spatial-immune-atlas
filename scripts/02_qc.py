from pathlib import Path
import scanpy as sc

input_path = Path(snakemake.input.object)
output_path = Path(snakemake.output.object)
output_path.parent.mkdir(parents=True, exist_ok=True)

combined = sc.read_h5ad(input_path)
combined.var["mt"] = combined.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(combined, qc_vars=["mt"], percent_top=None, inplace=True, log1p=False)
sc.pp.filter_cells(combined, min_genes=snakemake.params.min_genes)
sc.pp.filter_cells(combined, min_counts=snakemake.params.min_counts)
sc.pp.filter_cells(combined, max_counts=snakemake.params.max_counts)
combined = combined[combined.obs["pct_counts_mt"] <= snakemake.params.mt_threshold].copy()
sc.pp.scrublet(combined, batch_key="sample_id")
combined = combined[~combined.obs["predicted_doublet"]].copy()
sc.pp.filter_genes(combined, min_cells=snakemake.params.min_cells)
combined.write_h5ad(output_path)
