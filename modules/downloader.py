
from pathlib import Path
import sys, subprocess
from utils import verify_valid_id


def sra_downloader(sra_ids:list, download_path:str) -> list:
    """Recebe IDs, verifica se são válidos e utiliza o fasterq-dump
    para baixar os SRAs."""
    
    print("\nBAIXANDO OS ARQUIVOS SRA")

    valid_sra = verify_valid_id(sra_ids=sra_ids)
    download = Path(download_path)
    download = download / "raw"

    for i in range(len(valid_sra)):
        command_download = ["fasterq-dump", valid_sra[i], "-O", download, "-x"]

        print(f"Download {i+1}/{len(valid_sra)}: {valid_sra[i]}")

        log_path = Path("logs") / f"{valid_sra[i]}_fasterq-dump.log"

        with open(log_path, "w") as log_file:
            result = subprocess.run(command_download, stdout=log_file, stderr=log_file, text=True)

        if result.returncode != 0:
            print(f"Não foi possível baixar o SRA ID: {valid_sra[i]}")
            valid_sra.remove(valid_sra[i])

    if valid_sra == []:
        sys.exit("ERRO: Nenhum ID pôde ser baixado.")
    else:
        print("\nArquivos baixados com sucesso:")
        print('\n'.join(i for i in valid_sra))
        return valid_sra
