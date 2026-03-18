import sys, subprocess, logging

logger = logging.getLogger(__name__)

# function to verify conda
def conda_verify():
    """Verifica a instalação do conda e também a presença das ferramentas da pipeline no ambiente"""
    print("\nVERIFICANDO O CONDA")

    command_conda = ["conda", "--version"]
    tools = ["fastqc", "fastp", "multiqc", "fasterq-dump"]
    
    resp_conda = subprocess.run(command_conda, capture_output=True, text=True)

    if resp_conda.returncode == 0:
        print("CONDA: Instalação encontrada!")
        logger.info("CONDA: Instalação encontrada!")
        logger.info(resp_conda.stdout.strip())
    else:
        logger.error(f'CONDA: Instalação não encontrada: {resp_conda.stderr}')
        sys.exit("ERRO: Conda não instalado")

    try:
        for tool in tools:

            resp_tool = subprocess.run([tool, "--version"], capture_output=True, text=True)

            if resp_tool.returncode != 0:
                print(f"CONDA: {tool} não encontrado no ambiente.")
                logger.error(f"CONDA: {tool} não encontrado no ambiente.")
                sys.exit(f"ERRO: {tool} não encontrado no ambiente.")
            else:
                print(f"CONDA: {tool} encontrado.")
                logger.info(f"CONDA: {tool} encontrado.")
                logger.info(f'Versão {tool}: {resp_tool.stdout.strip()}')

    except FileNotFoundError:
        print("\nERRO: Ferramenta não encontrada.")
        logger.error("Ferramenta não encontrada.")
        logger.info("Ative o ambiente sra_qc.")
        sys.exit("CONDA: Ative o ambiente sra_qc -> conda activate sra_qc")
        