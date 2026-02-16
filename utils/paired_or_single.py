from pathlib import Path

def check_layout_file(download_path:str, sra_ids:list) -> list:
    """Verifica quais arquivos são PAIRED-END e quais são SINGLE-END."""

    paired_ids = []
    single_ids = []

    download_path = Path(download_path)

    for i in sra_ids:
        temp_fastq = i + "_2.fastq"

        print(temp_fastq)

        caminho_file = download_path / temp_fastq

        if caminho_file.exists():
            paired_ids.append(i)
        else:
            single_ids.append(i)
    
    return paired_ids, single_ids
