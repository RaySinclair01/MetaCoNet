# MetaCoNet
Metabolic Co-occurrence Network

**Simple Introduction:**
MetaCoNet is a computational pipeline for simulating metabolic interactions in microbial communities. It integrates automated genome-scale metabolic model reconstruction via CarveMe with iterative co-occurrence analysis to identify significant microbial assemblages, followed by community-level metabolic network inference using SMETANA. The toolkit processes microbial abundance data to generate representative co-occurring communities and evaluates metabolic complementarity and competition, supporting ecological and functional studies of microbiomes.

# MetaCoNet: Metabolic Co-occurrence Network Analysis Pipeline

## Overview

MetaCoNet is a modular computational framework designed to simulate and analyze metabolic interactions within microbial communities. This pipeline combines automated reconstruction of genome-scale metabolic models (GEMs) with statistical inference of higher-order species co-occurrences, culminating in community-level metabolic network modeling. By integrating tools such as CarveMe for individual species GEM reconstruction and SMETANA for interaction prediction, MetaCoNet enables the identification of statistically significant microbial assemblages and the quantification of metabolic complementarity and competition among community members.

The approach addresses key challenges in microbial ecology, including the combinatorial explosion in co-occurrence detection and the need for scalable metabolic simulations. It processes microbial relative abundance data to derive representative co-occurring communities, which are then used to model flux distributions and interaction networks. This workflow is particularly suited for analyzing complex microbiomes, such as those in environmental or host-associated samples, providing insights into ecological dynamics and functional potential.

The pipeline was developed to support reproducible analyses in systems biology, with core implementations in Python for co-occurrence computation and SMETANA execution. It relies on a controlled Conda environment to manage dependencies, ensuring compatibility across computational setups.

## Methodology

### Genome-Scale Metabolic Model Reconstruction
Individual species GEMs are reconstructed using CarveMe (version 1.6.1), an automated pipeline that processes protein sequence files in FASTA format. Sequence alignment is performed with DIAMOND as the alignment tool, yielding models in Systems Biology Markup Language (SBML) format. Species inclusion is determined by a relative abundance threshold of 0.1% across samples; sensitivity analyses with higher and lower thresholds confirmed negligible impacts on downstream results. Only species exceeding this threshold are retained for modeling.

### Higher-Order Co-occurrence Inference
To identify ecologically relevant microbial assemblages, an iterative algorithm computes co-occurrence statistics for species combinations starting from pairwise (n=2) up to higher orders (configurable up to n=5). For each combination generated from the full species list in a dataset, the observed co-occurrence frequency is calculated as the number of samples (subfolders) where all members co-occur.

Expected co-occurrence under independence is derived from the marginal probabilities of individual species across all samples. Statistical significance is assessed using a binomial distribution test to compute p-values for the deviation between observed and expected frequencies. P-values are adjusted for multiple testing via false discovery rate (FDR) correction to yield q-values. Significant combinations are filtered based on three criteria: (1) co-occurrence in at least 10 samples; (2) observed frequency at least twice the expected value; and (3) q < 0.05 post-FDR correction.

To mitigate computational demands from combinatorial growth, pre-filtering is applied prior to significance testing, using minimum sample count and frequency-to-expectation ratio thresholds. From the pool of significant combinations, the top 1,000 ranked by co-occurrence frequency are selected as representative communities. These are output as tab-separated value (TSV) files defining sample-specific community compositions.

### Community-Level Metabolic Network Analysis
The single-species SBML models and community TSV files serve as inputs to SMETANA (version 1.2.0), which performs flux balance analysis at the community scale. SMETANA employs a dynamic programming algorithm, solved using the Gurobi optimizer, to infer metabolic interactions including complementarity (mutualistic exchanges) and competition (resource overlap). This step generates network representations of flux dependencies, highlighting potential ecological roles within co-occurring assemblages.

### Workflow Visualization
Key stages include:

1. **Input Preparation**: Microbial abundance data and FASTA sequences.
2. **GEM Reconstruction**: CarveMe with DIAMOND alignment.
3. **Co-occurrence Computation**: Iterative combination generation and statistical testing.
4. **Community Definition**: Selection of top co-occurring assemblages.
5. **Network Inference**: SMETANA with Gurobi optimization.
6. **Output Generation**: Interaction networks, flux maps, and summary statistics.

