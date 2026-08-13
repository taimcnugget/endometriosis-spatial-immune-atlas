rule data_collection:
    input:
        raw_dir=p("raw_data")
    output:
        object=p("raw_object")
    params:
        exclude=config["dataset"]["exclude"]
    conda:
        "../envs/single_cell.yaml"
    log:
        str(BASE / config["paths"]["logs"] / "01_data_collection.log")
    script:
        "../scripts/01_data_collection.py"
