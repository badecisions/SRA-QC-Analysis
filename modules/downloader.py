
from pathlib import Path
import sys, subprocess, logging

# config info log
logger = logging.getLogger(__name__)

def _run_command(command:list, id_name:str|Path, tool_name):
    """Executa o comando no subprocesso"""

    run_cmd = command + [str(id_name)]

    logger.info(f"{tool_name}: Processando o ID {id_name}")
    logger.info(f"Comando utilizado: {' '.join(map(str, run_cmd))}")


    temp_name = str(id_name)

    if '.sra' in temp_name:
        corrigido_id = Path(id_name).parent.name
    else:
        corrigido_id = id_name
    
    log_path = Path("logs") / f"{corrigido_id}_{tool_name}.log"

    if not Path("logs").exists():
        Path("logs").mkdir()

    with open(log_path, "w") as log_file:
            try:
                result = subprocess.run(run_cmd, stdout=log_file, stderr=log_file, text=True, check=False)

                if result.returncode != 0:
                    logger.error(f"{tool_name} falhou para {corrigido_id}")
                    logger.error(f"Código: {result.returncode}")
                else:
                    logger.info(f"{tool_name}: {corrigido_id} concluído")
                    return corrigido_id
                
            except FileNotFoundError:
                logger.error(f'{tool_name}: Não encontrado no PATH.')
                sys.exit(1)


def prefetch_run(sra_ids:list, download_path:str) -> list:
    """Coordena a execução do Prefetch para o download de arquivos .sra"""

    download = Path(download_path) / "raw"
    sucesso_ids = []

    command_prefetch = ["prefetch", "-O", download, "-v"]

    print("\nPrefetch: Iniciando os Downloads")

    for i in sra_ids:
        result = _run_command(command=command_prefetch, id_name=i, tool_name="Prefetch")

        if result is not None:
            sucesso_ids.append(result)

    if not sucesso_ids:
        logger.error(f"Nenhum ID pôde ser baixado.")
        sys.exit("ERRO: Nenhum ID pôde ser baixado.")
    else:
        print("\nArquivos baixados com sucesso:")
        print('\n'.join(i for i in sucesso_ids))
        logger.info("Downloads concluidos utilizando o Prefetch.")
        logger.info(' '.join(i for i in sucesso_ids))

    return sucesso_ids

def sra_decompress(sra_ids:list, download_path:str, num_threads:int) -> list:
    """Recebe IDs e descomprime arquivos .sra, deixando-os em formato .fastq"""
    
    print("\nFasterq-dump: Descomprimindo arquivos .sra")

    data_path = Path(download_path) / "raw"
    threads = str(num_threads)
    sucesso_ids = []

    command_dump = ["fasterq-dump", "-O", data_path, "-x", "-e", threads]
    
    for i in sra_ids:
        sra_path = data_path / i / (i + ".sra")

        result = _run_command(command=command_dump, id_name=sra_path, tool_name="Fasterq-dump")

        if result is not None:
            sucesso_ids.append(result)

    if not sucesso_ids:
        logger.error(f"Nenhum ID pôde ser descomprimido.")
        sys.exit("ERRO: Nenhum ID pôde ser descomprimido.")
    else:
        print("\nArquivos descomprimidos com sucesso:")
        print('\n'.join(i for i in sucesso_ids))
        logger.info("Descompressão concluida utilizando o Fasterq-dump.")
        logger.info(' '.join(i for i in sucesso_ids))
        return sucesso_ids
