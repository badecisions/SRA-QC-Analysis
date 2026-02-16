
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
        sys.exit("Nenhum ID válido")
    else:
        return valid_sra_ids
