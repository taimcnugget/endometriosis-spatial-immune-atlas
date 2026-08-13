rule spatial_collection:
    output:
        sample_346=p("spatial_346_raw"),
        sample_355g=p("spatial_355g_raw")
    conda:
        "../envs/spatial.yaml"
    notebook:
        "../notebooks/00_spatial_data_collection.ipynb"
