from pathlib import Path
import scanpy as sc
import pandas as pd
import matplotlib.pyplot as plt

input_path = Path(snakemake.input.object)
object_output = Path(snakemake.output.object)
markers_output = Path(snakemake.output.markers)
plot_output = Path(snakemake.output.marker_plot)
for path in [object_output, markers_output, plot_output]:
    path.parent.mkdir(parents=True, exist_ok=True)

combined = sc.read_h5ad(input_path)
resolution = float(snakemake.params.resolution)
cluster_key = f"leiden_res_{resolution:.2f}"
sc.tl.leiden(combined, resolution=resolution, flavor="igraph", n_iterations=2, random_state=snakemake.params.random_state, key_added=cluster_key)
sc.tl.rank_genes_groups(combined, groupby=cluster_key, method="wilcoxon")
markers = sc.get.rank_genes_groups_df(combined, group=None)
markers = markers[(markers["logfoldchanges"] > snakemake.params.logfoldthreshold) & (markers["pvals_adj"] < snakemake.params.padj_threshold)]
markers.to_csv(markers_output, index=False)

marker_genes = {
    "Myeloid": ["CD68", "CD14", "FCGR1A", "LYZ", "S100A8", "S100A9"],
    "Lymphoid": ["CD3D", "CD3E", "CD8A", "CD4", "NKG7", "KLRD1"],
    "Stromal": ["COL1A1", "COL1A2", "DCN", "LUM", "ACTA2"],
    "Epithelial": ["EPCAM", "KRT8", "KRT18", "KRT19", "MUC1"],
    "Endothelial": ["PECAM1", "VWF", "CDH5", "CLDN5", "KDR"],
}
sc.pl.dotplot(combined, marker_genes, groupby=cluster_key, show=False)
plt.savefig(plot_output, dpi=300, bbox_inches="tight")
plt.close()

cluster_map = {str(k): v for k, v in snakemake.params.cluster_map.items()}
combined.obs["cluster_label"] = combined.obs[cluster_key].astype(str).map(cluster_map)
if combined.obs["cluster_label"].isna().any():
    missing = sorted(combined.obs.loc[combined.obs["cluster_label"].isna(), cluster_key].astype(str).unique())
    raise ValueError(f"Unmapped broad clusters: {missing}")
combined.obs["cluster_label"] = combined.obs["cluster_label"].astype("category")
combined.write_h5ad(object_output)
