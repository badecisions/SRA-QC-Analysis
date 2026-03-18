from pathlib import Path
import subprocess, logging

logger = logging.getLogger(__name__)

def quality_control(data_path:str, results_path:str, threads:int, raw:bool, sra_ids:list):
    """Realiza o controle de qualidade dos arquivos .fastq, usando o fastqc"""

    path_data = Path(data_path) / ("raw" if raw else "processed")
    path_output = Path(results_path) / ("01_fastqc_raw" if raw else "03_fastqc_clean")

    threads = str(threads)

    logger.info("Raw mode" if raw else "Processed mode")

    for i in sra_ids:
        print(f"\nID {i}")
        logger.info(f"FastQC: Iniciando ID {i}")

        padrao = f"{i}*" + (".fastq" if raw else ".fq.gz")
        arquivos_encontrados = list(path_data.glob(padrao))

        if not arquivos_encontrados:
            logger.warning(f"FastQC: Nenhum arquivo encontrado para {i} com padrão '{padrao}'")
            continue

        suffix = "raw" if raw else "clean"
        log_path = Path("logs") / f"{i}_fastqc_{suffix}.log"

        command_fastqc = ["fastqc", "--outdir", path_output, "--threads", threads]

        arquivos_str = [str(arq) for arq in arquivos_encontrados]

        run_cmd = command_fastqc + arquivos_str

        logger.info(f"Command: {' '.join(map(str, run_cmd))}")

        with open(log_path, "w") as log_file:
            fastqc = subprocess.run(run_cmd, stdout=log_file, stderr=log_file, text=True)

        if fastqc.returncode != 0:
            print(f"ERRO no ID {i}:")
            logger.error(f"FastQC falhou para {i}. Verifique: {log_path}")
        else:
            print(f'FastQC: concluído para o ID {i}')
            logger.info(f"FastQC: Concluído com sucessso ID {i}")
