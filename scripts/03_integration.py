from pathlib import Path
import scanpy as sc
import harmonypy

input_path = Path(snakemake.input.object)
output_path = Path(snakemake.output.object)
output_path.parent.mkdir(parents=True, exist_ok=True)

combined = sc.read_h5ad(input_path)
combined.layers["counts"] = combined.X.copy()
sc.pp.normalize_total(combined, target_sum=snakemake.params.target_sum)
sc.pp.log1p(combined)
sc.pp.highly_variable_genes(combined, n_top_genes=snakemake.params.n_top_genes, batch_key="sample_id")
sc.tl.pca(combined, n_comps=snakemake.params.n_pcs, use_highly_variable=True, random_state=snakemake.params.random_state)
ho = harmonypy.run_harmony(combined.obsm["X_pca"], combined.obs, "sample_id")
harmony = ho.Z_corr
if harmony.shape[0] != combined.n_obs:
    harmony = harmony.T
combined.obsm["X_pca_harmony"] = harmony
sc.pp.neighbors(combined, use_rep="X_pca_harmony", n_neighbors=snakemake.params.n_neighbors, random_state=snakemake.params.random_state)
sc.tl.umap(combined, random_state=snakemake.params.random_state)
combined.write_h5ad(output_path)
