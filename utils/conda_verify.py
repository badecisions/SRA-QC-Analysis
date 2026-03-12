import sys, subprocess, logging

logger = logging.getLogger(__name__)

# function to verify conda
def conda_verify():
    """Verifica a instação do conda e também a presença das ferramentas da pipeline no ambiente"""
    print("\nVERIFICANDO O CONDA")

    command_conda = ["conda", "--version"]
    command_tools = ["fastqc", "--version", "&&", 
                     "fastp", "--version", "&&", 
                     "multiqc", "--version", "&&", 
                     "fasterq-dump", "--version"]
    
    resp_conda = subprocess.run(command_conda, capture_output=True, text=True)

    if resp_conda.returncode == 0:
        print("CONDA: Instalação encontrada!")
        logger.info("CONDA: Instalação encontrada!")
        logger.info(resp_conda.stdout)
    else:
        logger.error(f'CONDA: Instalação não encontrada: {resp_conda.stderr}')
        sys.exit("ERRO: Conda não instalado")

    try:     
        resp_tools = subprocess.run(command_tools, capture_output=True, text=True)
        if resp_tools.returncode == 0:
            print("CONDA: Ambiente ativo e Ferramentas encontradas!")
            logger.info(f"CONDA: Ambiente ativo e Ferramentas encontradas")
            logger.info(f'Versão das ferramentas: {resp_tools.stdout}')
    except FileNotFoundError:
        print("\nERRO: Nenhuma ferramenta encontrada.")
        logger.error("Nenhuma ferramenta encontrada.")
        logger.info("Ative o ambiente sra_qc.")
        sys.exit("CONDA: Ative o ambiente sra_qc -> conda activate sra_qc")
        