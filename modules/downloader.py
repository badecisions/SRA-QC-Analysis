
from pathlib import Path
import sys, subprocess, logging

# config info log
logger = logging.getLogger(__name__)

def sra_downloader(sra_ids:list, download_path:str, num_threads:int) -> list:
    """Recebe IDs, verifica se são válidos e utiliza o fasterq-dump
    para baixar os SRAs."""
    
    print("\nBAIXANDO OS ARQUIVOS SRA")

    download = Path(download_path)
    download = download / "raw"
    contador = 1
    threads = str(num_threads)

    for i in sra_ids:
        command_download = ["fasterq-dump", i, "-O", download, "-x", "-e", threads]

        logger.info(f"Fasterq-dump: Baixando o ID {i}")
        logger.info(f"Comando utilizado: {' '.join(map(str, command_download))}")

        print(f"Download {contador}/{len(sra_ids)}: {i}")

        log_path = Path("logs") / f"{i}_fasterq-dump.log"

        with open(log_path, "w") as log_file:
            try:
                result = subprocess.run(command_download, stdout=log_file, stderr=log_file, text=True, check=True)
            except FileNotFoundError:
                logger.error(f'Fasterq-dump não encontrado.')
            except subprocess.CalledProcessError as e:
                logger.error(f"O Fasterq-dump falhou ao processar {i}.")
                logger.error(f"Mensagem do terminal (stderr): {e.stderr}")
            except Exception as e:
                logger.exception(f"Um erro impediu a execução: {e}")


        if result.returncode != 0:
            print(f"Não foi possível baixar o SRA ID: {i}")
            sra_ids.remove(i)
            logger.error(f"Não foi possível realizar o download do ID {i}")

        contador += 1

    if sra_ids == []:
        sys.exit("ERRO: Nenhum ID pôde ser baixado.")
        logger.error(f"Nenhum ID pôde ser baixado.")
    else:
        print("\nArquivos baixados com sucesso:")
        print('\n'.join(i for i in sra_ids))
        logger.info("Downloads concluidos utilizando o SRA Toolkit.")
        logger.info(' '.join(i for i in sra_ids))
        return sra_ids
