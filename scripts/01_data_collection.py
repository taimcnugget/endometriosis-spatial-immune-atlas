from pathlib import Path
import anndata as ad
import scanpy as sc
from metadata_gse179640 import METADATA

output_path = Path(snakemake.output.object)
output_path.parent.mkdir(parents=True, exist_ok=True)
exclude = set(snakemake.params.exclude)

metadata = METADATA
h5_files = sorted(Path(snakemake.input.raw_dir).rglob("*.h5"))
adatas = []

for file in h5_files:
    sample_id = file.name.replace("_filtered_feature_bc_matrix.h5", "")
    if any(label in sample_id for label in exclude) or sample_id not in metadata:
        continue
    adata = sc.read_10x_h5(file)
    adata.var_names_make_unique()
    meta = metadata[sample_id]
    for key, value in meta.items():
        adata.obs[key] = value
    adata.obs["sample_id"] = sample_id
    adata.obs["dataset"] = "GSE179640"
    adata.obs_names = [f"{sample_id}_{barcode}" for barcode in adata.obs_names]
    adatas.append(adata)

if not adatas:
    raise ValueError("No valid GSE179640 samples were loaded.")

combined = ad.concat(adatas, join="outer", merge="same")
combined.var_names_make_unique()
combined.write_h5ad(output_path)
