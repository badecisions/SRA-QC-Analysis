from pathlib import Path
import subprocess
import sys

# function to verify the existence of the directories
def directories_verify():
    """Verifica a presença de todos os diretórios necessários, e caso não existam cria eles."""
    print("Verificando a integridade das pastas...")
    results_base = Path("results")
    results_raw = results_base / "01_fastqc_raw"
    results_report = results_base / "02_fastp_report"
    results_clean = results_base / "03_fastqc_clean"
    results_multi = results_base / "04_multiqc"
    
    logs = Path("logs")

    data_base = Path("data")
    data_raw = data_base / "raw"
    data_processed = data_base / "processed"
    data_refs = data_base / "refs"

    directories = [results_base, results_raw, results_report, 
                   results_clean, results_multi, logs, 
                   data_base, data_raw, data_processed, data_refs]

    for dir in directories:
        dir.mkdir(exist_ok=True)

    print("Estrutura de diretórios completa!\n")

# function to verify conda
def conda_verify():
    """Verifica a instação do conda e também a presença das ferramentas da pipeline no ambiente"""

    command_conda = ["conda", "--version"]
    command_tools = ["fastqc", "--version", "&&", 
                     "fastp", "--version", "&&", 
                     "multiqc", "--version", "&&", 
                     "fasterq-dump", "--version"]
    
    resp_conda = subprocess.run(command_conda, capture_output=True, text=True)

    if resp_conda.returncode == 0:
        print("Instalação do conda encontrada!")
    else:
        sys.exit("Conda não instalado")

    try:     
        resp_tools = subprocess.run(command_tools, capture_output=True, text=True)
        if resp_tools.returncode == 0:
            print("Ferramentas encontradas!")
    except FileNotFoundError:
        print("\nFerramentas não encontradas!")
        print("Ative o ambiente sra_qc.")