import pytest
from utils.paired_or_single import check_layout_file

def test_paired_end_detectado(tmp_path):
    # verifica que SRR está em paired_ids e não em single_ids

    (tmp_path / "raw").mkdir(parents=True)
    (tmp_path / "raw" / "SRR2131412_2.fastq").touch()

    paired, single = check_layout_file(download_path=tmp_path, sra_ids=["SRR2131412"])
    assert paired == ["SRR2131412"] and not single, "ERRO: não identificou o arquivo paired."

def test_single_end_detectado(tmp_path):
    # verifica que SRR está em single_ids e não em paired_ids

    (tmp_path / "raw").mkdir(parents=True)
    (tmp_path / "raw" / "SRR2394121_1.fastq").touch()

    paired, single = check_layout_file(download_path=tmp_path, sra_ids=["SRR2394121"])
    assert single == ["SRR2394121"] and not paired, "ERRO: não identificou o arquivo single."

def test_lista_mista(tmp_path):
    # verifica que cada um foi classificado corretamente

    (tmp_path / "raw").mkdir(parents=True)
    (tmp_path / "raw" / "SRR23912313_2.fastq").touch()
    (tmp_path / "raw" / "SRR29318412_1.fastq").touch()

    paired, single = check_layout_file(download_path=tmp_path, sra_ids=["SRR29318412", "SRR23912313"])
    assert single == ["SRR29318412"] and paired == ["SRR23912313"], "ERRO: não separou paired e single."

def test_retorno_e_tupla(tmp_path):
    # verifica que o retorno é sempre duas listas
    # input não pode ser vazio — a função encerra com sys.exit

    (tmp_path / "raw").mkdir(parents=True)
    (tmp_path / "raw" / "SRR8523182_2.fastq").touch()
    (tmp_path / "raw" / "SRR8471231_1.fastq").touch()

    paired, single = check_layout_file(download_path=tmp_path, sra_ids=["SRR8523182", "SRR8471231"])
    assert isinstance(paired, list), "ERRO: o output paired não é lista."
    assert isinstance(single, list), "ERRO: o output single não é lista."

