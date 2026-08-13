rule immunosenescence:
    input:
        object=p("immune_annotation_object")
    output:
        object=p("immunosenescence_object")
    conda:
        "../envs/single_cell.yaml"
    resources:
        mem_mb=32000
    notebook:
        "../notebooks/06_immunosenescence.ipynb"
