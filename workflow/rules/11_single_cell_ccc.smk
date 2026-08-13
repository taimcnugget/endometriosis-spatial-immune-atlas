rule single_cell_ccc:
    input:
        object=p("immunosenescence_object")
    output:
        done=touch(p("single_cell_ccc_done"))
    params:
        **config["single_cell_ccc"]
    conda:
        "../envs/ccc.yaml"
    resources:
        mem_mb=52000
    notebook:
        "../notebooks/11_single_cell_ccc.ipynb"
