rule spatial_architecture:
    input:
        sample_346=p("spatial_346_c2l"),
        sample_355g=p("spatial_355g_c2l")
    output:
        done=touch(p("spatial_architecture_done"))
    conda:
        "../envs/spatial.yaml"
    notebook:
        "../notebooks/08_spatial_immune_architecture.ipynb"
