
from pathlib import Path
import sys, subprocess, logging

# config info log
logger = logging.getLogger(__name__)

def prefetch_run(sra_ids:list, download_path:str) -> list:
    """Coordena a execução do Prefetch para o download de arquivos .sra"""

    download = Path(download_path) / "raw"
    contador = 1

    print("\nPrefetch: Iniciando os Downloads")

    for i in sra_ids:
        command_prefetch = ["prefetch", i, "-O", download, "-v"]

        logger.info(f"Prefetch: Baixando o ID {i}")
        logger.info(f"Comando utilizado: {' '.join(map(str, command_prefetch))}")

        print(f"Download {contador}/{len(sra_ids)}: {i}")

        log_path = Path("logs") / f"{i}_prefetch.log"

        with open(log_path, "w") as log_file:
            try:
                result_prefetch = subprocess.run(command_prefetch, stdout=log_file, stderr=log_file, text=True, check=True)
            except FileNotFoundError:
                logger.error(f'Prefetch não encontrado.')
            except subprocess.CalledProcessError as e:
                logger.error(f"O Prefetch falhou ao processar {i}.")
                logger.error(f"Mensagem do terminal (stderr): {e.stderr}")
            except Exception as e:
                logger.exception(f"Um erro impediu a execução: {e}")


        if result_prefetch.returncode != 0:
            print(f"Não foi possível baixar o SRA ID: {i}")
            sra_ids.remove(i)
            logger.error(f"Não foi possível realizar o download do ID {i}")
        else:
            logger.info(f"Prefetch: Download {i} concluído")

        contador += 1

    if sra_ids == []:
        sys.exit("ERRO: Nenhum ID pôde ser baixado.")
        logger.error(f"Nenhum ID pôde ser baixado.")
    else:
        print("\nArquivos baixados com sucesso:")
        print('\n'.join(i for i in sra_ids))
        logger.info("Downloads concluidos utilizando o Prefetch.")
        logger.info(' '.join(i for i in sra_ids))

    return sra_ids

def sra_decompress(sra_ids:list, download_path:str, num_threads:int) -> list:
    """Recebe IDs e descomprime arquivos .sra, deixando-os em formato .fastq"""
    
    print("\nFasterq-dump: Descomprimindo arquivos .sra")

    data_path = Path(download_path) / "raw"
    contador = 1
    threads = str(num_threads)

    for i in sra_ids:
        sra_path = data_path / i / (i + ".sra")

        command_dump = ["fasterq-dump", sra_path, "-O", data_path, "-x", "-e", threads]

        logger.info(f"Fasterq-dump: Descomprimindo o ID {i}.sra")
        logger.info(f"Comando utilizado: {' '.join(map(str, command_dump))}")

        print(f"Descomprimindo {contador}/{len(sra_ids)}: {i}")

        log_path = Path("logs") / f"{i}_fasterq-dump.log"

        with open(log_path, "w") as log_file:
            try:
                result = subprocess.run(command_dump, stdout=log_file, stderr=log_file, text=True, check=True)
            except FileNotFoundError:
                logger.error(f'Fasterq-dump não encontrado.')
            except subprocess.CalledProcessError as e:
                logger.error(f"O Fasterq-dump falhou ao processar {i}.")
                logger.error(f"Mensagem do terminal (stderr): {e.stderr}")
            except Exception as e:
                logger.exception(f"Um erro impediu a execução: {e}")


        if result.returncode != 0:
            print(f"Não foi possível descomprimir o SRA ID: {i}")
            sra_ids.remove(i)
            logger.error(f"Não foi possível descomprimir do ID {i}")
        else:
            logger.info(f"Fasterq-dump: Descompressão {i} concluída")

        contador += 1

    if sra_ids == []:
        sys.exit("ERRO: Nenhum ID pôde ser descomprimido.")
        logger.error(f"Nenhum ID pôde ser descomprimido.")
    else:
        print("\nArquivos descomprimidos com sucesso:")
        print('\n'.join(i for i in sra_ids))
        logger.info("Descompressão concluida utilizando o Fasterq-dump.")
        logger.info(' '.join(i for i in sra_ids))
        return sra_ids
