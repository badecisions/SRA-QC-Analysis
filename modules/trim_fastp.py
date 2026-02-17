import subprocess
from pathlib import Path

def trimm_files(data_path:str, results_path:str, sra_ids:list, paried_end:bool, threads:int):
    """
    Realiza a limpeza de reads com o fastp.
    
    :param data_path: caminho do diretório de data
    :type data_path: str
    :param results_path: caminho do diretório de resultados
    :type results_path: str
    :param sra_ids: lista de ids dos arquivos sra
    :type sra_ids: list
    :param paried_end: argumento que mostra se os arquivos recebidos são, ou não, paired-end
    :type paried_end: bool
    :param threads: número de threads a serem utilizadas pelo fastp.
    :type threads: int
    """

    path_data_input = Path(data_path) / "raw"
    path_data_output = Path(data_path) / "processed"
    path_output = Path(results_path) / "02_fastp_report"

    threads = str(threads)

    for i in sra_ids:
        print(f"ID {i}")

        R1_name = (i + "_1" if paried_end else i)
        extension = ".fastq"
        extension_output = ".fq.gz"

        R1_path_input = path_data_input / (R1_name + extension)

        R1_path_output = path_data_output / (R1_name + extension_output)

        html_out = path_output / (i + ".html")
        json_out = path_output / (i + ".json")

        if paried_end == True:
            R2_name = i + "_2"

            R2_path_input = path_data_input / (R2_name + extension)
            R2_path_output = path_data_output / (R2_name + extension_output)

            command_fastp = ["fastp", 
                        "--in1", R1_path_input, "--out1", R1_path_output,
                        "--in2", R2_path_input, "--out2", R2_path_output,
                        "-w", threads,
                        "-h", html_out,
                        "-j", json_out]
        else:
            command_fastp = ["fastp", 
                            "--in1", R1_path_input, "--out1", R1_path_output,
                            "-w", threads,
                            "-h", html_out,
                            "-j", json_out]

        fastp = subprocess.run(command_fastp, capture_output=True, text=True)

        if fastp.returncode != 0:
                print(f"ERRO no ID {i}:")
                print(fastp.stderr)
        else:
                print(f'Fastp concluído para o ID {i}')

trimm_files(data_path='data', results_path='results', sra_ids=["SRR37189381"], paried_end=False, threads=4)