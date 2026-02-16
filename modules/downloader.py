
from pathlib import Path
import re, sys, subprocess


def verify_name_run(sra_ids:list) -> list:
    """Verifica se os IDs cedidos pelo usuário são válidos,
    retorna uma lista com os válidos, caso seja vazia, para o programa."""
    padrao = r'^[SED]RR\d+$'
    valid_sra_ids = []

    for i in sra_ids:
        if re.match(padrao, i) == None:
            print(f"O ID {i} é inválido")
        else:
            valid_sra_ids.append(i)

    if len(valid_sra_ids) == 0:
        print("Nenhum dos IDs digitados são válidos")
        sys.exit("ERRO: Nenhum ID válido.")
    else:
        return valid_sra_ids


def sra_downloader(sra_ids:list):
    """Recebe IDs de SRA, verifica se são válidos e utiliza o fasterq-dump
    para baixar os SRAs."""

    valid_sra = verify_name_run(sra_ids=sra_ids)
    dowload_path = Path("data/raw")
    command_download = ["fasterqdump", ""]