from typing import List, Optional
from pathlib import Path

def id_or_file(sra_lista: Optional[List[str]] = None, sra_file: Optional[str] = None) -> list:
    """Lida com o input, seja ele IDs digitados no terminal ou arquivo .txt"""

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


    lista_sra = list(set(lista_sra))

    print(f"\nTotal de IDs para processar: {len(lista_sra)}")

    return lista_sra
