from pathlib import Path

# function to verify the existence of the directories
def directories_verify(output_folder:str):
    """Verifica a presença de todos os diretórios necessários, e caso não existam cria eles."""
    print("Verificando a integridade das pastas...")
    results_base = Path(output_folder)
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