Required packages for the workflow are managed via Conda and include:
- **CarveMe (v1.6.1)**: For GEM reconstruction (Python 3.12 compatible).
- **SMETANA (v1.2.0)**: For community metabolic modeling (Python 3.6 required).
- **DIAMOND**: Sequence alignment tool.
- **Gurobi Optimizer**: Commercial solver for linear programming (academic license recommended).
- **Python Libraries**: `itertools`, `collections.Counter`, `openpyxl` for co-occurrence analysis; `subprocess` and `os` for script execution.
- **Additional Dependencies**: COBRApy (for SBML handling), NumPy, Pandas, and SciPy (for statistical computations).

The full dependency list is specified in the `environment.yml` file for easy replication.

## Implementation Details

### Core Scripts

#### Computing Co-occurrence (co-occurrence_0720New.py)
This script implements the optimized co-occurrence detection algorithm. It generates all possible species combinations up to a user-defined maximum size (default: 5) from XML files in a target directory, computes frequencies, and ranks the top N (default: 1,000) combinations by occurrence count. To handle memory efficiency, it uses frozen sets for combinations and a heap-based approach for top-N selection (though simplified here for pairwise and higher-order enumeration).

Key functions:
- `find_cooccurring_species_optimized(folder_path, max_combo_size=5, top_n=1000)`: Enumerates and counts combinations across samples.
- `generate_excel_output_optimized(co_occurrences, output_filename="cooccurrence_communities.xlsx")`: Exports ranked communities to an Excel file with community IDs and species lists.

Usage example:
```python
python co-occurrence_0720New.py
```
Input: Directory containing species XML files (e.g., "DL_all").
Output: Excel file with top co-occurring communities.

Note: The script assumes co-occurrence is derived from file presence in subdirectories representing samples. For production use, extend with explicit sample traversal for precise frequency calculation.

#### SMETANA Execution (Smetana.py)
This script automates the execution of SMETANA across multiple sample subfolders. It activates a dedicated Conda environment and runs the SMETANA command on all XML files in each subdirectory, using a provided communities TSV file for input.

Key logic:
- Iterates over predefined group folders (e.g., "CK_XML", "DL_XML").
- For each sample subfolder, invokes: `python smetana_script_path *.xml -c communities.tsv`.

Usage example:
```python
python Smetana.py
```
Input: Main directory with subfolders containing SBML XML models and TSV community files.
Output: SMETANA-generated metabolic interaction reports per sample.

### Environment Setup
The pipeline requires two Conda environments for compatibility:
- `smetana_env` (Python 3.6): Install via `conda env create -f environment_smetana.yml`.
- `carveme_env` (Python 3.12): Install via `conda env create -f environment_carveme.yml`.

Activate the appropriate environment before running scripts. Full installation instructions are in `INSTALL.md`.

## Results and Validation
In benchmark applications, MetaCoNet successfully identified robust co-occurring communities and predicted metabolic interactions consistent with known microbial consortia. Outputs include ranked community lists, p-value distributions, and interaction matrices, facilitating integration with downstream ecological modeling.

## Institution
This project was developed at the:

Hunan Provincial University Key Laboratory for Environmental and Ecological Health

Hunan Provincial University Key Laboratory for Environmental Behavior and Control Principle of New Pollutants

College of Environment and Resources, Xiangtan University, Xiangtan 411105, China

## License and Citation
This work is licensed under the MIT License. For academic use, please cite the associated publication (details forthcoming).

For questions or contributions, contact the developers via GitHub issues.

## References
- Machado, D. et al. (2018). Fast automated reconstruction of genome-scale metabolic models for microbial species and communities. *Nucleic Acids Research*, 46(15), 7542–7548. (CarveMe)
- Zomorrodi, A. R. & Segre, D. (2016). Synthetic ecology of microbes: Mathematical and computational approaches. *Science*, 352(6290), 1179–1183. (SMETANA foundation)

                          
