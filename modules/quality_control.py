from pathlib import Path
import subprocess

def quality_control(data_path:str, results_path:str, threads:int, raw:bool, sra_ids:list):
    """Realiza o controle de qualidade dos arquivos .fastq, usando o fastqc"""

    path_data = Path(data_path) / ("raw" if raw else "processed")
    path_output = Path(results_path) / ("01_fastqc_raw" if raw else "03_fastqc_clean")

    threads = str(threads)

    for i in sra_ids:
        print(f"\nID {i}")

        padrao = f"{i}*" + (".fastq" if raw else ".fq.gz")
        arquivos_encontrados = list(path_data.glob(padrao))

        log_path = Path("logs") / f"{i}_fastqc.log"

        command_fastqc = ["fastqc", "--outdir", path_output, "--threads", threads]

        for arq in arquivos_encontrados:
            command_fastqc.append(str(arq))

            with open(log_path, "w") as log_file:
                fastqc = subprocess.run(command_fastqc, stdout=log_file, stderr=log_file, text=True)

            if fastqc.returncode != 0:
                print(f"ERRO no ID {i}:")
                print(fastqc.stderr)
            else:
                print(f'FastQC concluído para o ID {i}')
