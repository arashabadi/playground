# h5ad AnnData vs R Seurat object 

sceasy uses reticulate and thus depends on python environment. Proved to be unstable and hard to use.
SeuratDisk also uses rhdf5, but uses h5-based Seurat format as an intermediate that looks like overcomplication. Additionally, SeuratDisk seems to be almost not supported and it fails even on examples from its own tutorial.
Despite all problems of both packages above they have clear advantage over schard: they allow not only to read h5ad into R but also to write it.

- sceasy by Wellcome Sanger Institute:
https://github.com/cellgeni/sceasy

https://github.com/cellgeni/schard

https://github.com/xleizi/easySCF

No to seuratdisk as it works with V3 assay and outdated. It also crashes on heavy datasets!


Also:
https://github.com/theislab/anndata2ri

Also:
https://github.com/theislab/zellkonverter


## NOT TESTED:

### suggested by Pooria
- Conversions: h5Seurat and AnnData:

    https://mojaveazure.github.io/seurat-disk/articles/convert-anndata.html

    > Also works with Seaurat V5 (?)

- Zellkonverter h5ad to Seurat Obj:

    ```R
    library(zellkonverter)
    h5ad_file <- "/.../subset_1.h5ad"
    ad <- readH5AD(h5ad_file)

    library(Seurat)
    seurat_obj <- as.Seurat(
    ad,
    counts = "counts",
    data   = "logcounts",
    project = "ROSMAP"
    )

    seurat_obj
    head(seurat_obj@meta.data)
    ```