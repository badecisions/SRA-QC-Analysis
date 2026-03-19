import pytest
from utils.recebe_input import id_or_file

def test_somente_lista():
    # passa sra_lista, sra_file=None
    # verifica que os dois IDs estão no resultado

    result = id_or_file(sra_lista=["SRR38912321", "ERR21931832"], sra_file=None)

    assert result == ["SRR38912321", "ERR21931832"], "ERRO sra_lista: Não recebeu a lista de IDs."

def test_somente_arquivo(tmp_path):
    # cria um arquivo com dois IDs, um por linha
    # passa sra_file=caminho, sra_lista=None
    # verifica que os IDs foram lidos corretamente

    file = tmp_path / "ids.txt"
    file.write_text("SRR38912321\nERR21931832\n")

    result = id_or_file(sra_file=file, sra_lista=None)
    assert sorted(result) == sorted(["SRR38912321", "ERR21931832"]), "Erro sra_file: Não encontrou/processou o arquivo."

def test_lista_e_arquivo(tmp_path):
    # cria arquivo com um ID
    # passa também sra_lista com outro ID diferente
    # verifica que ambos estão no resultado

    file = tmp_path / "id_file_cli.txt"
    file.write_text("SRR2131921\nSRR21391312\n")

    result = id_or_file(sra_file=file, sra_lista=["SRR894891821"])
    assert sorted(result) == sorted(["SRR38912321", "ERR21931832"]), "Erro: Não conseguiu processar dois inputs (CLI e File)."

def test_deduplicacao(tmp_path):
    # coloca o mesmo ID na lista e no arquivo
    # verifica que aparece só uma vez no resultado

    file = tmp_path / "id_duplicado.txt"
    file.write_text("SRR2319312\n")

    result = id_or_file(sra_file=file, sra_lista=["SRR2319312"])
    assert result == ["SRR2319312"], "Erro: Mostrou IDs duplicados na lista final"

def test_ambos_none_encerra():
    with pytest.raises(SystemExit):
        # chame sem nenhum argumento ou com ambos None
        id_or_file()

def test_arquivo_inexistente_encerra():
    with pytest.raises(SystemExit):
        # passe um caminho que não existe
        id_or_file(sra_file="testando.txt")