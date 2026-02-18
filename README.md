# SRA-QC-Analysis Pipeline

An automated and modular **Python pipeline** for reproducible Quality Control (QC) and preprocessing of Illumina sequencing data (Single-end & Paired-end), downloaded directly from the Sequence Read Archive (SRA).

## 1. Features

- **Automated Download:** Fetches raw data using `fasterq-dump` (SRA Toolkit).
- **Quality Control:** Generates pre-trimming QC reports using `FastQC`.
- **Trimming & Filtering:** Cleans reads (adapters, low quality) using `fastp`.
- **Post-Trim QC:** Generates post-trimming QC reports.
- **Aggregation:** Compiles a final interactive HTML report using `MultiQC`.
- **Modular Design:** Easy to maintain and extend Python architecture.


## 2. Installation

### Prerequisites
- **Conda** or **Mamba** (Recommended for faster environment solving).
- **Git**


### 2.1 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/badecisions/SRA-QC-Analysis.git
   cd SRA-QC-Analysis
   ```

2. Create and activate the environment:
   ```bash
   # Create the environment from the provided file
   conda env create -f environment.yaml

   # Activate it
   conda activate sra_qc
   ```
   *(Note: Ensure your environment file is named `environment.yaml`. If it is named differently, adjust the command above).*


## 3. Usage

The pipeline is executed via the `main.py` script. You can process multiple SRA IDs in a single run.

```bash
python main.py --sra <SRA_ID_1> <SRA_ID_2> ... [OPTIONS]
```

```bash
python main.py -f ID_list.txt ... [OPTIONS]
```


### 3.1 Arguments

| Argument    | Description                                     |  Default   |
| :---------- | :---------------------------------------------- | :--------: |
| `--sra`     | List of SRA Accession IDs (e.g., `SRR123456`)   |     -      |
| `--file`    | File .txt with SRA Accession IDs (one per line) |     -      |
| `--outdir`  | Directory for outputs files                     | `results/` |
| `--help`    | Show help message                               |     -      |
| `--threads` | Specifies the number of threads used            |     4      |
| `--data`    | Directory for Raw and Processed data            |  `data/`   |


### 3.2 Examples


**3.2.1 Basic Run (Single Sample):**
```bash
python main.py --sra SRR1153403
```


**3.2.2 Multi-Sample Run (Paired-end supported automatically):**
```bash
python main.py --sra SRR1153403 SRR1234567 --outdir my_analysis_2026
```


**3.2.3 Reading a list of IDs from a file**
```bash
python main.py --file sra_ids.txt
```


## 4. Output Structure

The pipeline organizes files into a clean directory structure:

```text
results/
├── 01_fastqc_raw/        # FastQC reports for raw data
├── 02_fastp_report/      # Fastp reports
├── 03_fastqc_clean/      # FastQC reports for trimmed data
└── 04_multiqc/           # Aggregated MultiQC report (HTML)

data/
├── raw/                  # Raw .fastq files downloaded from SRA
└── processed/            # Cleaned .fq.gz files (output from fastp)

logs/
├── run_datatime.log      # Log of the pipeline execution
├── ID_fasterq-dump.log   # Log from Fasterq-dump (one per ID)
└── ID_fastp.log          # Log from Fastp (one per ID)
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Contributions & Support
Contributions and suggestions for new features are welcome, as possibles bug reports.

 To these, please create a new issue, including examples and logs when possible. 
 
 And if you want to PR and add some features, or fixing we're welcome to do this.