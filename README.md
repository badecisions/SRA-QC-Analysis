
## SRA-QC-Analysis Pipeline

An automated Bash pipeline for reproducible Quality Control (QC) analysis of single-end Illumina sequencing data downloaded directly from the Sequence Read Archive (SRA).

### Installation/Setup
**Recommended method:** Using the Devcontainer. 
- Provides a fully configured and reproducible environment with minimal setup.
- *Requirements:* Docker, VS Code with Dev Containers extension.

Clone this repository, open the folder in VS Code, and select "Reopen in Container" when prompted.
```bash
git clone https://github.com/badecisions/SRA-QC-Analysis.git
```

**Alternative method:** Reconstruct the Conda/Mamba environment.
- Provides the necessary software but is less reproducible across different systems than the Devcontainer method.
- *Requirements:* Mamba/Conda.

Clone this repository, navigate into the project directory in your terminal, and create the environment using the provided file: `SRA-QC-Analysis.yaml`
```bash
git clone https://github.com/badecisions/SRA-QC-Analysis.git
cd SRA-QC-Analysis
conda env create -f SRA-QC-Analysis.yaml
conda activate qc_env
```

### Usage
The basic command structure is:

```bash
bash path/to/run_qc_pipeline.sh SRA_ID_1 [SRA_ID_2 SRA_ID_3 ...]
```

Currently, this pipeline only supports single-end SRA datasets. Support for paired-end files is under development.

#### Input
- One or more valid SRA accession IDs corresponding to single-end Illumina sequencing runs

#### Output
- Three new directories will be created: `1-raw_data`, `2-qc_reports` and `3-trimmed_data
	- `1-raw_files` - Raw .fastq.gz data from the SRAs
	- `2-qc_reports` - Contains FastQC reports for both raw and trimmed data, along with a final aggregated MultiQC report (`multiqc_report.html`)
	- `3-trimmed_data` - Contains the trimmed files in the `fq.gz` format

##### Example
```bash
# Download and run QC analysis for two SRA datasets
bash run_qc_pipeline.sh SRR1153403 SRRXXXXXXX
```

#### License
This project is licensed under the MIT License - see the LICENSE file for details.
