rule qc:
    input:
        object=p("raw_object")
    output:
        object=p("qc_object")
    params:
        **config["qc"]
    conda:
        "../envs/single_cell.yaml"
    log:
        str(BASE / config["paths"]["logs"] / "02_qc.log")
    script:
        "../scripts/02_qc.py"
