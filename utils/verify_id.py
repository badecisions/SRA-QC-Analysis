
import re, sys, logging

logger = logging.getLogger(__name__)

def verify_valid_id(sra_ids:list) -> list:
    """Verifica se os IDs cedidos pelo usuário são válidos,
    retorna uma lista com os válidos, caso seja vazia, para o programa."""
    padrao = r'^[SED]RR\d+$'
    valid_sra_ids = []

    for i in sra_ids:
        if re.match(padrao, i) is None:
            print(f"O ID {i} é inválido")
            logger.error(f"ID inválido: {i}")
        else:
            valid_sra_ids.append(i)

    if not valid_sra_ids:
        print("Nenhum dos IDs digitados são válidos")
        logger.error("ERRO: Nenhum ID válido.")
        sys.exit("ERRO: Nenhum ID válido.")
    else:
        logger.info(f"IDs válidos: {' '.join(valid_sra_ids)}")
        return valid_sra_ids