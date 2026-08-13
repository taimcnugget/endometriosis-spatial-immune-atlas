rule integration:
    input:
        object=p("qc_object")
    output:
        object=p("integration_object")
    params:
        **config["integration"]
    conda:
        "../envs/single_cell.yaml"
    resources:
        mem_mb=32000
    log:
        str(BASE / config["paths"]["logs"] / "03_integration.log")
    script:
        "../scripts/03_integration.py"
