rule total_clustering:
    input:
        object=p("integration_object")
    output:
        object=p("cluster_object"),
        markers=p("cluster_markers"),
        marker_plot=p("cluster_marker_plot")
    params:
        **config["total_clustering"]
    conda:
        "../envs/single_cell.yaml"
    log:
        str(BASE / config["paths"]["logs"] / "04_total_clustering.log")
    script:
        "../scripts/04_total_clustering.py"
