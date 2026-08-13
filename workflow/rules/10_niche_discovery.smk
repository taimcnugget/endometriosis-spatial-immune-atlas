rule niche_discovery:
    input:
        spatial=p("spatial_immunosenescence_done")
    output:
        object=p("spatial_niche_object")
    params:
        **config["spatial_niches"]
    conda:
        "../envs/cellcharter.yaml"
    resources:
        mem_mb=48000
    notebook:
        "../notebooks/10_niche_discovery.ipynb"
