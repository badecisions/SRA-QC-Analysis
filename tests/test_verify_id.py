import pytest
from utils.verify_id import verify_valid_id

def test_srr_valido():
    result = verify_valid_id(["SRR9312311"])
    assert result == ["SRR9312311"]

def test_err_valido():
    result = verify_valid_id(["ERR14029807"])
    assert result == ["ERR14029807"]

def test_drr_valido():
    result = verify_valid_id(["DRR03910213"])
    assert result == ["DRR03910213"]

def test_id_invalido_sozinho_encerra():
    with pytest.raises(SystemExit):
        verify_valid_id(["PRS0239102D"])

def test_lista_mista():
    result = verify_valid_id(["SRR9312311", "ERR2312132", "DASDASDA", "113213213", "DRR123213941"])
    assert result == ["SRR9312311", "ERR2312132", "DRR123213941"]

def test_todos_invalidos_encerra():
    with pytest.raises(SystemExit):
        verify_valid_id(["INVALIDO", "123456", "XRRASDA"])