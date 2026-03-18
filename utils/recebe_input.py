from pathlib import Path
import logging, sys

logger = logging.getLogger(__name__)

def id_or_file(sra_lista: list[str]| None = None, sra_file: str | None = None) -> list:
    """Lida com o input, seja ele IDs digitados no terminal ou arquivo .txt"""

    if not sra_lista and not sra_file:
        logger.error("ERRO: Forneça IDs via --sra ou --file.")
        sys.exit("ERRO: Forneça IDs via --sra ou --file.")

    lista_sra = []

    if sra_lista:
        lista_sra.extend(sra_lista)

    if sra_file:
        path_arquivo = Path(sra_file)

        if path_arquivo.exists() and path_arquivo.is_file():
            try:
                with open(sra_file, "r") as f:
                    ids_arquivo = [line.strip() for line in f if line.strip()]
                    lista_sra.extend(ids_arquivo)

            except Exception as erro:
                print(f"Erro ao ler o arquivo: {erro}")
        elif not path_arquivo.exists():
            logger.error(f"ERRO: Arquivo não encontrado: {path_arquivo}")
            sys.exit(f"ERRO: Arquivo não encontrado: {path_arquivo}")

    lista_sra = list(dict.fromkeys(lista_sra))

    print(f"\nTotal de IDs para processar: {len(lista_sra)}")

    return lista_sra
