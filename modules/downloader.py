
from pathlib import Path
import sys, subprocess


def sra_downloader(sra_ids:list, download_path:str) -> list:
    """Recebe IDs, verifica se são válidos e utiliza o fasterq-dump
    para baixar os SRAs."""
    
    print("\nBAIXANDO OS ARQUIVOS SRA")

    download = Path(download_path)
    download = download / "raw"
    contador = 1

    for i in sra_ids:
        command_download = ["fasterq-dump", i, "-O", download, "-x"]

        print(f"Download {contador}/{len(sra_ids)}: {i}")

        log_path = Path("logs") / f"{i}_fasterq-dump.log"

        with open(log_path, "w") as log_file:
            result = subprocess.run(command_download, stdout=log_file, stderr=log_file, text=True)

        if result.returncode != 0:
            print(f"Não foi possível baixar o SRA ID: {i}")
            sra_ids.remove(i)

            contador += 1

    if sra_ids == []:
        sys.exit("ERRO: Nenhum ID pôde ser baixado.")
    else:
        print("\nArquivos baixados com sucesso:")
        print('\n'.join(i for i in sra_ids))
        return sra_ids
