rule immune_annotation:
    input:
        object=p("cluster_object")
    output:
        object=p("immune_annotation_object")
    params:
        **config["immune_annotation"]
    conda:
        "../envs/single_cell.yaml"
    log:
        str(BASE / config["paths"]["logs"] / "05_immune_annotation.log")
    script:
        "../scripts/05_immune_annotation.py"
