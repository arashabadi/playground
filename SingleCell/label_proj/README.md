
scANVI Tutorials and Pipelines

1. Basic Integration & Label Transfer
	•	Goal: Train scANVI from scratch with a labeled reference and an unlabeled query, then transfer labels.
	•	Best for: Standard label transfer workflows (e.g., cross-study or cross-tech).
	•	Tutorial link: Integration and label transfer with Tabula Muris
https://docs.scvi-tools.org/en/1.3.2/tutorials/notebooks/scrna/tabula_muris.html
⸻

2. Seed Labeling (Partial Labels)
	•	Goal: Start with a small set of seed labels and propagate them across unlabeled cells using scANVI.
	•	Best for: When you have very few annotated cells.
	•	Tutorial link: Seed labeling with scANVI
https://docs.scvi-tools.org/en/1.3.2/tutorials/notebooks/scrna/seed_labeling.html
⸻

3. scArches “Surgery” with scANVI
	•	Goal: Train a reference model once, then update (“surgery”) with new query data without full retraining.
	•	Best for: Mapping multiple new datasets efficiently into the same reference space.
	•	Tutorial link: Semi-supervised scANVI surgery pipeline (scArches)
https://docs.scarches.org/en/latest/scanvi_surgery_pipeline.html
⸻

4. Reference Mapping with scArches (SCVI/SCANVI/TOTALVI)
	•	Goal: Map new query data onto an existing pretrained model (SCVI, SCANVI, or TOTALVI) using scArches.
	•	Best for: Large-scale projects, multimodal data (e.g., CITE-seq), or when you need consistent embeddings across many queries.
	•	Tutorial link: Reference mapping with SCVI-Tools (multimodal)
https://docs.scvi-tools.org/en/1.3.2/tutorials/notebooks/multimodal/scarches_scvi_tools.html
⸻

5. API Reference (for custom pipelines)
	•	Goal: Learn available functions, parameters, and usage for scANVI in scvi-tools.
	•	Best for: Building your own pipeline, tuning hyperparameters, or integrating with custom preprocessing.
	•	Docs link: scANVI API — scvi-tools
https://docs.scvi-tools.org/en/stable/api/reference/scANVI.html