# Welcome to the PATOG Wiki
*Bioinformatics and Computational Biology Learning Roadmap (from ZERO to HERO!)*

> ⚠️ UNDER MAINTENANCE & UPDATES

![Bioinformatics Roadmap](https://github.com/cellravel/patog/blob/main/images/bioinfo_curriculum_structure_fr_layout.png)
[OPEN ROADMAP PHOTO_High Res](https://raw.githubusercontent.com/cellravel/patog/main/images/bioinfo_curriculum_structure_fr_layout.png)

## Introduction

This roadmap is designed to guide learners through the fields of Bioinformatics and Computational Biology. These intertwined disciplines combine biology, computer science, and mathematics to analyze, model, and interpret complex biological data and systems.

To better understand the Differences Between Computational Biology and Bioinformatics, please visit [Pluto website](https://pluto.bio/resources/Learning%20Series/differences-between-computational-biology-and-bioinformatics).

## Overview

This Wiki is structured to cover the following key areas:

1. **Omics Data Analysis and Interpretation**: Techniques and tools for analyzing multi-omics data.
2. **Modeling and Simulation**: Modeling and simulation of biological systems.
3. **Integrated Platforms, Tools, and Technologies**: Modern SaaS platforms, HPC, and data visualization tools.
4. **Specialized Topics**: Clinical Bioinformatics, Personalized Medicine, and more.
5. **Additional Resources**: Books, courses, and career guidance.

## Getting Started

Before diving into the main sections, ensure you have a solid understanding of the [Prerequisites](./Prerequisites) based on your background in either computational or biological sciences.

## Navigation

- [Prerequisites](./Prerequisites)
- [Omics Data Analysis and Interpretation](./Main-Sections/Data-Analysis-and-Interpretation.md)
- [Modeling and Simulation](./Main-Sections/Modeling-and-Simulation.md)
- [Integrated Platforms, Tools, and Technologies](./Main-Sections/Integrated-Platforms-Tools-and-Technologies.md)
- [Specialized Topics](./Specialized-Topics.md)
- [Additional Resources](./Additional-Resources.md)

---

# Understanding the Differences: Biomedical Engineering

As you navigate the **Bioinformatics and Computational Biology Roadmap**, you may encounter terms and fields that are related but distinct from bioinformatics. These fields often belong to **Biomedical Engineering**. While they share certain computational and biological concepts, their focus, goals, and tools are different. Below, we explain these fields, provide examples of tools used in each, and clarify how they differ from bioinformatics. However, it's important to recognize that some areas, like **Genetic Engineering** and **CRISPR**, are closely related to bioinformatics.

1. **Bioelectronics** involves applying electrical engineering principles to create devices that interact with biological systems. Examples include pacemakers, biosensors, and lab-on-a-chip technologies.

- **Tools**: 
  - **MATLAB** for signal processing.
  - **COMSOL Multiphysics** for simulating electronic circuits in biological environments.
  
- **Why It's Different**: Bioelectronics focuses on hardware design and electrical circuits, whereas bioinformatics is centered on analyzing biological data. The physical creation and optimization of devices, rather than data analysis, are the primary concerns of bioelectronics.

2. **Biomaterials** is the study and development of materials that can interact with biological systems, such as implants, prosthetics, and drug delivery systems.

- **Tools**: 
  - **Finite Element Analysis (FEA)** software like **Abaqus** for simulating material behavior.
  - **Material Studio** for molecular modeling of biomaterials.
  
- **Why It's Different**: Biomaterials research is concerned with the properties and interactions of materials within biological environments. While computational tools are used, the focus is on material properties, not on the analysis of biological data typical in bioinformatics.

3. **Biomechanics** studies the mechanics of biological systems, often involving the analysis of movement and the forces exerted by and on the body.

- **Tools**:
  - **OpenSim** for musculoskeletal modeling and simulation.
  - **ANSYS** for biomechanical simulations.

- **Why It's Different**: Biomechanics is concerned with physical forces and movements within biological systems, not with molecular data analysis or biological sequence data, which are the focus areas of bioinformatics.

4. **Biomedical Imaging** refers to techniques for visualizing the internal structures and functions of the body, such as MRI, CT scans, and ultrasound.

- **Tools**:
  - **ImageJ** for image analysis and processing.
  - **3D Slicer** for medical image visualization and analysis.
  
- **Why It's Different**: Biomedical imaging focuses on the acquisition and processing of images from biological systems. Bioinformatics might intersect here in image analysis using machine learning, but the primary goal of biomedical imaging is to visualize and diagnose, not to analyze biological data sequences.

5. **Bioinstrumentation** is the development of instruments and devices for measuring biological parameters, such as heart rate monitors, glucose sensors, and EEG machines.

- **Tools**:
  - **LabVIEW** for designing and testing bioinstrumentation.
  - **MATLAB** for data acquisition and analysis from biomedical devices.
  
- **Why It's Different**: Bioinstrumentation is about creating devices that collect biological data, whereas bioinformatics focuses on analyzing biological data after it has been collected, often on a molecular level (e.g., DNA, RNA).

6. **Bionanotechnology** involves applying nanotechnology in biological systems, such as in drug delivery mechanisms or nanoscale biosensors.

- **Tools**:
  - **NAMD** and **VMD** for molecular dynamics simulations at the nanoscale.
  - **NanoEngineer-1** for designing nanoscale devices.
  
- **Why It's Different**: Bionanotechnology is about manipulating biological systems at the nanoscale to create new materials or devices. Bioinformatics, on the other hand, deals with large-scale data analysis rather than the design and synthesis of materials.

7. **Cellular and Tissue Engineering** is the development of biological tissues through engineering techniques, such as creating artificial organs or regenerating tissues.

- **Tools**:
  - **BioCAD** for designing tissue scaffolds.
  - **CellDesigner** for modeling biochemical networks involved in tissue growth.

- **Why It's Different**: This field is focused on building functional biological tissues, often through physical and biochemical means, rather than analyzing biological data, which is the main focus of bioinformatics.

8. **Clinical Engineering** involves the application of engineering principles to healthcare, particularly in managing medical equipment and technologies in clinical settings.

- **Tools**:
  - **Healthcare technology management (HTM) systems** for managing medical devices.
  - **Calibration and testing tools** for ensuring the accuracy of medical devices.
  
- **Why It's Different**: Clinical engineering focuses on the practical application and maintenance of medical devices within healthcare environments, not on the computational analysis of biological data that bioinformatics focuses on.

9. **Medical Devices** are tools used for diagnosing, preventing, or treating diseases, such as insulin pumps, defibrillators, and imaging machines.

- **Tools**:
  - **SolidWorks** for designing medical devices.
  - **Mimics** for creating 3D models from medical imaging data.
  
- **Why It's Different**: The focus here is on the design, development, and regulation of physical devices, not on data analysis or computational biology.

10. **Neural Engineering** is the application of engineering techniques to the nervous system, including brain-computer interfaces and neuroprosthetics.

- **Tools**:
  - **EEGLAB** for processing EEG data.
  - **BCI2000** for brain-computer interface research.
  
- **Why It's Different**: Neural engineering involves creating interfaces between machines and the nervous system, focusing on signal processing and device development, rather than on the computational analysis of molecular data typical in bioinformatics.

11. **Rehabilitation Engineering** focuses on creating technologies to help individuals with disabilities, such as prosthetics, orthotics, and assistive technologies.

- **Tools**:
  - **Gait analysis software** for assessing movement disorders.
  - **Prosthetic design software** like **Creo** for designing assistive devices.
  
- **Why It's Different**: This field is dedicated to the design and development of devices to aid rehabilitation, rather than the computational analysis of biological data.

12. **Orthopedic Bioengineering** involves the study and development of implants and devices for the musculoskeletal system, such as hip replacements and spinal implants.

- **Tools**:
  - **Finite Element Analysis (FEA)** software for simulating orthopedic devices.
  - **Orthoview** for preoperative planning and implant selection.

- **Why It's Different**: Orthopedic bioengineering is focused on the mechanical and material aspects of devices used in orthopedics, not on analyzing biological sequence data or omics data.

13. **Biopharmaceutical Engineering** is concerned with the development and manufacturing of therapeutic drugs and biologics, such as vaccines and monoclonal antibodies.

- **Tools**:
  - **Bioprocess simulation software** like **BioSolve Process**.
  - **Pharmacokinetic modeling software** such as **NONMEM**.

- **Why It's Different**: While bioinformatics plays a role in drug discovery (e.g., analyzing genetic data), biopharmaceutical engineering focuses on the production, formulation, and regulatory aspects of drug development.

## 14. Biomolecular Engineering
**Biomolecular Engineering** involves designing and manipulating molecules for specific biological functions, such as enzymes, antibodies, or synthetic DNA.

- **Tools**:
  - **PyMOL** for visualizing and manipulating molecular structures.
  - **Rosetta** for protein structure prediction and design.
  
- **Why It's Different**: Although bioinformatics tools are used for analyzing biomolecules, biomolecular engineering is focused on the physical creation and optimization of these molecules, rather than on large-scale data analysis.

## 15. Genetic Engineering and CRISPR
**Genetic Engineering** is the direct manipulation of an organism's DNA to alter its characteristics. Techniques like **CRISPR-Cas9** allow for precise editing of genes, making this a powerful tool in biotechnology and medicine.

- **Tools**:
  - **CRISPR-Cas9** systems for gene editing.
  - **Geneious** and **Benchling** for sequence analysis and design.
  - **BLAST** for sequence alignment and comparison.
  - **Galaxy** for managing and analyzing sequence data.

- **Why It's Related to Bioinformatics**: Genetic engineering, especially with tools like CRISPR, is closely related to bioinformatics. Before editing genes, extensive computational analysis is required to identify target sequences, predict off-target effects, and design guide RNAs. Bioinformatics tools are essential for analyzing genomic data, predicting outcomes, and optimizing gene editing strategies. This field exemplifies the intersection between computational biology and practical biotechnology, where data analysis directly informs experimental techniques.

## Summary
While the fields of **Biomedical Engineering** share some computational tools and biological concepts with **Bioinformatics** and **Computational Biology**, their core focuses are different. Biomedical Engineering and Biotechnology emphasize the design, creation, and optimization of physical devices, materials, and systems that interact with biological organisms. In contrast, bioinformatics is dedicated to the analysis of biological data, such as DNA sequences, protein structures, and gene expression patterns. However, in areas like **Genetic Engineering** and **CRISPR**, bioinformatics is deeply integrated, supporting the computational aspects necessary for these advanced biotechnological applications.

_Thanks to [Pedram](https://github.com/PedramKhalaj) for his help in comparing Biomedical Engineering and Bioinformatics._
