rule spatial_immunosenescence:
    input:
        architecture=p("spatial_architecture_done"),
        reference=p("immunosenescence_object")
    output:
        done=touch(p("spatial_immunosenescence_done"))
    conda:
        "../envs/spatial.yaml"
    notebook:
        "../notebooks/09_spatial_immunosenescence.ipynb"
