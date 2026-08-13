rule cell2location:
    input:
        reference=p("immunosenescence_object"),
        sample_346=p("spatial_346_raw"),
        sample_355g=p("spatial_355g_raw")
    output:
        sample_346=p("spatial_346_c2l"),
        sample_355g=p("spatial_355g_c2l")
    conda:
        "../envs/cell2location.yaml"
    resources:
        mem_mb=48000
    script:
        "../scripts/07_spatial_cell2location.py"
