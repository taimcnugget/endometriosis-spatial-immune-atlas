rule spatial_niche_ccc:
    input:
        object=p("spatial_niche_object")
    output:
        done=touch(p("spatial_niche_ccc_done"))
    params:
        **config["spatial_ccc"]
    conda:
        "../envs/spatial.yaml"
    resources:
        mem_mb=52000
    notebook:
        "../notebooks/12_spatial_niche_ccc.ipynb"
