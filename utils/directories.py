from pathlib import Path

# function to verify the existence of the directories
def create_directories(output_folder:str, data_folder:str):
    """Cria/verifica todos os diretórios necessários."""
    
    print("DIRETÓRIOS")
    
    print("Criando os diretórios necessários...")

    results_base = Path(output_folder)
    results_raw = results_base / "01_fastqc_raw"
    results_report = results_base / "02_fastp_report"
    results_clean = results_base / "03_fastqc_clean"
    results_multi = results_base / "04_multiqc"
    
    logs = Path("logs")

    data_base = Path(data_folder)
    data_raw = data_base / "raw"
    data_processed = data_base / "processed"

    print(f'''
            resultados: {results_base.absolute()}
            logs: {logs.absolute()}
            data: {data_base.absolute()}
            ''')

    directories = [results_base, results_raw, results_report, 
                   results_clean, results_multi, logs, 
                   data_base, data_raw, data_processed]

    for dir in directories:
        dir.mkdir(exist_ok=True)

    print("Estrutura de diretórios completa!\n")